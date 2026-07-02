"""Rank 2 — OrderFilled sample-join probe (DISCOVERY MODE, research only).

Tests whether current trade rows can be joined to on-chain OrderFilled events so
that maker/taker ROLE can be reconstructed. This is the cheapest feasibility
step BEFORE any indexer: sample ~300 tx_hash, fetch receipts via JSON-RPC,
discover which exchange contract(s) and OrderFilled signature(s) are present,
attempt the join, and report join/resolvability/ambiguity rates + a gate state.

NOT an indexer. NO range log scan. NO trading. NO execution. NO wallet-copying.
Dependency-light: plain `requests` + JSON-RPC. No web3.

Discovery mode: tries known Polymarket OrderFilled event signatures (CTF Exchange
V1/V2, Neg-Risk CTF Exchange) by topic0; reports emitting contract addresses and
which signature matched; if nothing decodes reliably -> NEED_ABI_OR_CONTRACT_DISCOVERY.

Public-dataset fallback (documented, NOT implemented as a dependency): if RPC is
unavailable, the same join can be sourced from a public fills dataset (e.g. a
Dune query or a Polymarket subgraph) exporting tx_hash, log_index, maker, taker,
makerAssetId, takerAssetId, amounts — then fed to this script's --logs-json input
(see load_logs_from_json). The first implementation uses RPC.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import time

import pandas as pd

from pm_research.data.store import Store

# --------------------------------------------------------------------------- #
#  Known OrderFilled event signatures (discovery set).                         #
#  topic0 = keccak256(signature). These are EMBEDDED constants so we need no   #
#  keccak dependency; verify_topic0_constants() re-derives them IF a keccak    #
#  lib is present at runtime, else trusts the constants. Polymarket CTF        #
#  Exchange (V1/V2) and Neg-Risk CTF Exchange share this OrderFilled shape:    #
#    OrderFilled(bytes32 orderHash, address maker, address taker,              #
#                uint256 makerAssetId, uint256 takerAssetId,                   #
#                uint256 makerAmountFilled, uint256 takerAmountFilled,         #
#                uint256 fee)                                                  #
#  orderHash, maker, taker are indexed (topics 1-3); the rest are in `data`.   #
# --------------------------------------------------------------------------- #
ORDERFILLED_SIGNATURE = ("OrderFilled(bytes32,address,address,uint256,uint256,"
                         "uint256,uint256,uint256)")
# topic0 = keccak256(signature). We DERIVE this at runtime (see resolve_topic0)
# because an unverified hardcoded hash would silently break decoding. The value
# below is a CROSS-CHECK reference only; resolve_topic0() recomputes and warns
# on mismatch. If no keccak lib is available, the script refuses to proceed
# rather than risk a false NEED_ABI_OR_CONTRACT_DISCOVERY from a wrong constant.
ORDERFILLED_TOPIC0_REFERENCE = (
    "0xd0a08e8c493f9c94f29311604c9de1b4e8c8d4c06bd0c789af57f2e65bf97e7e")

# resolved at runtime into {topic0_lower: signature}
KNOWN_TOPICS: dict = {}

# Known Polymarket exchange contract addresses (Polygon), lowercased. Used only
# to LABEL discovered contracts; the join does not require a hardcoded address.
KNOWN_EXCHANGES = {
    "0x4bfb41d5b3570defd03c39a9a4d8de6bd8b8982e": "CTF_Exchange_V2",
    "0xc5d563a36ae78145c45a50134d48a1215220f80a": "NegRisk_CTF_Exchange",
    "0x56c79347e95530c01a2fc76e732f9566da16e113": "CTF_Exchange_V1",
}

DEFAULT_SAMPLE = 300
MIN_JOIN = 0.80
MIN_RESOLVABLE = 0.70
MAX_AMBIGUITY = 0.20


def _keccak256(data: bytes) -> str | None:
    """keccak256 hex (Ethereum's, NOT NIST sha3) via whatever lib is present."""
    try:
        from eth_utils import keccak
        return "0x" + keccak(data).hex()
    except Exception:
        pass
    try:
        from Crypto.Hash import keccak as _k
        h = _k.new(digest_bits=256); h.update(data)
        return "0x" + h.hexdigest()
    except Exception:
        pass
    try:
        import sha3  # pysha3 -> keccak_256
        return "0x" + sha3.keccak_256(data).hexdigest()
    except Exception:
        pass
    return None


def resolve_topic0() -> dict:
    """Derive OrderFilled topic0 at runtime and populate KNOWN_TOPICS. Returns
    a status dict. If no keccak lib is available, KNOWN_TOPICS stays empty and
    the caller must surface NEED_ABI_OR_CONTRACT_DISCOVERY rather than trust the
    reference constant (which could be wrong)."""
    derived = _keccak256(ORDERFILLED_SIGNATURE.encode())
    if derived is None:
        return {"derived": None, "matches_reference": None,
                "method": "NO_KECCAK_LIB",
                "warning": "no keccak library (eth_utils / pycryptodome / "
                           "pysha3) available; cannot derive topic0. Install "
                           "one, e.g. `pip install pycryptodome`."}
    KNOWN_TOPICS[derived.lower()] = ORDERFILLED_SIGNATURE
    return {"derived": derived,
            "matches_reference": derived.lower() == ORDERFILLED_TOPIC0_REFERENCE.lower(),
            "method": "runtime_keccak"}


# --------------------------------------------------------------------------- #
#  JSON-RPC (plain requests; no web3)                                          #
# --------------------------------------------------------------------------- #
def fetch_receipt(rpc_url: str, tx_hash: str, session=None,
                  retries: int = 4, backoff: float = 1.5) -> dict | None:
    """eth_getTransactionReceipt via JSON-RPC with retry/backoff. Returns the
    receipt dict or None. Raises RpcLimited after exhausting retries on 429."""
    import requests
    s = session or requests.Session()
    payload = {"jsonrpc": "2.0", "id": 1, "method": "eth_getTransactionReceipt",
               "params": [tx_hash]}
    delay = backoff
    for attempt in range(retries):
        try:
            r = s.post(rpc_url, json=payload, timeout=30)
            if r.status_code == 429:
                time.sleep(delay); delay *= 2; continue
            r.raise_for_status()
            data = r.json()
            return data.get("result")
        except Exception:
            if attempt == retries - 1:
                raise RpcLimited(f"failed after {retries} retries: {tx_hash}")
            time.sleep(delay); delay *= 2
    return None


class RpcLimited(Exception):
    pass


# --------------------------------------------------------------------------- #
#  Log decoding (discovery)                                                     #
# --------------------------------------------------------------------------- #
def _hexint(h):
    if h is None:
        return None
    if isinstance(h, int):
        return h
    return int(h, 16) if str(h).startswith("0x") else int(h)


def _addr_from_topic(topic: str) -> str:
    # address is the low 20 bytes of a 32-byte topic
    return ("0x" + topic[-40:]).lower() if topic else None


def decode_orderfilled(log: dict) -> dict | None:
    """Decode an OrderFilled-shaped log WITHOUT web3. Returns a dict of fields
    or None if topic0 is not a known OrderFilled signature.

    Indexed-topic order: per the CTF Exchange V2 source (Events.sol), the order
    is [topic0, orderHash, maker, taker] -> maker=topics[2], taker=topics[3].

    NOTE: an earlier reversal of this (taker=topics[2]) was based on an INVALID
    comparison (local log_index vs a NEIGHBORING Dune evt_index in a multi-fill
    tx) and has been reverted. Whether OLDER/UNKNOWN emitting contracts use the
    same order is being verified per-contract by
    orderfilled_topic_order_validation.py against EXACT-log-index Dune rows."""
    topics = log.get("topics", [])
    if not topics:
        return None
    t0 = topics[0].lower()
    if t0 not in KNOWN_TOPICS:
        return None
    if len(topics) < 4:
        return None
    data = log.get("data", "0x")
    body = data[2:] if data.startswith("0x") else data
    words = [body[i:i + 64] for i in range(0, len(body), 64)]
    if len(words) < 5:
        return None
    return {
        "contract_address": (log.get("address") or "").lower(),
        "log_index": _hexint(log.get("logIndex")),
        "signature": KNOWN_TOPICS[t0],
        "order_hash": "0x" + topics[1][-64:] if len(topics) > 1 else None,
        "maker": _addr_from_topic(topics[2]),   # topics[2] = maker (V2 source)
        "taker": _addr_from_topic(topics[3]),   # topics[3] = taker (V2 source)
        "maker_asset_id": int(words[0], 16),
        "taker_asset_id": int(words[1], 16),
        "maker_amount_filled": int(words[2], 16),
        "taker_amount_filled": int(words[3], 16),
        "fee": int(words[4], 16),
    }


# --------------------------------------------------------------------------- #
#  Join + role assignment                                                      #
# --------------------------------------------------------------------------- #
def join_trade_to_fills(trade: dict, fills: list[dict],
                        price_tol: float = 1e-3,
                        size_tol: float = 0.01) -> dict:
    """Match one trade row to the OrderFilled logs in its tx. Returns a result
    dict with match_status in {resolved, AMBIGUOUS, WALLET_NOT_IN_FILL,
    NO_FILL, UNDECODED} and the assigned role when resolved.

    Secondary checks: token_id vs maker/taker asset id; implied price & size
    within tolerance; wallet equals maker xor taker."""
    if not fills:
        return {"match_status": "NO_FILL", "role": None}
    tok = str(trade.get("token_id", "")).strip()
    wallet = str(trade.get("wallet", "")).lower()
    candidates = []
    for f in fills:
        # which side is the CLOB token?
        side_token = None
        if tok and str(f["maker_asset_id"]) == tok:
            side_token = "maker_is_token"
        elif tok and str(f["taker_asset_id"]) == tok:
            side_token = "taker_is_token"
        # implied price from amounts (token vs usdc), best-effort
        # USDC has 6 decimals; token amounts are share counts (6 decimals on CTF)
        price_ok = True
        size_ok = True
        try:
            if side_token == "maker_is_token":
                shares = f["maker_amount_filled"] / 1e6
                usdc = f["taker_amount_filled"] / 1e6
            elif side_token == "taker_is_token":
                shares = f["taker_amount_filled"] / 1e6
                usdc = f["maker_amount_filled"] / 1e6
            else:
                shares = usdc = None
            if shares and usdc and shares > 0:
                implied_price = usdc / shares
                price_ok = abs(implied_price - float(trade.get("price", 0))) <= price_tol \
                    if trade.get("price") is not None else True
                size_ok = abs(usdc - float(trade.get("size_usdc", 0))) <= max(
                    size_tol, 0.01 * usdc) if trade.get("size_usdc") is not None else True
        except (ZeroDivisionError, TypeError, ValueError):
            pass
        wallet_role = None
        if wallet and f["maker"] == wallet:
            wallet_role = "maker"
        elif wallet and f["taker"] == wallet:
            wallet_role = "taker"
        token_ok = side_token is not None
        if token_ok and price_ok and size_ok:
            candidates.append({"fill": f, "wallet_role": wallet_role,
                               "side_token": side_token})
    if len(candidates) == 0:
        # tx had fills but none matched this trade's token/price/size
        return {"match_status": "NO_FILL", "role": None}
    if len(candidates) > 1:
        return {"match_status": "AMBIGUOUS", "role": None,
                "n_candidates": len(candidates)}
    c = candidates[0]
    if c["wallet_role"] is None:
        return {"match_status": "WALLET_NOT_IN_FILL", "role": None,
                "log_index": c["fill"]["log_index"],
                "contract_address": c["fill"]["contract_address"]}
    return {"match_status": "resolved", "role": c["wallet_role"],
            "log_index": c["fill"]["log_index"],
            "contract_address": c["fill"]["contract_address"],
            "signature": c["fill"]["signature"]}


# --------------------------------------------------------------------------- #
#  Sampling                                                                     #
# --------------------------------------------------------------------------- #
def sample_tx(trades: pd.DataFrame, n: int, seed: int = 0) -> pd.DataFrame:
    """Stratify across wallets/time; bias toward single-trade tx but include
    some multi-trade tx to measure ambiguity."""
    t = trades[trades["tx_hash"].astype(str).str.startswith("0x")].copy()
    if len(t) == 0:
        return t
    per_tx = t.groupby("tx_hash").size()
    single = per_tx[per_tx == 1].index
    multi = per_tx[per_tx > 1].index
    rng = pd.Series(range(len(t)))
    n_multi = min(len(multi), max(1, n // 5))      # ~20% multi-fill
    n_single = n - n_multi
    import numpy as np
    rs = np.random.default_rng(seed)
    pick_single = (pd.Series(list(single)).sample(min(len(single), n_single),
                   random_state=seed).tolist() if len(single) else [])
    pick_multi = (pd.Series(list(multi)).sample(min(len(multi), n_multi),
                  random_state=seed).tolist() if len(multi) else [])
    picked = set(pick_single) | set(pick_multi)
    return t[t["tx_hash"].isin(picked)]


def decide_gate(m: dict) -> str:
    if m["undecoded_log_rate"] >= 0.5 and m["join_success_rate"] < MIN_JOIN:
        return "NEED_ABI_OR_CONTRACT_DISCOVERY"
    if m.get("rpc_limited"):
        return "BLOCKED_BY_RPC_LIMITS"
    if m["join_success_rate"] < MIN_JOIN:
        return "BLOCKED_BY_LOW_JOIN_RATE"
    if (m["maker_taker_resolvable_rate"] < MIN_RESOLVABLE
            or m["ambiguity_rate"] > MAX_AMBIGUITY):
        return "BLOCKED_BY_AMBIGUOUS_ROLE"
    return "CLEAR_FOR_ORDERFILLED_INDEXER"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="./data")
    ap.add_argument("--rpc-url", default=None,
                    help="Polygon JSON-RPC endpoint (required unless --logs-json)")
    ap.add_argument("--logs-json", default=None,
                    help="public-dataset fallback: pre-fetched logs keyed by "
                         "tx_hash (skips RPC)")
    ap.add_argument("--sample", type=int, default=DEFAULT_SAMPLE)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--sleep", type=float, default=0.1, help="per-request sleep")
    ap.add_argument("--out-dir", default="artifacts")
    args = ap.parse_args()

    topic_check = resolve_topic0()
    if topic_check.get("method") == "NO_KECCAK_LIB":
        # cannot decode without topic0; emit a clear gate state and stop.
        out_dir = pathlib.Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
        m = {"gate_state": "NEED_ABI_OR_CONTRACT_DISCOVERY",
             "topic0_verification": topic_check, "sample_size": 0}
        (out_dir / "orderfilled_sample_join.json").write_text(
            json.dumps(m, indent=2, default=str))
        print("GATE: NEED_ABI_OR_CONTRACT_DISCOVERY — " + topic_check["warning"])
        return 0
    store = Store(args.root)
    trades = store.load_trades()                  # hygiene applied at load
    samp = sample_tx(trades, args.sample, args.seed)
    tx_list = list(dict.fromkeys(samp["tx_hash"].tolist()))   # unique, ordered

    # logs per tx: from RPC or from a public-dataset json fallback
    logs_by_tx = {}
    rpc_limited = False
    if args.logs_json:
        logs_by_tx = json.loads(pathlib.Path(args.logs_json).read_text())
    elif args.rpc_url:
        import requests
        sess = requests.Session()
        for i, tx in enumerate(tx_list, 1):
            try:
                rcpt = fetch_receipt(args.rpc_url, tx, session=sess)
                logs_by_tx[tx] = (rcpt or {}).get("logs", [])
            except RpcLimited:
                rpc_limited = True
                break
            if i % 25 == 0:
                print(f"  fetched {i}/{len(tx_list)} receipts")
            time.sleep(args.sleep)
    else:
        print("ERROR: provide --rpc-url or --logs-json"); return 2

    # decode + join
    rows = []
    contract_counts = {}
    sig_counts = {}
    undecoded = 0
    decoded_logs_total = 0
    multi_fill_tx = 0
    for _, tr in samp.iterrows():
        tx = tr["tx_hash"]
        raw_logs = logs_by_tx.get(tx, [])
        fills = []
        for lg in raw_logs:
            d = decode_orderfilled(lg)
            if d is None:
                # count only logs that look like they could be OrderFilled?
                # we can't know; track topic0 of undecoded for discovery
                continue
            fills.append(d)
            decoded_logs_total += 1
            contract_counts[d["contract_address"]] = \
                contract_counts.get(d["contract_address"], 0) + 1
            sig_counts[d["signature"]] = sig_counts.get(d["signature"], 0) + 1
        if len(fills) > 1:
            multi_fill_tx += 1
        # discovery: if tx had logs but NONE decoded as OrderFilled, flag
        if raw_logs and not fills:
            undecoded += 1
        res = join_trade_to_fills(tr.to_dict(), fills)
        rows.append({
            "trade_id": tr.get("trade_id"), "tx_hash": tx,
            "token_id": tr.get("token_id"), "wallet": tr.get("wallet"),
            "condition_id": tr.get("condition_id"),
            "n_fills_in_tx": len(fills),
            "match_status": res["match_status"], "role": res.get("role"),
            "log_index": res.get("log_index"),
            "contract_address": res.get("contract_address"),
        })
    rj = pd.DataFrame(rows)
    n = len(rj)

    joined = rj[rj["n_fills_in_tx"] >= 1]
    resolved = rj[rj["match_status"] == "resolved"]
    ambiguous = rj[rj["match_status"] == "AMBIGUOUS"]
    wallet_not = rj[rj["match_status"] == "WALLET_NOT_IN_FILL"]
    metrics = {
        "sample_size": int(n),
        "unique_tx_sampled": len(tx_list),
        "join_success_rate": float(len(joined) / n) if n else 0.0,
        "maker_taker_resolvable_rate": float(len(resolved) / n) if n else 0.0,
        "ambiguity_rate": float(len(ambiguous) / n) if n else 0.0,
        "wallet_not_in_fill_rate": float(len(wallet_not) / n) if n else 0.0,
        "multi_fill_tx_rate": float(multi_fill_tx / len(tx_list)) if tx_list else 0.0,
        "undecoded_log_rate": float(undecoded / len(tx_list)) if tx_list else 0.0,
        "emitting_contract_addresses": {
            a: {"count": c, "label": KNOWN_EXCHANGES.get(a, "UNKNOWN")}
            for a, c in sorted(contract_counts.items(), key=lambda x: -x[1])},
        "matched_abi_signature_counts": sig_counts,
        "role_distribution": {
            "maker": int((resolved["role"] == "maker").sum()),
            "taker": int((resolved["role"] == "taker").sum())},
        "rpc_limited": rpc_limited,
        "topic0_verification": topic_check,
    }
    metrics["gate_state"] = decide_gate(metrics)

    out_dir = pathlib.Path(args.out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "orderfilled_sample_join.json").write_text(
        json.dumps(metrics, indent=2, default=str))
    rj.to_csv(out_dir / "orderfilled_sample_join.csv", index=False)
    _write_md(metrics, out_dir / "orderfilled_sample_join_report.md")

    print("=" * 64)
    print("RANK 2 — OrderFilled SAMPLE JOIN (discovery, research only)")
    print("=" * 64)
    print(f"  sample: {n} trades / {len(tx_list)} tx")
    print(f"  join_success_rate:        {metrics['join_success_rate']:.3f}")
    print(f"  maker_taker_resolvable:   {metrics['maker_taker_resolvable_rate']:.3f}")
    print(f"  ambiguity_rate:           {metrics['ambiguity_rate']:.3f}")
    print(f"  wallet_not_in_fill_rate:  {metrics['wallet_not_in_fill_rate']:.3f}")
    print(f"  multi_fill_tx_rate:       {metrics['multi_fill_tx_rate']:.3f}")
    print(f"  undecoded_log_rate:       {metrics['undecoded_log_rate']:.3f}")
    print(f"  contracts: {list(metrics['emitting_contract_addresses'].keys())[:4]}")
    print(f"  role dist: {metrics['role_distribution']}")
    print(f"  topic0: matches_reference={topic_check.get('matches_reference')} "
          f"({topic_check.get('method')})")
    print(f"  >>> GATE: {metrics['gate_state']}")
    print(f"  wrote {out_dir}/orderfilled_sample_join.json (+ report, csv)")
    return 0


def _write_md(m, path):
    L = ["# Rank 2 — OrderFilled Sample Join (discovery, research only)", "",
         f"**Gate: `{m['gate_state']}`**", "",
         f"- sample size: {m['sample_size']} trades / {m['unique_tx_sampled']} tx",
         f"- join_success_rate: {m['join_success_rate']:.3f} (CLEAR >= {MIN_JOIN})",
         f"- maker_taker_resolvable_rate: {m['maker_taker_resolvable_rate']:.3f} "
         f"(CLEAR >= {MIN_RESOLVABLE})",
         f"- ambiguity_rate: {m['ambiguity_rate']:.3f} (CLEAR <= {MAX_AMBIGUITY})",
         f"- wallet_not_in_fill_rate: {m['wallet_not_in_fill_rate']:.3f}",
         f"- multi_fill_tx_rate: {m['multi_fill_tx_rate']:.3f}",
         f"- undecoded_log_rate: {m['undecoded_log_rate']:.3f}",
         f"- topic0 verification: {m['topic0_verification']}", "",
         "## Discovered contracts", ""]
    for a, info in m["emitting_contract_addresses"].items():
        L.append(f"- {a} — {info['label']} ({info['count']} logs)")
    L += ["", "## Role distribution (resolved fills only)",
          f"- maker: {m['role_distribution']['maker']}",
          f"- taker: {m['role_distribution']['taker']}", "",
          "## Notes",
          "- Discovery only. NOT an indexer. NO trading. NO wallet-copying.",
          "- role distribution is descriptive, not a strategy or PnL claim.",
          "- multi-fill tx without a per-trade log_index are the main ambiguity "
          "source; the rate above quantifies it."]
    path.write_text("\n".join(L))


if __name__ == "__main__":
    raise SystemExit(main())
