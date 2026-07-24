"""REV23 Finding 4 I0A -- descriptor, descriptor-set, exact physical, decoded
logical, structural, selected sidecar, and unit validation plus dispatch.

Scope: REV23_FINDING4_I0A_SCOPE_REVISION_08
Governing sections: Finding 4 SS3.4-3.7, 5.1-5.6

This module performs no filesystem, network, subprocess, or Parquet-decoding
side effects. It never imports governing_package.py.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from typing import Mapping, Optional, Tuple

from .canonical import (
    AssuranceLevel,
    I0AResultCode,
    StructuralRelationSchemaId,
    TypedCell,
    TypedCellTag,
    TypedFieldSpec,
    ValidationResult,
    canonical_typed_row_bytes,
)
from .claim_hashes import (
    compute_claim_scope_sha256,
    compute_snapshot_claim_semantic_sha256,
)
from .finding4_registry import (
    FrozenPathGrammarId,
    PreparedObjectRole,
    PreparedUnitKind,
    PublicationMode,
    UnitContext,
    validate_normalized_relative_path,
)

__all__ = [
    "PreparedObjectDescriptor",
    "DescriptorSetInput",
    "PhysicalPayloadResult",
    "AcceptedRegistryLogicalValidationInput",
    "StructuralRelationValidationInput",
    "SelectedJsonPayloadInput",
    "StructuralMemberName",
    "StructuralJsonMemberInput",
    "PreparedUnitStructureInput",
    "FilesystemClaimKind",
    "FilesystemValidationRequest",
    "FullPreparedObjectValidationRequest",
    "FullPreparedUnitValidationRequest",
    "dispatch_i0a_unit_validation",
    "validate_prepared_object_descriptor",
    "validate_prepared_descriptor_set",
    "reconcile_physical_payload",
    "validate_payload_logical_representation",
    "validate_structural_relation",
    "validate_selected_json_payload",
    "validate_structural_json_member",
    "validate_prepared_unit_structure",
    "validate_filesystem_facts",
    "validate_full_prepared_object",
    "validate_full_prepared_unit",
]

@dataclass(frozen=True)
class PreparedObjectDescriptor:
    object_ordinal: int
    object_role: PreparedObjectRole
    content_schema_id: str
    publication_mode: PublicationMode
    durable_source_path: str
    canonical_target_path: str
    file_size_bytes: int
    file_sha256: str
    logical_sha256: Optional[str]
    sidecar_of_object_ordinal: Optional[int]


@dataclass(frozen=True)
class DescriptorSetInput:
    unit_context: UnitContext
    descriptors: Tuple[PreparedObjectDescriptor, ...]
    snapshot_claim_semantic_bytes: Optional[bytes]


@dataclass(frozen=True)
class PhysicalPayloadResult:
    code: I0AResultCode
    established_assurances: Tuple[AssuranceLevel, ...]
    observed_size_bytes: Optional[int]
    observed_sha256: Optional[str]


@dataclass(frozen=True)
class AcceptedRegistryLogicalValidationInput:
    schema_id: str
    decoded_rows: Optional[Tuple[Mapping[str, object], ...]]
    expected_logical_sha256: str
    accepted_registry_bytes: bytes


@dataclass(frozen=True)
class StructuralRelationValidationInput:
    schema_id: StructuralRelationSchemaId
    decoded_rows: Tuple[Mapping[str, object], ...]
    expected_logical_sha256: str


@dataclass(frozen=True)
class SelectedJsonPayloadInput:
    descriptor_set_input: DescriptorSetInput
    selected_object_ordinal: int
    selected_payload_bytes: bytes
    paired_target_payload_bytes: Optional[bytes]
    accepted_registry_bytes: bytes


class StructuralMemberName(Enum):
    CLAIM_SCOPE_JSON = "CLAIM_SCOPE.json"
    CLAIM_SCOPE_SHA256 = "CLAIM_SCOPE.sha256"
    CLAIM_SEMANTIC_JSON = "CLAIM_SEMANTIC.json"
    CLAIM_SEMANTIC_SHA256 = "CLAIM_SEMANTIC.sha256"
    PREPARATION_PLAN_JSON = "PREPARATION_PLAN.json"
    PREPARATION_PLAN_SHA256 = "PREPARATION_PLAN.sha256"
    PREPARED_UNIT_JSON = "PREPARED_UNIT.json"
    PREPARED_UNIT_SHA256 = "PREPARED_UNIT.sha256"


@dataclass(frozen=True)
class StructuralJsonMemberInput:
    unit_context: UnitContext
    run_id: str
    prepared_unit_id: str
    member_name: StructuralMemberName
    payload_bytes: bytes
    expected_file_size_bytes: int
    expected_file_sha256: str
    paired_target_bytes: Optional[bytes]
    paired_target_expected_file_size_bytes: Optional[int]
    paired_target_expected_file_sha256: Optional[str]


@dataclass(frozen=True)
class PreparedUnitStructureInput:
    accepted_registry_bytes: bytes
    unit_context: UnitContext
    structural_members: Mapping[StructuralMemberName, bytes]
    object_payload_bytes_by_ordinal: Mapping[int, bytes]


class FilesystemClaimKind(Enum):
    SYMLINK_FREE_REGULAR_FILE = "SYMLINK_FREE_REGULAR_FILE"
    CANONICAL_TARGET_REOPENED = "CANONICAL_TARGET_REOPENED"
    REUSE_IMMUTABLE_SOURCE_VALIDATED = "REUSE_IMMUTABLE_SOURCE_VALIDATED"
    PREPARED_OBJECT_FULL = "PREPARED_OBJECT_FULL"
    PREPARED_UNIT_FULL = "PREPARED_UNIT_FULL"


@dataclass(frozen=True)
class FilesystemValidationRequest:
    claim_kind: FilesystemClaimKind
    claimed_path: str
    caller_asserted_value: Optional[bool]


@dataclass(frozen=True)
class FullPreparedObjectValidationRequest:
    selected_input: SelectedJsonPayloadInput
    filesystem_request: FilesystemValidationRequest


@dataclass(frozen=True)
class FullPreparedUnitValidationRequest:
    unit_input: PreparedUnitStructureInput
    filesystem_requests: Tuple[FilesystemValidationRequest, ...]


# ---------------------------------------------------------------------------
# Private symbols (absent from __all__)
# ---------------------------------------------------------------------------


class _PrivateDescriptorSetInvariantCode(Enum):
    PRIVATE_DESCRIPTOR_SET_INVARIANTS_VALID = "PRIVATE_DESCRIPTOR_SET_INVARIANTS_VALID"
    PRIVATE_DESCRIPTOR_SET_ROLE_CARDINALITY_INVALID = (
        "PRIVATE_DESCRIPTOR_SET_ROLE_CARDINALITY_INVALID"
    )
    PRIVATE_DESCRIPTOR_SET_ORDINAL_SEQUENCE_INVALID = (
        "PRIVATE_DESCRIPTOR_SET_ORDINAL_SEQUENCE_INVALID"
    )
    PRIVATE_DESCRIPTOR_SET_CANONICAL_TARGET_DUPLICATE = (
        "PRIVATE_DESCRIPTOR_SET_CANONICAL_TARGET_DUPLICATE"
    )
    PRIVATE_DESCRIPTOR_SET_SIDECAR_RELATION_INVALID = (
        "PRIVATE_DESCRIPTOR_SET_SIDECAR_RELATION_INVALID"
    )


@dataclass(frozen=True)
class _DescriptorSetInvariantSummary:
    object_ordinal: int
    object_role: PreparedObjectRole
    canonical_target_path: str
    is_sidecar: bool
    sidecar_of_object_ordinal: Optional[int]


@dataclass(frozen=True)
class _DescriptorSetInvariantInput:
    summaries: Tuple[_DescriptorSetInvariantSummary, ...]
    expected_role_counts: Mapping[PreparedObjectRole, int]


@dataclass(frozen=True)
class _PrivateDescriptorSetInvariantResult:
    code: _PrivateDescriptorSetInvariantCode
    summaries: Optional[Tuple[_DescriptorSetInvariantSummary, ...]]


def _validate_descriptor_set_invariants(
    value: _DescriptorSetInvariantInput,
) -> _PrivateDescriptorSetInvariantResult:
    # Exact Revision 09 private ordered_outcomes
    # (I0A_PUBLIC_API_CONTRACT.json _validate_descriptor_set_invariants):
    # role cardinality, ordinal sequence, canonical-target uniqueness,
    # sidecar relation, then valid. The closed _DescriptorSetInvariantInput
    # and _DescriptorSetInvariantSummary carry no logical_sha256 or
    # partition-entry value domain, so this reducer MUST NOT inspect or
    # decide logical-hash nullability or same-ordinal partition binding;
    # Revision 09 assigns logical-hash nullability to
    # validate_prepared_object_descriptor and same-ordinal partition
    # binding to validate_prepared_descriptor_set. Every failure returns
    # summaries=None; only valid returns the complete ordinal-order
    # summaries.
    summaries = value.summaries

    role_counts: dict = {}
    for s in summaries:
        role_counts[s.object_role] = role_counts.get(s.object_role, 0) + 1
    for role, expected in value.expected_role_counts.items():
        if role_counts.get(role, 0) != expected:
            return _PrivateDescriptorSetInvariantResult(
                code=_PrivateDescriptorSetInvariantCode.PRIVATE_DESCRIPTOR_SET_ROLE_CARDINALITY_INVALID,
                summaries=None,
            )

    ordinals = [s.object_ordinal for s in summaries]
    if ordinals != list(range(len(summaries))):
        return _PrivateDescriptorSetInvariantResult(
            code=_PrivateDescriptorSetInvariantCode.PRIVATE_DESCRIPTOR_SET_ORDINAL_SEQUENCE_INVALID,
            summaries=None,
        )

    targets_seen = set()
    for s in summaries:
        if s.canonical_target_path in targets_seen:
            return _PrivateDescriptorSetInvariantResult(
                code=_PrivateDescriptorSetInvariantCode.PRIVATE_DESCRIPTOR_SET_CANONICAL_TARGET_DUPLICATE,
                summaries=None,
            )
        targets_seen.add(s.canonical_target_path)

    # Exact sidecar-role-to-target-role pairing, derived from the frozen
    # binding table's role naming (each sidecar role's target is its role
    # name with the "_SIDECAR" suffix stripped); every entry here is one of
    # the five roles the frozen table's sidecar_rule field designates as
    # requiring exactly one sidecar in the same unit.
    sidecar_target_role_pairing = {
        PreparedObjectRole.HISTORY_MANIFEST_SIDECAR: PreparedObjectRole.HISTORY_MANIFEST,
        PreparedObjectRole.PUBLICATION_MARKER_SIDECAR: PreparedObjectRole.PUBLICATION_MARKER,
        PreparedObjectRole.CURRENT_GENERATION_MANIFEST_SIDECAR: PreparedObjectRole.CURRENT_GENERATION_MANIFEST,
        PreparedObjectRole.CURRENT_GENERATION_MARKER_SIDECAR: PreparedObjectRole.CURRENT_GENERATION_MARKER,
        PreparedObjectRole.LEGACY_CURRENT_MANIFEST_SIDECAR: PreparedObjectRole.LEGACY_CURRENT_MANIFEST,
    }
    sidecar_required_target_roles = frozenset(sidecar_target_role_pairing.values())

    ordinal_index = {s.object_ordinal: s for s in summaries}
    sidecar_pointer_counts: dict = {}
    for s in summaries:
        if s.is_sidecar:
            if s.sidecar_of_object_ordinal is None:
                return _PrivateDescriptorSetInvariantResult(
                    code=_PrivateDescriptorSetInvariantCode.PRIVATE_DESCRIPTOR_SET_SIDECAR_RELATION_INVALID,
                    summaries=None,
                )
            paired = ordinal_index.get(s.sidecar_of_object_ordinal)
            # Missing target, or a sidecar pointing to another sidecar.
            if paired is None or paired.is_sidecar:
                return _PrivateDescriptorSetInvariantResult(
                    code=_PrivateDescriptorSetInvariantCode.PRIVATE_DESCRIPTOR_SET_SIDECAR_RELATION_INVALID,
                    summaries=None,
                )
            # Exact sidecar-role-to-target-role pairing: a wrong-producer
            # pairing (e.g. HISTORY_MANIFEST_SIDECAR pointing at a
            # PUBLICATION_MARKER descriptor) is invalid even though the
            # target exists and is a non-sidecar descriptor.
            expected_target_role = sidecar_target_role_pairing.get(s.object_role)
            if expected_target_role is None or paired.object_role != expected_target_role:
                return _PrivateDescriptorSetInvariantResult(
                    code=_PrivateDescriptorSetInvariantCode.PRIVATE_DESCRIPTOR_SET_SIDECAR_RELATION_INVALID,
                    summaries=None,
                )
            # Same-unit sibling relationship: every accepted
            # target/sidecar grammar pair (HISTORY_MANIFEST/_SIDECAR,
            # PUBLICATION_MARKER/_SIDECAR, CURRENT_GENERATION_MANIFEST/
            # _SIDECAR, CURRENT_GENERATION_MARKER/_SIDECAR,
            # LEGACY_CURRENT_MANIFEST/_SIDECAR) shares an identical frozen
            # template -- run_id, family_root, and (where present)
            # snapshot_sequence -- differing only in the final filename's
            # extension (.json vs .sha256). Sharing the exact registered
            # producer-unit placeholders is therefore exactly sharing the
            # same parent directory; a cross-run, cross-family,
            # cross-sequence, or otherwise cross-producer pairing changes
            # that directory and is rejected here even though the role
            # pairing above is satisfied.
            sidecar_parent = s.canonical_target_path.rsplit("/", 1)[0]
            target_parent = paired.canonical_target_path.rsplit("/", 1)[0]
            if sidecar_parent != target_parent:
                return _PrivateDescriptorSetInvariantResult(
                    code=_PrivateDescriptorSetInvariantCode.PRIVATE_DESCRIPTOR_SET_SIDECAR_RELATION_INVALID,
                    summaries=None,
                )
            sidecar_pointer_counts[s.sidecar_of_object_ordinal] = (
                sidecar_pointer_counts.get(s.sidecar_of_object_ordinal, 0) + 1
            )
        else:
            if s.sidecar_of_object_ordinal is not None:
                return _PrivateDescriptorSetInvariantResult(
                    code=_PrivateDescriptorSetInvariantCode.PRIVATE_DESCRIPTOR_SET_SIDECAR_RELATION_INVALID,
                    summaries=None,
                )

    # No duplicate sidecar pointer: at most one sidecar may point to any
    # given target ordinal.
    for count in sidecar_pointer_counts.values():
        if count > 1:
            return _PrivateDescriptorSetInvariantResult(
                code=_PrivateDescriptorSetInvariantCode.PRIVATE_DESCRIPTOR_SET_SIDECAR_RELATION_INVALID,
                summaries=None,
            )

    # No target left unpaired: every sidecar-required role's descriptor
    # must have exactly one sidecar pointing to it.
    for s in summaries:
        if s.object_role in sidecar_required_target_roles:
            if sidecar_pointer_counts.get(s.object_ordinal, 0) != 1:
                return _PrivateDescriptorSetInvariantResult(
                    code=_PrivateDescriptorSetInvariantCode.PRIVATE_DESCRIPTOR_SET_SIDECAR_RELATION_INVALID,
                    summaries=None,
                )

    return _PrivateDescriptorSetInvariantResult(
        code=_PrivateDescriptorSetInvariantCode.PRIVATE_DESCRIPTOR_SET_INVARIANTS_VALID,
        summaries=summaries,
    )


def _reject_duplicate_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON object key: " + str(key))
        result[key] = value
    return result


def _reject_non_integer(token: str):
    raise ValueError("non-integer JSON number rejected: " + token)


def _reject_constant(token: str):
    raise ValueError("non-standard JSON constant rejected: " + token)


def _parse_canonical_json_strict(payload_bytes: bytes):
    """Strict UTF-8 decode, duplicate-key rejection, float/constant
    rejection, and canonical lexicographic-key reserialization byte
    equality. Returns the parsed object or raises ValueError."""
    text = payload_bytes.decode("utf-8", "strict")
    value = json.loads(
        text,
        object_pairs_hook=_reject_duplicate_pairs,
        parse_float=_reject_non_integer,
        parse_constant=_reject_constant,
    )
    reserialized = json.dumps(
        value, ensure_ascii=False, separators=(",", ":"), sort_keys=True
    ).encode("utf-8")
    if reserialized != payload_bytes:
        raise ValueError("non-canonical JSON bytes")
    return value


def reconcile_physical_payload(
    expected_file_size_bytes: int,
    expected_file_sha256: str,
    payload_bytes: bytes,
) -> PhysicalPayloadResult:
    """Uniform generic A3: validate expected length/hash syntax, compare
    exact byte length, then recompute complete-file SHA-256. No
    descriptor/unit/binding assurance."""
    valid_length = (
        isinstance(expected_file_size_bytes, int)
        and not isinstance(expected_file_size_bytes, bool)
        and expected_file_size_bytes >= 0
    )
    valid_hash = (
        isinstance(expected_file_sha256, str)
        and len(expected_file_sha256) == 64
        and all(c in "0123456789abcdef" for c in expected_file_sha256)
    )
    if not valid_length or not valid_hash:
        return PhysicalPayloadResult(
            code=I0AResultCode.ERR_PHYSICAL_EXPECTATION_INVALID,
            established_assurances=(),
            observed_size_bytes=None,
            observed_sha256=None,
        )

    observed_size = len(payload_bytes)
    observed_sha256 = hashlib.sha256(payload_bytes).hexdigest()

    if observed_size != expected_file_size_bytes:
        return PhysicalPayloadResult(
            code=I0AResultCode.ERR_PHYSICAL_SIZE_MISMATCH,
            established_assurances=(),
            observed_size_bytes=observed_size,
            observed_sha256=observed_sha256,
        )
    if observed_sha256 != expected_file_sha256:
        return PhysicalPayloadResult(
            code=I0AResultCode.ERR_PHYSICAL_SHA256_MISMATCH,
            established_assurances=(),
            observed_size_bytes=observed_size,
            observed_sha256=observed_sha256,
        )
    return PhysicalPayloadResult(
        code=I0AResultCode.I0A_VALID_A3_EXACT,
        established_assurances=(AssuranceLevel.A3_EXACT_LENGTH_AND_SHA256_RECONCILED,),
        observed_size_bytes=observed_size,
        observed_sha256=observed_sha256,
    )


_SHA256_HEX_CHARS = set("0123456789abcdef")

# SHA-256 hex digest of the empty byte string; used for the empty-relation
# and empty-prefix-coverage digest requirements.
_EMPTY_BYTES_SHA256 = hashlib.sha256(b"").hexdigest()


def _is_sha256_hex(value) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(c in _SHA256_HEX_CHARS for c in value)
    )


def _is_run_id(value) -> bool:
    """Exact ^run_[0-9a-f]{64}$ check using prefix/length/lowercase-hex
    logic only; no regex."""
    prefix = "run_"
    return (
        isinstance(value, str)
        and value.startswith(prefix)
        and _is_sha256_hex(value[len(prefix) :])
    )


def _is_partition_id(value) -> bool:
    """Exact ^part_[0-9a-f]{64}$ check using prefix/length/lowercase-hex
    logic only; no regex."""
    prefix = "part_"
    return (
        isinstance(value, str)
        and value.startswith(prefix)
        and _is_sha256_hex(value[len(prefix) :])
    )


def _find_partition_id_in_path(path) -> Optional[str]:
    """Pure-Python equivalent of a leftmost part_[0-9a-f]{64} search: scans
    for the 'part_' marker and returns the first occurrence whose following
    64 characters are all lowercase hex, or None if absent. No regex."""
    if not isinstance(path, str):
        return None
    marker = "part_"
    start = 0
    while True:
        idx = path.find(marker, start)
        if idx == -1:
            return None
        candidate = path[idx + len(marker) : idx + len(marker) + 64]
        if _is_sha256_hex(candidate):
            return marker + candidate
        start = idx + 1

# Exact unsigned-integer upper bounds for the accepted UINT16/UINT32/UINT64
# field types (json:snapshot_publication_claim_semantic_v23 and
# embedded:snapshot_claim_partition_entry_v23).
_UINT16_MAX = 65535
_UINT32_MAX = 4294967295
_UINT64_MAX = 18446744073709551615

# Capture-family/coverage-state matrix, taken from the accepted claim
# fixtures: the capture family uses CAPTURE_EMPTY_PREFIX_ORIGIN or
# CAPTURE_THROUGH_FENCE_SEQUENCE, and the two analysis families use
# NOT_CAPTURE exclusively.
_AUDIT_FAMILY_COVERAGE_STATES = {
    "capture": frozenset(
        {"CAPTURE_EMPTY_PREFIX_ORIGIN", "CAPTURE_THROUGH_FENCE_SEQUENCE"}
    ),
    "analysis_compatibility": frozenset({"NOT_CAPTURE"}),
    "analysis_strict": frozenset({"NOT_CAPTURE"}),
}


def _is_canonical_uint(value: object, maximum: int) -> bool:
    """True only for a non-negative Python int within the given unsigned
    bound. bool is a subclass of int and is always rejected, so False can
    never satisfy a UINT constant-zero or range requirement."""
    return (
        isinstance(value, int)
        and not isinstance(value, bool)
        and 0 <= value <= maximum
    )
_CLAIM_SEMANTIC_CLOSED_TOP_LEVEL_KEYS = frozenset(
    {
        "schema_version",
        "spec_revision",
        "run_id",
        "audit_family",
        "snapshot_sequence",
        "previous_snapshot_file_sha256",
        "previous_publication_commit_file_sha256",
        "total_row_count",
        "duplicate_key_count",
        "first_key_canonical_json",
        "last_key_canonical_json",
        "partition_entries_semantic_logical_sha256",
        "ordered_relation_logical_sha256",
        "capture_coverage_state",
        "covered_through_fence_sequence",
        "capture_coverage_relation_logical_sha256",
        "partition_entries",
    }
)




def _registry_target_grammar_for_role(object_role, unit_kind):
    """Resolve the frozen target path grammar for a (role, unit_kind) by
    consuming finding4_registry's authoritative frozen binding table.
    prepared_evidence keeps no independent role->grammar authority; grammar
    ownership stays in finding4_registry per Revision 08. Returns the
    unique target_grammar_id, or None if the pair is absent (no reachable
    binding). If the frozen table ever bound one (role, unit_kind) to more
    than one grammar the resolution is ambiguous and returns None rather
    than guessing."""
    from .finding4_registry import _FROZEN_PRODUCTION_BINDINGS

    grammars = {
        b.target_grammar_id
        for b in _FROZEN_PRODUCTION_BINDINGS
        if b.role == object_role and b.unit_kind == unit_kind
    }
    if len(grammars) != 1:
        return None
    return next(iter(grammars))


def _parse_prepared_object_source_identity(path):
    """Deterministically recovers the placeholder values embedded in a
    durable_source_path that has ALREADY been validated against
    FrozenPathGrammarId.PREPARED_OBJECT_BIN by
    finding4_registry.validate_normalized_relative_path. This is pure
    string decomposition of an already-valid path -- it introduces no
    second grammar or lexical-path authority and asserts no filesystem
    fact.

    Frozen template:
      artifacts/local_curl_per_side/runs/<run_id>/prepared_evidence/
      <unit_kind>/<prepared_unit_id>/objects/<object_ordinal_10d>.bin

    Returns (run_id, unit_kind, prepared_unit_directory, object_ordinal),
    or None if the path does not decompose (which cannot occur for a path
    the registry validator has accepted)."""
    if not isinstance(path, str):
        return None
    parts = path.split("/")
    # 0:artifacts 1:local_curl_per_side 2:runs 3:<run_id> 4:prepared_evidence
    # 5:<unit_kind> 6:<prepared_unit_id> 7:objects 8:<ordinal>.bin
    if len(parts) != 9:
        return None
    if parts[4] != "prepared_evidence" or parts[7] != "objects":
        return None
    run_id = parts[3]
    unit_kind_value = parts[5]
    prepared_unit_directory = "/".join(parts[:7])
    ordinal_token = parts[8]
    if not ordinal_token.endswith(".bin"):
        return None
    ordinal_digits = ordinal_token[: -len(".bin")]
    if len(ordinal_digits) != 10 or not ordinal_digits.isdigit():
        return None
    return (run_id, unit_kind_value, prepared_unit_directory, int(ordinal_digits))


def _resolve_frozen_row(object_role, unit_kind, publication_mode, content_schema_id):
    """Resolve the complete compatible frozen binding row for the exact
    (role, unit_kind, publication_mode, content_schema_id) combination by
    consuming finding4_registry's authoritative frozen binding table.
    Compatibility is never derived from role alone: every field of the row
    -- publication mode and content_schema_id, not just role and unit_kind
    -- must match a single accepted row before it is used as authority for
    target grammar or logical-hash nullability. Returns the matching
    SchemaBinding, or None if no frozen row admits this exact combination."""
    from .finding4_registry import _FROZEN_PRODUCTION_BINDINGS

    matches = [
        b
        for b in _FROZEN_PRODUCTION_BINDINGS
        if b.role == object_role
        and b.unit_kind == unit_kind
        and b.publication_mode == publication_mode
        and b.content_schema_id == content_schema_id
    ]
    if len(matches) != 1:
        return None
    return matches[0]


def validate_prepared_object_descriptor(
    descriptor: PreparedObjectDescriptor, unit_context: UnitContext
) -> ValidationResult:
    """Validates exactly one full descriptor. It does not evaluate
    partition cardinality, ordinal completeness, target uniqueness, or
    sidecar graph completeness."""
    if unit_context.unit_kind != PreparedUnitKind.SNAPSHOT_PUBLICATION:
        return ValidationResult(
            code=I0AResultCode.STOP_UNIT_KIND_NOT_ACCEPTED_I0A,
            established_assurances=(),
        )

    closed_fields_ok = (
        _is_canonical_uint(descriptor.object_ordinal, _UINT32_MAX)
        and isinstance(descriptor.object_role, PreparedObjectRole)
        and isinstance(descriptor.content_schema_id, str)
        and isinstance(descriptor.publication_mode, PublicationMode)
        and isinstance(descriptor.durable_source_path, str)
        and isinstance(descriptor.canonical_target_path, str)
        and _is_canonical_uint(descriptor.file_size_bytes, _UINT64_MAX)
        and _is_sha256_hex(descriptor.file_sha256)
        and (descriptor.logical_sha256 is None or _is_sha256_hex(descriptor.logical_sha256))
        and (
            descriptor.sidecar_of_object_ordinal is None
            or _is_canonical_uint(descriptor.sidecar_of_object_ordinal, _UINT32_MAX)
        )
    )
    if not closed_fields_ok:
        return ValidationResult(
            code=I0AResultCode.ERR_DESCRIPTOR_CLOSED_FIELD_INVALID,
            established_assurances=(),
        )

    # Every ERR_ROLE_DISPOSITION_INVALID predicate -- frozen-row
    # compatibility and sidecar-pointer presence/nullness -- is evaluated
    # before any target or source path lexical/grammar validation.
    frozen_row = _resolve_frozen_row(
        descriptor.object_role,
        unit_context.unit_kind,
        descriptor.publication_mode,
        descriptor.content_schema_id,
    )
    if frozen_row is None:
        return ValidationResult(
            code=I0AResultCode.ERR_ROLE_DISPOSITION_INVALID,
            established_assurances=(),
        )

    is_sidecar_role = descriptor.object_role.value.endswith("_SIDECAR")
    if is_sidecar_role:
        if descriptor.sidecar_of_object_ordinal is None:
            return ValidationResult(
                code=I0AResultCode.ERR_ROLE_DISPOSITION_INVALID,
                established_assurances=(),
            )
    else:
        if descriptor.sidecar_of_object_ordinal is not None:
            return ValidationResult(
                code=I0AResultCode.ERR_ROLE_DISPOSITION_INVALID,
                established_assurances=(),
            )

    # Path validation across BOTH path fields. Each field is evaluated far
    # enough to determine every applicable path fault class BEFORE either
    # class is returned, then the classes are returned in the accepted
    # precedence: ERR_PATH_LEXICAL_INVALID (8) strictly outranks
    # ERR_PATH_GRAMMAR_MISMATCH (9). A canonical-target grammar fault
    # combined with a durable-source lexical fault therefore returns
    # ERR_PATH_LEXICAL_INVALID, not the grammar fault discovered first.
    # Role disposition (7) was already ruled out above and still outranks
    # both path classes.
    #
    # finding4_registry.validate_normalized_relative_path is the ONLY
    # lexical and grammar authority consulted; this module reproduces
    # neither. The registry validator returns ERR_PATH_LEXICAL_INVALID for
    # a lexical fault and ERR_PATH_GRAMMAR_MISMATCH for a grammar fault,
    # so each field's class is read directly from its result.
    path_fault_classes = []

    target_path_result = validate_normalized_relative_path(
        descriptor.canonical_target_path, frozen_row.target_grammar_id
    )
    if target_path_result.code != I0AResultCode.I0A_VALID_A1_PATH:
        path_fault_classes.append(target_path_result.code)

    if descriptor.publication_mode == PublicationMode.REUSE_IMMUTABLE_SOURCE:
        # Reuse source: validated against the SAME resolved target grammar
        # (the durable source IS the immutable target artifact), then
        # required to be byte-for-byte equal to the canonical target. The
        # equality mismatch is a grammar-class fault.
        source_path_result = validate_normalized_relative_path(
            descriptor.durable_source_path, frozen_row.target_grammar_id
        )
        if source_path_result.code != I0AResultCode.I0A_VALID_A1_PATH:
            path_fault_classes.append(source_path_result.code)
        elif descriptor.durable_source_path != descriptor.canonical_target_path:
            path_fault_classes.append(I0AResultCode.ERR_PATH_GRAMMAR_MISMATCH)
    else:
        # Non-reuse source: the exact frozen prepared-object path grammar.
        source_path_result = validate_normalized_relative_path(
            descriptor.durable_source_path, FrozenPathGrammarId.PREPARED_OBJECT_BIN
        )
        if source_path_result.code != I0AResultCode.I0A_VALID_A1_PATH:
            path_fault_classes.append(source_path_result.code)
        else:
            # Ordinal-placeholder agreement with this descriptor's own
            # object_ordinal is a grammar-class fault of the source path
            # itself (the <object_ordinal_10d> placeholder is part of the
            # frozen template), not a cross-input mismatch.
            expected_ordinal_suffix = f"objects/{descriptor.object_ordinal:010d}.bin"
            if not descriptor.durable_source_path.endswith(expected_ordinal_suffix):
                path_fault_classes.append(I0AResultCode.ERR_PATH_GRAMMAR_MISMATCH)

    for path_fault_class in (
        I0AResultCode.ERR_PATH_LEXICAL_INVALID,
        I0AResultCode.ERR_PATH_GRAMMAR_MISMATCH,
    ):
        if path_fault_class in path_fault_classes:
            return ValidationResult(
                code=path_fault_class,
                established_assurances=(),
            )

    # Role-local logical-hash nullability from the resolved row itself, not
    # a role-based exemption list: every reachable non-sidecar role
    # (including PARTITION_PAYLOAD and the three index roles) requires
    # non-null logical_sha256; every sidecar role requires null.
    requires_null_logical_hash = frozen_row.logical_sha256_nullability == "NULL_REQUIRED"
    if requires_null_logical_hash:
        if descriptor.logical_sha256 is not None:
            return ValidationResult(
                code=I0AResultCode.ERR_LOGICAL_HASH_NULLABILITY_INVALID,
                established_assurances=(),
            )
    else:
        if descriptor.logical_sha256 is None:
            return ValidationResult(
                code=I0AResultCode.ERR_LOGICAL_HASH_NULLABILITY_INVALID,
                established_assurances=(),
            )

    return ValidationResult(
        code=I0AResultCode.I0A_VALID_A2_SINGLE,
        established_assurances=(
            AssuranceLevel.A1_LEXICAL_PATH_SHAPE,
            AssuranceLevel.A2_SINGLE_DESCRIPTOR_CLOSED_FIELDS,
        ),
    )


_REACHABLE_SNAPSHOT_ROLE_COUNTS_FIXED = {
    PreparedObjectRole.HISTORY_MANIFEST: 1,
    PreparedObjectRole.HISTORY_MANIFEST_SIDECAR: 1,
    PreparedObjectRole.HISTORY_INDEX: 1,
    PreparedObjectRole.PUBLICATION_MARKER: 1,
    PreparedObjectRole.PUBLICATION_MARKER_SIDECAR: 1,
    PreparedObjectRole.CURRENT_GENERATION_MANIFEST: 1,
    PreparedObjectRole.CURRENT_GENERATION_MANIFEST_SIDECAR: 1,
    PreparedObjectRole.CURRENT_GENERATION_INDEX: 1,
    PreparedObjectRole.CURRENT_GENERATION_MARKER: 1,
    PreparedObjectRole.CURRENT_GENERATION_MARKER_SIDECAR: 1,
    PreparedObjectRole.LEGACY_CURRENT_MANIFEST: 1,
    PreparedObjectRole.LEGACY_CURRENT_MANIFEST_SIDECAR: 1,
    PreparedObjectRole.LEGACY_CURRENT_INDEX: 1,
}


# Sixteen-cell top-level scalar projection (json:snapshot_publication_
# claim_semantic_v23 minus the partition_entries array), matching
# claim_hashes.compute_snapshot_claim_semantic_sha256's accepted field/tag
# contract exactly. Used only to route the claim's scalar cells through the
# accepted public canonical constructor for NFC/tag/type/order validation;
# no private cross-module symbol is imported for this.
_SNAPSHOT_CLAIM_SEMANTIC_PROJECTION_FIELDS = (
    TypedFieldSpec(name="schema_version", type_tag=TypedCellTag.STRING),
    TypedFieldSpec(name="spec_revision", type_tag=TypedCellTag.UINT),
    TypedFieldSpec(name="run_id", type_tag=TypedCellTag.STRING),
    TypedFieldSpec(name="audit_family", type_tag=TypedCellTag.STRING),
    TypedFieldSpec(name="snapshot_sequence", type_tag=TypedCellTag.UINT),
    TypedFieldSpec(name="previous_snapshot_file_sha256", type_tag=TypedCellTag.SHA256),
    TypedFieldSpec(
        name="previous_publication_commit_file_sha256", type_tag=TypedCellTag.SHA256
    ),
    TypedFieldSpec(name="total_row_count", type_tag=TypedCellTag.UINT),
    TypedFieldSpec(name="duplicate_key_count", type_tag=TypedCellTag.UINT),
    TypedFieldSpec(name="first_key_canonical_json", type_tag=TypedCellTag.STRING),
    TypedFieldSpec(name="last_key_canonical_json", type_tag=TypedCellTag.STRING),
    TypedFieldSpec(
        name="partition_entries_semantic_logical_sha256", type_tag=TypedCellTag.SHA256
    ),
    TypedFieldSpec(name="ordered_relation_logical_sha256", type_tag=TypedCellTag.SHA256),
    TypedFieldSpec(name="capture_coverage_state", type_tag=TypedCellTag.STRING),
    TypedFieldSpec(name="covered_through_fence_sequence", type_tag=TypedCellTag.UINT),
    TypedFieldSpec(
        name="capture_coverage_relation_logical_sha256", type_tag=TypedCellTag.SHA256
    ),
)
_SNAPSHOT_CLAIM_SEMANTIC_PROJECTION_NULLABLE_FIELDS = frozenset(
    {
        "previous_snapshot_file_sha256",
        "previous_publication_commit_file_sha256",
        "first_key_canonical_json",
        "last_key_canonical_json",
        "covered_through_fence_sequence",
        "capture_coverage_relation_logical_sha256",
    }
)


def _validate_claim_projection_via_accepted_constructor(claim):
    """Builds the accepted sixteen-cell scalar projection and validates it
    through the already-permitted public compute_snapshot_claim_semantic_sha256
    constructor (canonical_typed_row_bytes under the hood), which enforces
    exact field name/order, tag/type matching, and NFC normalization for
    every STRING-tagged cell -- including schema_version, run_id,
    audit_family, first_key_canonical_json, last_key_canonical_json, and
    capture_coverage_state. Internal A0 constructor failures (tag/type/NFC/
    order faults) are mapped into ERR_SELECTED_SCHEMA_INVALID; no A0
    constructor result escapes this function."""
    cells = []
    for field in _SNAPSHOT_CLAIM_SEMANTIC_PROJECTION_FIELDS:
        raw_value = claim.get(field.name)
        is_null = (
            raw_value is None
            and field.name in _SNAPSHOT_CLAIM_SEMANTIC_PROJECTION_NULLABLE_FIELDS
        )
        cells.append(
            TypedCell(
                name=field.name,
                type_tag=TypedCellTag.NULL if is_null else field.type_tag,
                value=raw_value,
            )
        )
    digest_result = compute_snapshot_claim_semantic_sha256(cells)
    if digest_result.code != I0AResultCode.I0A_DIGEST_CONSTRUCTED_A0:
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID
    return None


def _validate_snapshot_claim_semantic_complete(claim, unit_kind):
    """Fully validates a parsed snapshot claim-semantic object against
    json:snapshot_publication_claim_semantic_v23 and recomputes its
    partition-entry relation, returning an in-domain I0AResultCode on the
    first fault or None when fully valid.

    Faults are ordered to match validate_prepared_descriptor_set.
    ordered_error_precedence: EVERY selected-schema condition (closed
    membership, field type/constant/bound, NFC, nested partition-entry
    membership/type/format, partition_id/path uniqueness, total_row_count
    reconciliation, and top-level first/last-key nullability --
    ERR_SELECTED_SCHEMA_INVALID, precedence 2) is evaluated and ruled out
    before predecessor nullability (ERR_PREDECESSOR_RULE_INVALID, 3),
    coverage-state consistency (ERR_COVERAGE_STATE_INVALID, 4), and the
    recomputed logical-hash comparisons (ERR_LOGICAL_SHA256_MISMATCH, 5). A
    nested partition-entry ordinal-sequence mismatch (public precedence 11,
    far below all of the above) is never returned immediately: it is
    recorded and validation continues through every remaining entry and
    every higher-priority condition, and is returned only at the very end,
    after 2/3/4/5 have all been ruled out. No forged relation hash, invalid
    coverage state, malformed nested entry, non-NFC string, or invalid
    constant/type/bound can pass. The recomputation never trusts the stored
    digest (structural_schema_validation_disposition.no_digest_trust)."""
    if not isinstance(claim, dict):
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID
    if set(claim.keys()) != _CLAIM_SEMANTIC_CLOSED_TOP_LEVEL_KEYS:
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID

    # Exact field types and constants (json:snapshot_publication_claim_semantic_v23).
    if claim.get("schema_version") != "local_curl_snapshot_publication_claim_semantic.v23":
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID
    # spec_revision is UINT16 const 23; duplicate_key_count is UINT64 const 0.
    # Both are range- and bool-checked before the constant comparison so that
    # False can never satisfy the constant-zero requirement.
    if not _is_canonical_uint(claim.get("spec_revision"), _UINT16_MAX):
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID
    if claim.get("spec_revision") != 23:
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID
    if not _is_canonical_uint(claim.get("duplicate_key_count"), _UINT64_MAX):
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID
    if claim.get("duplicate_key_count") != 0:
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID
    audit_family = claim.get("audit_family")
    if audit_family not in _AUDIT_FAMILY_COVERAGE_STATES:
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID
    run_id = claim.get("run_id")
    if not _is_run_id(run_id):
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID
    for uint64_field in ("snapshot_sequence", "total_row_count"):
        if not _is_canonical_uint(claim.get(uint64_field), _UINT64_MAX):
            return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID
    for sha_field in (
        "partition_entries_semantic_logical_sha256",
        "ordered_relation_logical_sha256",
    ):
        v = claim.get(sha_field)
        if not _is_sha256_hex(v):
            return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID
    for nullable_sha_field in (
        "previous_snapshot_file_sha256",
        "previous_publication_commit_file_sha256",
        "capture_coverage_relation_logical_sha256",
    ):
        v = claim.get(nullable_sha_field)
        if v is not None and not _is_sha256_hex(v):
            return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID
    for nullable_str_field in ("first_key_canonical_json", "last_key_canonical_json"):
        v = claim.get(nullable_str_field)
        if v is not None and not isinstance(v, str):
            return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID

    # NFC (and redundant tag/type/order) validation of the sixteen scalar
    # cells through the accepted public constructor.
    projection_fault = _validate_claim_projection_via_accepted_constructor(claim)
    if projection_fault is not None:
        return projection_fault

    # Nested partition entries: exact seven-cell membership/types/NFC,
    # deferring only an ordinal-VALUE mismatch (correct type, wrong
    # sequence position) so every remaining entry and every aggregate
    # selected-schema condition is still evaluated.
    partition_entries = claim.get("partition_entries")
    if not isinstance(partition_entries, list):
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID
    deferred_ordinal_fault = None
    entry_row_bytes = []
    partition_grammar_id = _registry_target_grammar_for_role(
        PreparedObjectRole.PARTITION_PAYLOAD, unit_kind
    )
    for i, entry in enumerate(partition_entries):
        entry_fault, ordinal_mismatch, row_bytes = _validate_partition_entry_and_project(
            entry, i, partition_grammar_id
        )
        if entry_fault is not None:
            return entry_fault
        if ordinal_mismatch:
            deferred_ordinal_fault = I0AResultCode.ERR_ORDINAL_SEQUENCE_INVALID
        entry_row_bytes.append(row_bytes)

    # partition_id and partition_path are each unique across the entries.
    partition_ids = [e.get("partition_id") for e in partition_entries]
    if len(set(partition_ids)) != len(partition_ids):
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID
    partition_paths = [e.get("partition_path") for e in partition_entries]
    if len(set(partition_paths)) != len(partition_paths):
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID

    # total_row_count reconciles with the sum of the partition-entry row counts.
    if claim.get("total_row_count") != sum(
        e.get("row_count") for e in partition_entries
    ):
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID

    # Top-level first/last key: "STRING nullable iff empty" -- both are null
    # exactly when the claim carries no rows, and both non-null otherwise.
    claim_is_empty = claim.get("total_row_count") == 0
    for top_level_key_field in (
        "first_key_canonical_json",
        "last_key_canonical_json",
    ):
        if claim_is_empty != (claim.get(top_level_key_field) is None):
            return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID

    # covered_through_fence_sequence's own type/width -- null or a non-bool
    # UINT64 -- is validated here, in selected-schema (2), unconditionally
    # on coverage_state. This is separate from the state-conditional
    # nullability rule below (coverage, precedence 4): an out-of-range or
    # wrong-type value is a selected-schema fault regardless of which
    # coverage state the claim declares.
    covered_through_raw = claim.get("covered_through_fence_sequence")
    if covered_through_raw is not None and not _is_canonical_uint(
        covered_through_raw, _UINT64_MAX
    ):
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID

    # Every selected-schema condition (2) is now ruled out. Predecessor/
    # origin rules (3): snapshot_sequence 0 is the origin. BOTH
    # previous_snapshot_file_sha256 and previous_publication_commit_file_sha256
    # are declared "SHA256 nullable, null iff origin", so each is null
    # exactly at the origin and non-null exactly off-origin.
    sequence_value = claim.get("snapshot_sequence")
    is_origin = sequence_value == 0
    for origin_nullable_field in (
        "previous_snapshot_file_sha256",
        "previous_publication_commit_file_sha256",
    ):
        if is_origin != (claim.get(origin_nullable_field) is None):
            return I0AResultCode.ERR_PREDECESSOR_RULE_INVALID

    # Coverage-state rules (4): the state must be one the claim's
    # audit_family admits; covered_through_fence_sequence is a UINT64
    # non-null iff CAPTURE_THROUGH_FENCE_SEQUENCE; and
    # capture_coverage_relation_logical_sha256 is non-null and equal to
    # ordered_relation_logical_sha256 for the capture family, null for the
    # non-capture (NOT_CAPTURE) families. Empty-prefix semantics: capture +
    # CAPTURE_EMPTY_PREFIX_ORIGIN additionally requires an empty partition
    # relation (total_row_count and top-level key nullability are already
    # enforced generically above whenever partition_entries is empty).
    coverage_state = claim.get("capture_coverage_state")
    if coverage_state not in _AUDIT_FAMILY_COVERAGE_STATES[audit_family]:
        return I0AResultCode.ERR_COVERAGE_STATE_INVALID
    covered_through = claim.get("covered_through_fence_sequence")
    if coverage_state == "CAPTURE_THROUGH_FENCE_SEQUENCE":
        if not _is_canonical_uint(covered_through, _UINT64_MAX):
            return I0AResultCode.ERR_COVERAGE_STATE_INVALID
    elif covered_through is not None:
        return I0AResultCode.ERR_COVERAGE_STATE_INVALID
    if coverage_state == "CAPTURE_EMPTY_PREFIX_ORIGIN" and partition_entries:
        return I0AResultCode.ERR_COVERAGE_STATE_INVALID
    coverage_relation = claim.get("capture_coverage_relation_logical_sha256")
    if coverage_state == "NOT_CAPTURE":
        if coverage_relation is not None:
            return I0AResultCode.ERR_COVERAGE_STATE_INVALID
    else:
        if coverage_relation is None or coverage_relation != claim.get(
            "ordered_relation_logical_sha256"
        ):
            return I0AResultCode.ERR_COVERAGE_STATE_INVALID

    # Logical-hash recomputation (5): recompute and compare the seven-cell
    # partition-entry relation using each entry's own already-constructed
    # canonical row bytes (never trusting the stored digest), then, for an
    # empty partition relation, require ordered_relation_logical_sha256 to
    # equal the empty-bytes digest too (the only case in which this
    # out-of-I0A-scope aggregate is independently knowable).
    rows_bytes = b"\n".join(entry_row_bytes) if entry_row_bytes else b""
    if hashlib.sha256(rows_bytes).hexdigest() != claim.get(
        "partition_entries_semantic_logical_sha256"
    ):
        return I0AResultCode.ERR_LOGICAL_SHA256_MISMATCH
    if not partition_entries and claim.get(
        "ordered_relation_logical_sha256"
    ) != _EMPTY_BYTES_SHA256:
        return I0AResultCode.ERR_LOGICAL_SHA256_MISMATCH

    # Precedence 11: the deferred nested partition-entry ordinal fault, now
    # that every higher-priority claim-level condition has passed.
    if deferred_ordinal_fault is not None:
        return deferred_ordinal_fault
    return None


_PARTITION_ENTRY_ROW_FIELD_TAGS = (
    ("partition_ordinal", "UINT"),
    ("partition_id", "STRING"),
    ("partition_path", "STRING"),
    ("partition_logical_sha256", "SHA256"),
    ("row_count", "UINT"),
    ("first_key_canonical_json", "STRING"),
    ("last_key_canonical_json", "STRING"),
)
_PARTITION_ENTRY_CLOSED_KEYS = frozenset(
    name for name, _tag in _PARTITION_ENTRY_ROW_FIELD_TAGS
)


_PARTITION_ENTRY_PROJECTION_FIELDS = tuple(
    TypedFieldSpec(name=name, type_tag=TypedCellTag[tag])
    for name, tag in _PARTITION_ENTRY_ROW_FIELD_TAGS
)
_PARTITION_ENTRY_PROJECTION_NULLABLE_FIELDS = frozenset(
    {"first_key_canonical_json", "last_key_canonical_json"}
)


def _validate_partition_entry_and_project(entry, expected_ordinal, partition_grammar_id):
    """Validates one embedded:snapshot_claim_partition_entry_v23 object
    against every non-ordinal-sequencing condition: exact seven-field
    closed membership, domain-specific partition_id/path format,
    partition_path compatibility with the frozen PARTITION_PAYLOAD target
    grammar (validated here, independent of and before any matching
    descriptor is processed), UINT32/UINT64 bounds (bool always rejected),
    row_count-conditional first/last-key nullability, and -- via the
    accepted public canonical_typed_row_bytes constructor -- per-cell
    tag/type/NFC/SHA256-format validation, which also yields the exact
    canonical row bytes for the seven-cell relation hash.

    Returns (fault_code, is_ordinal_mismatch, row_bytes). A wrong ordinal
    VALUE (correct type, wrong sequence position) is reported as
    (None, True, row_bytes) so the caller can defer it behind every
    higher-priority selected-schema condition, including conditions on
    later entries and the claim's aggregate fields. Any other fault
    returns immediately as (fault_code, False, None)."""
    if not isinstance(entry, dict) or set(entry.keys()) != _PARTITION_ENTRY_CLOSED_KEYS:
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID, False, None

    ordinal = entry.get("partition_ordinal")
    if not _is_canonical_uint(ordinal, _UINT32_MAX):
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID, False, None
    partition_id = entry.get("partition_id")
    if not _is_partition_id(partition_id):
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID, False, None
    partition_path = entry.get("partition_path")
    if not isinstance(partition_path, str) or not partition_path:
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID, False, None
    # Claim partition_path is fully validated against the frozen
    # PARTITION_PAYLOAD target grammar here, as part of claim
    # selected-schema validation -- an incompatible path never relies on
    # the later matching descriptor to establish claim schema validity,
    # and this claim-level fault outranks any descriptor path fault
    # (precedence 2 vs. 8/9).
    if partition_grammar_id is None:
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID, False, None
    path_result = validate_normalized_relative_path(partition_path, partition_grammar_id)
    if path_result.code != I0AResultCode.I0A_VALID_A1_PATH:
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID, False, None
    partition_logical = entry.get("partition_logical_sha256")
    if not _is_sha256_hex(partition_logical):
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID, False, None
    row_count = entry.get("row_count")
    if not _is_canonical_uint(row_count, _UINT64_MAX):
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID, False, None
    first_key = entry.get("first_key_canonical_json")
    last_key = entry.get("last_key_canonical_json")
    keys_should_be_null = row_count == 0
    for key_value in (first_key, last_key):
        if keys_should_be_null and key_value is not None:
            return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID, False, None
        if not keys_should_be_null and (
            key_value is None or not isinstance(key_value, str)
        ):
            return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID, False, None

    cells = []
    for field in _PARTITION_ENTRY_PROJECTION_FIELDS:
        raw_value = entry.get(field.name)
        is_null = (
            raw_value is None
            and field.name in _PARTITION_ENTRY_PROJECTION_NULLABLE_FIELDS
        )
        cells.append(
            TypedCell(
                name=field.name,
                type_tag=TypedCellTag.NULL if is_null else field.type_tag,
                value=raw_value,
            )
        )
    expected_fields = tuple(
        TypedFieldSpec(
            name=f.name,
            type_tag=(
                cells[i].type_tag
                if cells[i].type_tag is TypedCellTag.NULL
                else f.type_tag
            ),
        )
        for i, f in enumerate(_PARTITION_ENTRY_PROJECTION_FIELDS)
    )
    row_result = canonical_typed_row_bytes(cells, expected_fields)
    if row_result.code != I0AResultCode.I0A_BYTES_CONSTRUCTED_A0:
        return I0AResultCode.ERR_SELECTED_SCHEMA_INVALID, False, None

    if ordinal != expected_ordinal:
        return None, True, row_result.value
    return None, False, row_result.value


def validate_prepared_descriptor_set(value: DescriptorSetInput) -> ValidationResult:
    """For SNAPSHOT_PUBLICATION first validates exact snapshot claim-semantic
    bytes, derives partition cardinality from partition_entries, and binds
    each PARTITION_PAYLOAD descriptor to the exact same-ordinal claim entry
    path, partition identity, and logical hash; then validates every
    remaining descriptor and exact full-set invariants."""
    if value.unit_context.unit_kind != PreparedUnitKind.SNAPSHOT_PUBLICATION:
        return ValidationResult(
            code=I0AResultCode.STOP_UNIT_KIND_NOT_ACCEPTED_I0A,
            established_assurances=(),
        )

    if value.snapshot_claim_semantic_bytes is None:
        return ValidationResult(
            code=I0AResultCode.ERR_CANONICAL_JSON_INVALID,
            established_assurances=(),
        )
    try:
        claim = _parse_canonical_json_strict(value.snapshot_claim_semantic_bytes)
    except (ValueError, UnicodeDecodeError):
        return ValidationResult(
            code=I0AResultCode.ERR_CANONICAL_JSON_INVALID,
            established_assurances=(),
        )
    # Complete snapshot claim-semantic validation and hash-binding BEFORE the
    # claim is used as partition-cardinality or descriptor-binding authority
    # (rule: "first validates exact snapshot claim-semantic bytes ... before").
    # Enforces closed membership, exact field types/constants, predecessor
    # nullability, coverage-state nullability, exact seven-cell nested
    # partition-entry membership and ascending ordinal, and recomputes and
    # compares partition_entries_semantic_logical_sha256. A forged relation
    # hash, invalid coverage state, malformed nested entry, or invalid
    # constant/type cannot reach I0A_VALID_A2_SET. All returned codes are in
    # the function's accepted closed domain; ERR_CLAIM_SEMANTIC_SCHEMA_MISMATCH
    # is never emitted here.
    claim_fault = _validate_snapshot_claim_semantic_complete(
        claim, value.unit_context.unit_kind
    )
    # A nested partition-entry ordinal fault carries the public code
    # ERR_ORDINAL_SEQUENCE_INVALID, which sits at precedence 11 -- below every
    # descriptor fault (6..10). It is therefore computed here but DEFERRED so
    # that a higher-priority descriptor fault is never displaced by it. All
    # other claim faults (selected-schema 2, predecessor 3, coverage 4,
    # logical-hash 5) outrank the descriptors and return immediately.
    deferred_claim_ordinal_fault = None
    if claim_fault is I0AResultCode.ERR_ORDINAL_SEQUENCE_INVALID:
        deferred_claim_ordinal_fault = claim_fault
    elif claim_fault is not None:
        return ValidationResult(code=claim_fault, established_assurances=())
    partition_entries = claim["partition_entries"]

    # Descriptor faults (precedence 6..10). object_ordinal validity (type,
    # bool exclusion, non-negative) is itself part of each descriptor's own
    # closed-field check (ERR_DESCRIPTOR_CLOSED_FIELD_INVALID), so ordinals
    # must never be compared or sorted before that check has run: sorting a
    # mixed-type ordinal set would raise TypeError. A first pass therefore
    # validates every descriptor in the exact order supplied (no sorting,
    # no ordinal comparison), so a mixed-type ordinal input is caught and
    # returns ERR_DESCRIPTOR_CLOSED_FIELD_INVALID without ever comparing
    # ordinals or raising.
    for d in value.descriptors:
        first_pass_result = validate_prepared_object_descriptor(d, value.unit_context)
        if first_pass_result.code == I0AResultCode.ERR_DESCRIPTOR_CLOSED_FIELD_INVALID:
            return first_pass_result

    # Every descriptor's object_ordinal is now known to be a valid,
    # comparable canonical UINT, so sorting/ranking by ordinal is safe.
    #
    # Requirement: select the first satisfied PUBLIC FAULT CLASS across the
    # complete descriptor tuple (not the first arbitrary fault encountered
    # by ordinal). Each descriptor's own first-applicable fault is computed
    # in the exact order supplied (no sort needed for this collection
    # step, since per-descriptor validation does not compare ordinals
    # across descriptors). Then, for each class in the accepted
    # ordered_error_precedence, if ANY descriptor exhibits it, the lowest
    # canonical ordinal AMONG DESCRIPTORS SHARING THAT CLASS is selected
    # and its code returned -- never the fault of whichever descriptor
    # happens to come first in ordinal order if a higher-precedence class
    # is exhibited by a later-ordinal descriptor.
    per_descriptor_results = [
        (d, validate_prepared_object_descriptor(d, value.unit_context))
        for d in value.descriptors
    ]
    for fault_class in (
        I0AResultCode.ERR_ROLE_DISPOSITION_INVALID,
        I0AResultCode.ERR_PATH_LEXICAL_INVALID,
        I0AResultCode.ERR_PATH_GRAMMAR_MISMATCH,
        I0AResultCode.ERR_LOGICAL_HASH_NULLABILITY_INVALID,
    ):
        matching_descriptors = [
            d for d, r in per_descriptor_results if r.code == fault_class
        ]
        if matching_descriptors:
            # ValidationResult carries only a code, so identifying the
            # lowest-ordinal descriptor does not change the code returned
            # for this class; it is still computed to honor the selection
            # rule explicitly rather than relying on discovery order.
            lowest_ordinal_descriptor = min(
                matching_descriptors, key=lambda x: x.object_ordinal
            )
            del lowest_ordinal_descriptor
            return ValidationResult(code=fault_class, established_assurances=())

    # With every descriptor fault ruled out, the deferred nested partition-entry
    # ordinal fault is now the highest remaining priority (11).
    if deferred_claim_ordinal_fault is not None:
        return ValidationResult(
            code=deferred_claim_ordinal_fault, established_assurances=()
        )

    # Descriptor ordinal-sequence validity is calculated independently of
    # the role-first private reducer, whose accepted internal order checks
    # role cardinality before ordinal sequence. A simultaneous descriptor
    # ordinal-sequence fault and fixed-role-cardinality fault must return
    # ERR_ORDINAL_SEQUENCE_INVALID, so this independent check is evaluated
    # -- and returned on failure -- before the reducer's role-cardinality
    # result is ever consulted. Every ordinal is already known comparable
    # (the first pass above ruled out any closed-field/type fault), so this
    # comparison is safe.
    #
    # This checks the ACTUAL SUPPLIED ORDER of value.descriptors against
    # 0..N-1 -- no sorting. A tuple ordered 1,0,2,... is a complete set of
    # ordinals but the WRONG order, and must fail here even though sorting
    # it would produce range(N); sorting before this comparison would mask
    # exactly that defect.
    descriptor_ordinals = [d.object_ordinal for d in value.descriptors]
    if descriptor_ordinals != list(range(len(value.descriptors))):
        return ValidationResult(
            code=I0AResultCode.ERR_ORDINAL_SEQUENCE_INVALID,
            established_assurances=(),
        )

    # value.descriptors is now confirmed to already be in canonical ordinal
    # order (0..N-1 in supplied position), so it is used directly for
    # summaries and subsequent processing; no further sort is needed here.
    # Full-set invariants. The private reducer keeps its accepted role-first
    # internal order, so its result is mapped and then re-ordered here into the
    # separate public precedence: fixed-role and variable PARTITION_PAYLOAD
    # cardinality (12) outrank canonical-target duplicate (13) and sidecar
    # relation (14); and all of them outrank same-ordinal cross-member
    # mismatch (15). Ordinal sequence (11) was already independently ruled
    # out above, so the reducer's own ordinal branch is unreachable here and
    # kept only as defensive total-mapping, never observed.
    expected_role_counts = dict(_REACHABLE_SNAPSHOT_ROLE_COUNTS_FIXED)
    summaries = tuple(
        _DescriptorSetInvariantSummary(
            object_ordinal=d.object_ordinal,
            object_role=d.object_role,
            canonical_target_path=d.canonical_target_path,
            is_sidecar=d.object_role.value.endswith("_SIDECAR"),
            sidecar_of_object_ordinal=d.sidecar_of_object_ordinal,
        )
        for d in value.descriptors
    )
    invariant_input = _DescriptorSetInvariantInput(
        summaries=summaries, expected_role_counts=expected_role_counts
    )
    invariant_result = _validate_descriptor_set_invariants(invariant_input)
    private_to_public = {
        _PrivateDescriptorSetInvariantCode.PRIVATE_DESCRIPTOR_SET_ROLE_CARDINALITY_INVALID: I0AResultCode.ERR_ROLE_CARDINALITY_INVALID,
        _PrivateDescriptorSetInvariantCode.PRIVATE_DESCRIPTOR_SET_ORDINAL_SEQUENCE_INVALID: I0AResultCode.ERR_ORDINAL_SEQUENCE_INVALID,
        _PrivateDescriptorSetInvariantCode.PRIVATE_DESCRIPTOR_SET_CANONICAL_TARGET_DUPLICATE: I0AResultCode.ERR_CANONICAL_TARGET_DUPLICATE,
        _PrivateDescriptorSetInvariantCode.PRIVATE_DESCRIPTOR_SET_SIDECAR_RELATION_INVALID: I0AResultCode.ERR_SIDECAR_RELATION_INVALID,
    }
    # The Revision 09 private domain is closed to exactly these four failures
    # plus valid; the mapping is total over the reachable failures. No silent
    # default masks an unmapped private code.
    reducer_public_fault = (
        None
        if invariant_result.code
        is _PrivateDescriptorSetInvariantCode.PRIVATE_DESCRIPTOR_SET_INVARIANTS_VALID
        else private_to_public[invariant_result.code]
    )

    # value.descriptors is already canonical-ordered, so filtering preserves
    # ascending order; no re-sort is needed.
    partition_descriptors = [
        d
        for d in value.descriptors
        if d.object_role == PreparedObjectRole.PARTITION_PAYLOAD
    ]
    partition_cardinality_fault = (
        I0AResultCode.ERR_ROLE_CARDINALITY_INVALID
        if len(partition_descriptors) != len(partition_entries)
        else None
    )

    # Emit the remaining set-invariant faults in public precedence order:
    #   12 role cardinality (fixed roles, from the reducer) and variable
    #      PARTITION_PAYLOAD cardinality (derived from the claim)
    #   13 canonical-target duplicate
    #   14 sidecar relation
    if reducer_public_fault is I0AResultCode.ERR_ROLE_CARDINALITY_INVALID:
        return ValidationResult(
            code=reducer_public_fault, established_assurances=()
        )
    if partition_cardinality_fault is not None:
        return ValidationResult(
            code=partition_cardinality_fault, established_assurances=()
        )
    if reducer_public_fault is not None:
        return ValidationResult(
            code=reducer_public_fault, established_assurances=()
        )
    # Exact descriptor-to-entry binding (partition_payload_cardinality_
    # authority): the PARTITION_PAYLOAD descriptor at partition_ordinal k
    # binds claim entry k under the complete descriptor ordering rule.
    # There is no independent path/identity/logical-hash authority: the
    # same-ordinal descriptor's canonical_target_path, grammar-parsed
    # partition_id, and logical_sha256 must each equal the bound entry's.
    # This is the lowest-priority fault class (precedence 15) and runs only
    # after every higher-priority claim, descriptor, and set-invariant fault
    # has been ruled out.
    for k, entry in enumerate(partition_entries):
        d = partition_descriptors[k]
        # Exact descriptor-entry ordinal binding: the descriptor bound to
        # claim entry k must itself have object_ordinal == k. A partition
        # descriptor set that is complete and role-cardinality-correct but
        # not laid out at contiguous ordinals 0..M-1 (e.g. a PARTITION_PAYLOAD
        # descriptor at ordinal 1 while claim entry 0 needs binding) is
        # caught here rather than silently bound by list position alone.
        if d.object_ordinal != k:
            return ValidationResult(
                code=I0AResultCode.ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH,
                established_assurances=(),
            )
        if d.canonical_target_path != entry.get("partition_path"):
            return ValidationResult(
                code=I0AResultCode.ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH,
                established_assurances=(),
            )
        descriptor_partition_id = _find_partition_id_in_path(d.canonical_target_path)
        if descriptor_partition_id != entry.get("partition_id"):
            return ValidationResult(
                code=I0AResultCode.ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH,
                established_assurances=(),
            )
        if d.logical_sha256 != entry.get("partition_logical_sha256"):
            return ValidationResult(
                code=I0AResultCode.ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH,
                established_assurances=(),
            )

    # Non-reuse prepared-object source identity binding (precedence 15).
    # Each non-reuse durable_source_path has ALREADY passed the frozen
    # PREPARED_OBJECT_BIN grammar and its own ordinal-placeholder check in
    # validate_prepared_object_descriptor, so every path reaching here is a
    # VALID path. What is checked now is whether that valid path's embedded
    # identity AGREES with the other validated inputs -- a cross-input
    # mismatch, not a malformed path. Malformed paths never reach this
    # point; they were already returned as path-class faults at 8/9.
    #
    # PREPARED_OBJECT_BIN template:
    #   artifacts/local_curl_per_side/runs/<run_id>/prepared_evidence/
    #   <unit_kind>/<prepared_unit_id>/objects/<object_ordinal_10d>.bin
    # so the placeholders are recoverable by deterministic string splitting.
    # These are string/placeholder identity comparisons only; they assert no
    # filesystem fact.
    claim_run_id = claim.get("run_id")
    prepared_unit_directories = set()
    for d in value.descriptors:
        if d.publication_mode == PublicationMode.REUSE_IMMUTABLE_SOURCE:
            continue
        source_identity = _parse_prepared_object_source_identity(
            d.durable_source_path
        )
        if source_identity is None:
            return ValidationResult(
                code=I0AResultCode.ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH,
                established_assurances=(),
            )
        source_run_id, source_unit_kind, source_unit_dir, source_ordinal = (
            source_identity
        )
        # Embedded unit_kind equals the context's unit kind.
        if source_unit_kind != value.unit_context.unit_kind.value:
            return ValidationResult(
                code=I0AResultCode.ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH,
                established_assurances=(),
            )
        # Embedded object ordinal equals this descriptor's object_ordinal.
        if source_ordinal != d.object_ordinal:
            return ValidationResult(
                code=I0AResultCode.ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH,
                established_assurances=(),
            )
        # Source run identity equals the validated claim run identity, which
        # the same-ordinal binding above has already tied to the canonical
        # target paths.
        if source_run_id != claim_run_id:
            return ValidationResult(
                code=I0AResultCode.ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH,
                established_assurances=(),
            )
        prepared_unit_directories.add(source_unit_dir)
    # All non-reuse descriptors belong to one common prepared-unit directory.
    if len(prepared_unit_directories) > 1:
        return ValidationResult(
            code=I0AResultCode.ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH,
            established_assurances=(),
        )

    # UnitContext-to-claim identity binding (precedence 15). The context and
    # the claim are two separately-valid inputs; a context describing a
    # different subject family or sequence than the fully validated claim is
    # a cross-input mismatch and must not reach I0A_VALID_A2_SET. This runs
    # last, after every claim-schema, predecessor, coverage, logical-hash,
    # descriptor, ordinal, and set-invariant fault has been ruled out, so it
    # never displaces a higher-precedence fault.
    if value.unit_context.subject_family != claim.get("audit_family"):
        return ValidationResult(
            code=I0AResultCode.ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH,
            established_assurances=(),
        )
    if value.unit_context.subject_sequence != claim.get("snapshot_sequence"):
        return ValidationResult(
            code=I0AResultCode.ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH,
            established_assurances=(),
        )

    return ValidationResult(
        code=I0AResultCode.I0A_VALID_A2_SET,
        established_assurances=(
            AssuranceLevel.A1_LEXICAL_PATH_SHAPE,
            AssuranceLevel.A2_SINGLE_DESCRIPTOR_CLOSED_FIELDS,
            AssuranceLevel.A2_DESCRIPTOR_SET_COMPLETE,
        ),
    )


_IMPLEMENTED_ACCEPTED_SCHEMA_SET = frozenset()  # I0A implements no accepted-registry table/json payload decoder


def validate_payload_logical_representation(
    value: AcceptedRegistryLogicalValidationInput,
) -> ValidationResult:
    """Accepted-registry json:/table: membership surface only. Internal
    i0a: relation IDs return ERR_SELECTED_SCHEMA_INVALID before membership
    lookup. I0A implements no accepted-registry table payload decoder, so
    valid table IDs stop without A4."""
    from .finding4_registry import build_accepted_registry_schema_definition_index

    registry_result = build_accepted_registry_schema_definition_index(
        value.accepted_registry_bytes
    )
    if registry_result.code != I0AResultCode.I0A_REGISTRY_INDEX_MATERIALIZED_A3H:
        return ValidationResult(
            code=I0AResultCode.ERR_GOVERNING_PACKAGE_BYTES_MISMATCH,
            established_assurances=(),
        )
    if not isinstance(value.schema_id, str) or value.schema_id.startswith("i0a:"):
        return ValidationResult(
            code=I0AResultCode.ERR_SELECTED_SCHEMA_INVALID,
            established_assurances=(),
        )
    if value.schema_id not in registry_result.index.schema_ids:
        return ValidationResult(
            code=I0AResultCode.STOP_SCHEMA_REFERENCE_UNRESOLVED,
            established_assurances=(),
        )
    # I0A implements no accepted-registry payload decoder (json: or
    # table:), so every accepted-registry member stops here with the typed
    # out-of-scope code (pinned by T067). _IMPLEMENTED_ACCEPTED_SCHEMA_SET
    # remains empty in I0A; a future increment implementing a decoder
    # would branch to decoded-row validation for its members instead.
    return ValidationResult(
        code=I0AResultCode.STOP_PAYLOAD_LOGICAL_VALIDATION_OUT_OF_SCOPE,
        established_assurances=(),
    )


_INTERNAL_RELATION_ROW_FIELDS = {
    StructuralRelationSchemaId.PREPARED_CLAIM_OBJECT_RELATION: (
        "object_ordinal",
        "object_role",
        "content_schema_id",
        "canonical_target_path",
    ),
    StructuralRelationSchemaId.PREPARED_PLANNED_OBJECT_RELATION: (
        "object_ordinal",
        "object_role",
        "content_schema_id",
        "publication_mode",
        "canonical_target_path",
    ),
    StructuralRelationSchemaId.PREPARED_OBJECT_DESCRIPTOR_RELATION: (
        "object_ordinal",
        "object_role",
        "content_schema_id",
        "publication_mode",
        "durable_source_path",
        "canonical_target_path",
        "file_size_bytes",
        "file_sha256",
        "logical_sha256",
        "sidecar_of_object_ordinal",
    ),
}


_INTERNAL_RELATION_ROW_FIELD_TAGS = {
    StructuralRelationSchemaId.PREPARED_CLAIM_OBJECT_RELATION: (
        ("object_ordinal", "UINT"),
        ("object_role", "STRING"),
        ("content_schema_id", "STRING"),
        ("canonical_target_path", "STRING"),
    ),
    StructuralRelationSchemaId.PREPARED_PLANNED_OBJECT_RELATION: (
        ("object_ordinal", "UINT"),
        ("object_role", "STRING"),
        ("content_schema_id", "STRING"),
        ("publication_mode", "STRING"),
        ("canonical_target_path", "STRING"),
    ),
    StructuralRelationSchemaId.PREPARED_OBJECT_DESCRIPTOR_RELATION: (
        ("object_ordinal", "UINT"),
        ("object_role", "STRING"),
        ("content_schema_id", "STRING"),
        ("publication_mode", "STRING"),
        ("durable_source_path", "STRING"),
        ("canonical_target_path", "STRING"),
        ("file_size_bytes", "UINT"),
        ("file_sha256", "SHA256"),
        ("logical_sha256", "SHA256"),
        ("sidecar_of_object_ordinal", "UINT"),
    ),
}

_RELATION_NULLABLE_FIELDS = {
    StructuralRelationSchemaId.PREPARED_CLAIM_OBJECT_RELATION: frozenset(),
    StructuralRelationSchemaId.PREPARED_PLANNED_OBJECT_RELATION: frozenset(),
    StructuralRelationSchemaId.PREPARED_OBJECT_DESCRIPTOR_RELATION: frozenset(
        {"logical_sha256", "sidecar_of_object_ordinal"}
    ),
}


def _relation_row_bytes(schema_id: StructuralRelationSchemaId, row: Mapping[str, object]) -> bytes:
    # Confirmed via valid_structural_claim_scope_sidecar_input's pinned
    # object_claims_logical_sha256: internal relation rows use the same
    # typed-cell-object (n/t/v) encoding as canonical_typed_row_bytes, not
    # a plain positional JSON array.
    field_tags = _INTERNAL_RELATION_ROW_FIELD_TAGS[schema_id]
    nullable = _RELATION_NULLABLE_FIELDS[schema_id]
    cells = []
    for name, tag in field_tags:
        value = row.get(name)
        effective_tag = "NULL" if (name in nullable and value is None) else tag
        cells.append({"n": name, "t": effective_tag, "v": value})
    parts = [
        json.dumps(c, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        for c in cells
    ]
    return b"[" + b",".join(parts) + b"]"


def _partition_entry_typed_row_bytes(entry: Mapping[str, object]) -> bytes:
    # embedded:snapshot_claim_partition_entry_v23 relation row: the seven
    # declared fields, each encoded as a canonical typed-cell (n/t/v)
    # object in field order, wrapped in a JSON array with compact
    # separators and no LF. first_key_canonical_json and
    # last_key_canonical_json are NULL iff row_count=0 (both null together);
    # a null value carries the NULL tag. Byte-identical to the pinned
    # exact_rev06_fixture typed_row_utf8.
    cells = []
    for name, tag in _PARTITION_ENTRY_ROW_FIELD_TAGS:
        value = entry.get(name)
        effective_tag = "NULL" if value is None else tag
        cells.append({"n": name, "t": effective_tag, "v": value})
    parts = [
        json.dumps(c, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        for c in cells
    ]
    return b"[" + b",".join(parts) + b"]"


def validate_structural_relation(
    value: StructuralRelationValidationInput,
) -> ValidationResult:
    """Validates only the three internal StructuralRelationSchemaId
    domains. It performs no accepted-registry membership lookup and cannot
    accept json:/table: IDs."""
    if not isinstance(value.schema_id, StructuralRelationSchemaId):
        return ValidationResult(
            code=I0AResultCode.ERR_LOGICAL_ROWS_INVALID,
            established_assurances=(),
        )

    required_fields = set(_INTERNAL_RELATION_ROW_FIELDS[value.schema_id])
    for row in value.decoded_rows:
        if not isinstance(row, dict) or set(row.keys()) != required_fields:
            return ValidationResult(
                code=I0AResultCode.ERR_LOGICAL_ROWS_INVALID,
                established_assurances=(),
            )

    for i, row in enumerate(value.decoded_rows):
        if row.get("object_ordinal") != i:
            return ValidationResult(
                code=I0AResultCode.ERR_ORDINAL_SEQUENCE_INVALID,
                established_assurances=(),
            )

    if value.decoded_rows:
        joined = b"\n".join(
            _relation_row_bytes(value.schema_id, row) for row in value.decoded_rows
        )
    else:
        joined = b""
    logical_sha256 = hashlib.sha256(joined).hexdigest()
    if logical_sha256 != value.expected_logical_sha256:
        return ValidationResult(
            code=I0AResultCode.ERR_LOGICAL_SHA256_MISMATCH,
            established_assurances=(),
        )

    return ValidationResult(
        code=I0AResultCode.I0A_VALID_A4_INTERNAL_RELATION,
        established_assurances=(AssuranceLevel.A4_DECODED_LOGICAL_ROWS_VALIDATED,),
    )


def validate_selected_json_payload(value: SelectedJsonPayloadInput) -> ValidationResult:
    """Only json:sha256_sidecar is selected-schema implemented. Revalidate
    A2 set and binding, reconcile sidecar and paired target independently
    at generic A3, then validate exact canonical sidecar fields/path/hash."""
    unit_context = value.descriptor_set_input.unit_context
    if unit_context.unit_kind != PreparedUnitKind.SNAPSHOT_PUBLICATION:
        return ValidationResult(
            code=I0AResultCode.STOP_UNIT_KIND_NOT_ACCEPTED_I0A,
            established_assurances=(),
        )

    from .finding4_registry import build_accepted_registry_schema_definition_index

    registry_result = build_accepted_registry_schema_definition_index(
        value.accepted_registry_bytes
    )
    if registry_result.code != I0AResultCode.I0A_REGISTRY_INDEX_MATERIALIZED_A3H:
        return ValidationResult(
            code=I0AResultCode.ERR_GOVERNING_PACKAGE_BYTES_MISMATCH,
            established_assurances=(),
        )

    try:
        sidecar_obj = _parse_canonical_json_strict(value.selected_payload_bytes)
    except (ValueError, UnicodeDecodeError):
        return ValidationResult(
            code=I0AResultCode.ERR_CANONICAL_JSON_INVALID,
            established_assurances=(),
        )

    descriptors = value.descriptor_set_input.descriptors
    by_ordinal = {d.object_ordinal: d for d in descriptors}
    selected_descriptor = by_ordinal.get(value.selected_object_ordinal)
    if selected_descriptor is None:
        return ValidationResult(
            code=I0AResultCode.ERR_DESCRIPTOR_CLOSED_FIELD_INVALID,
            established_assurances=(),
        )
    selected_schema_id = selected_descriptor.content_schema_id
    if not isinstance(selected_schema_id, str) or selected_schema_id.startswith("i0a:"):
        return ValidationResult(
            code=I0AResultCode.ERR_SELECTED_SCHEMA_INVALID,
            established_assurances=(),
        )
    if selected_schema_id not in registry_result.index.schema_ids:
        return ValidationResult(
            code=I0AResultCode.STOP_SCHEMA_REFERENCE_UNRESOLVED,
            established_assurances=(),
        )
    if selected_schema_id != "json:sha256_sidecar":
        # Accepted-registry member whose selected-schema validation is not
        # implemented in I0A (pinned by T064): typed stop, not an error.
        return ValidationResult(
            code=I0AResultCode.STOP_CONTENT_SCHEMA_NOT_IMPLEMENTED_I0A,
            established_assurances=(),
        )

    set_result = validate_prepared_descriptor_set(value.descriptor_set_input)
    if set_result.code != I0AResultCode.I0A_VALID_A2_SET:
        return set_result

    paired_ordinal = selected_descriptor.sidecar_of_object_ordinal
    if paired_ordinal is None:
        return ValidationResult(
            code=I0AResultCode.ERR_ROLE_DISPOSITION_INVALID,
            established_assurances=(),
        )
    paired_descriptor = by_ordinal.get(paired_ordinal)
    if paired_descriptor is None:
        return ValidationResult(
            code=I0AResultCode.ERR_SIDECAR_RELATION_INVALID,
            established_assurances=(),
        )

    if value.paired_target_payload_bytes is None:
        return ValidationResult(
            code=I0AResultCode.ERR_PAIRED_TARGET_PHYSICAL_PROOF_REQUIRED,
            established_assurances=(),
        )

    sidecar_physical = reconcile_physical_payload(
        selected_descriptor.file_size_bytes,
        selected_descriptor.file_sha256,
        value.selected_payload_bytes,
    )
    if sidecar_physical.code != I0AResultCode.I0A_VALID_A3_EXACT:
        return ValidationResult(code=sidecar_physical.code, established_assurances=())

    paired_physical = reconcile_physical_payload(
        paired_descriptor.file_size_bytes,
        paired_descriptor.file_sha256,
        value.paired_target_payload_bytes,
    )
    if paired_physical.code != I0AResultCode.I0A_VALID_A3_EXACT:
        return ValidationResult(code=paired_physical.code, established_assurances=())

    if not isinstance(sidecar_obj, dict):
        return ValidationResult(
            code=I0AResultCode.ERR_PAIRED_TARGET_DESCRIPTOR_MISMATCH,
            established_assurances=(),
        )
    # Exact closed JSON membership for json:sha256_sidecar: the accepted
    # implemented_schema_contracts closed field set is exactly
    # {target_file_sha256, target_path}; any missing/extra key is a
    # selected-schema validity fault.
    if set(sidecar_obj.keys()) != {"target_file_sha256", "target_path"}:
        return ValidationResult(
            code=I0AResultCode.ERR_SELECTED_SCHEMA_INVALID,
            established_assurances=(),
        )
    if (
        sidecar_obj.get("target_path") != paired_descriptor.canonical_target_path
        or sidecar_obj.get("target_file_sha256") != paired_descriptor.file_sha256
    ):
        return ValidationResult(
            code=I0AResultCode.ERR_PAIRED_TARGET_DESCRIPTOR_MISMATCH,
            established_assurances=(),
        )

    # Establish exactly one compatible frozen binding for the selected
    # sidecar descriptor before asserting A1_REGISTRY_BINDING_RESOLVED.
    # Binding, grammar, and frozen-role ownership stay in finding4_registry;
    # this consumes its accepted resolver. The resolver's stop/error codes
    # (STOP_SCHEMA_REFERENCE_UNRESOLVED, STOP_CONTENT_SCHEMA_TARGET_BINDING_INVALID,
    # ERR_PATH_LEXICAL_INVALID, ERR_PATH_GRAMMAR_MISMATCH) are all inside
    # this function's closed result domain.
    from .finding4_registry import BindingQuery, resolve_selected_schema_binding

    binding_query = BindingQuery(
        role=selected_descriptor.object_role,
        unit_kind=unit_context.unit_kind,
        publication_mode=selected_descriptor.publication_mode,
        canonical_target_path=selected_descriptor.canonical_target_path,
        content_schema_id=selected_descriptor.content_schema_id,
        logical_sha256_is_null=selected_descriptor.logical_sha256 is None,
        sidecar_of_object_ordinal_is_null=(
            selected_descriptor.sidecar_of_object_ordinal is None
        ),
        paired_target_role=paired_descriptor.object_role,
        paired_target_content_schema_id=paired_descriptor.content_schema_id,
        paired_target_canonical_target_path=paired_descriptor.canonical_target_path,
    )
    binding_result = resolve_selected_schema_binding(
        binding_query, value.accepted_registry_bytes
    )
    if binding_result.code != I0AResultCode.I0A_BINDING_RESOLVED_A1:
        return ValidationResult(
            code=binding_result.code,
            established_assurances=(),
        )

    return ValidationResult(
        code=I0AResultCode.I0A_VALID_A6_SELECTED,
        established_assurances=(
            AssuranceLevel.A1_LEXICAL_PATH_SHAPE,
            AssuranceLevel.A1_REGISTRY_BINDING_RESOLVED,
            AssuranceLevel.A2_SINGLE_DESCRIPTOR_CLOSED_FIELDS,
            AssuranceLevel.A2_DESCRIPTOR_SET_COMPLETE,
            AssuranceLevel.A3_EXACT_LENGTH_AND_SHA256_RECONCILED,
            AssuranceLevel.A6_DESCRIPTOR_SELECTED_SCHEMA_COMPLETE,
        ),
    )


from . import finding4_registry as _registry

_SIDECAR_SIBLING_JSON_GRAMMAR = {
    StructuralMemberName.CLAIM_SCOPE_SHA256: _registry.FrozenPathGrammarId.PREPARED_CLAIM_SCOPE_JSON,
    StructuralMemberName.CLAIM_SEMANTIC_SHA256: _registry.FrozenPathGrammarId.PREPARED_CLAIM_SEMANTIC_JSON,
    StructuralMemberName.PREPARATION_PLAN_SHA256: _registry.FrozenPathGrammarId.PREPARED_PREPARATION_PLAN_JSON,
    StructuralMemberName.PREPARED_UNIT_SHA256: _registry.FrozenPathGrammarId.PREPARED_PREPARED_UNIT_JSON,
}

_STRUCTURAL_MEMBER_SUCCESS = {
    StructuralMemberName.CLAIM_SCOPE_JSON: (
        I0AResultCode.I0A_VALID_A6_STRUCTURAL,
        (
            AssuranceLevel.A3_EXACT_LENGTH_AND_SHA256_RECONCILED,
            AssuranceLevel.A6_STRUCTURAL_SCHEMA_COMPLETE,
        ),
    ),
    StructuralMemberName.CLAIM_SEMANTIC_JSON: (
        I0AResultCode.I0A_VALID_A6_STRUCTURAL,
        (
            AssuranceLevel.A3_EXACT_LENGTH_AND_SHA256_RECONCILED,
            AssuranceLevel.A6_STRUCTURAL_SCHEMA_COMPLETE,
        ),
    ),
    StructuralMemberName.PREPARATION_PLAN_JSON: (
        I0AResultCode.I0A_VALID_A3_A4_STRUCTURAL_OBJECT,
        (
            AssuranceLevel.A3_EXACT_LENGTH_AND_SHA256_RECONCILED,
            AssuranceLevel.A4_DECODED_LOGICAL_ROWS_VALIDATED,
        ),
    ),
    StructuralMemberName.PREPARED_UNIT_JSON: (
        I0AResultCode.I0A_VALID_A3_A4_STRUCTURAL_OBJECT,
        (
            AssuranceLevel.A3_EXACT_LENGTH_AND_SHA256_RECONCILED,
            AssuranceLevel.A4_DECODED_LOGICAL_ROWS_VALIDATED,
        ),
    ),
}

_STRUCTURAL_SIDECAR_SUCCESS = (
    I0AResultCode.I0A_VALID_A3_STRUCTURAL_SIDECAR,
    (
        AssuranceLevel.A3_EXACT_LENGTH_AND_SHA256_RECONCILED,
        AssuranceLevel.A3_STRUCTURAL_SIDECAR_PAIR_RECONCILED,
    ),
)


def _recompute_relation_logical_sha256(schema_id, rows):
    for i, row in enumerate(rows):
        if not isinstance(row, dict) or row.get("object_ordinal") != i:
            return None, I0AResultCode.ERR_ORDINAL_SEQUENCE_INVALID
    if rows:
        joined = b"\n".join(_relation_row_bytes(schema_id, row) for row in rows)
    else:
        joined = b""
    return hashlib.sha256(joined).hexdigest(), None


_STRUCTURAL_MEMBER_CLOSED_TOP_LEVEL_KEYS = {
    StructuralMemberName.CLAIM_SCOPE_JSON: frozenset(
        {
            "schema_version",
            "spec_revision",
            "run_id",
            "unit_kind",
            "subject_family",
            "subject_sequence",
            "expected_predecessor_commit_sha256",
            "object_claims",
            "object_claims_logical_sha256",
        }
    ),
    StructuralMemberName.CLAIM_SEMANTIC_JSON: _CLAIM_SEMANTIC_CLOSED_TOP_LEVEL_KEYS,
    StructuralMemberName.PREPARATION_PLAN_JSON: frozenset(
        {
            "schema_version",
            "spec_revision",
            "run_id",
            "unit_kind",
            "subject_family",
            "subject_sequence",
            "expected_predecessor_commit_sha256",
            "claim_scope_file_sha256",
            "claim_scope_sha256",
            "claim_semantic_file_sha256",
            "claim_semantic_sha256",
            "claim_semantic_schema_id",
            "planned_objects",
            "planned_objects_logical_sha256",
        }
    ),
    StructuralMemberName.PREPARED_UNIT_JSON: frozenset(
        {
            "schema_version",
            "spec_revision",
            "run_id",
            "unit_kind",
            "subject_family",
            "subject_sequence",
            "expected_predecessor_commit_sha256",
            "claim_scope_file_sha256",
            "claim_scope_sha256",
            "claim_semantic_file_sha256",
            "claim_semantic_sha256",
            "claim_semantic_schema_id",
            "preparation_plan_file_sha256",
            "prepared_unit_id",
            "objects",
            "objects_logical_sha256",
        }
    ),
}


def validate_structural_json_member(value: StructuralJsonMemberInput) -> ValidationResult:
    """Gate unit_kind first. Derive exact structural target paths from
    run_id, unit_context.unit_kind, prepared_unit_id, and member_name
    through finding4_registry-owned frozen grammars. Reconcile every
    member's expected length and complete-file SHA-256. For sidecars
    require paired target bytes plus exact paired expected length/SHA-256
    and require sidecar target_path to equal the independently derived
    paired target path. Persisted JSON is parsed with duplicate rejection
    and lexicographic-key canonical byte equality. Sidecars never receive
    A4."""
    if value.unit_context.unit_kind != PreparedUnitKind.SNAPSHOT_PUBLICATION:
        return ValidationResult(
            code=I0AResultCode.STOP_UNIT_KIND_NOT_ACCEPTED_I0A,
            established_assurances=(),
        )

    physical = reconcile_physical_payload(
        value.expected_file_size_bytes, value.expected_file_sha256, value.payload_bytes
    )
    if physical.code != I0AResultCode.I0A_VALID_A3_EXACT:
        return ValidationResult(code=physical.code, established_assurances=())

    is_sidecar = value.member_name in _SIDECAR_SIBLING_JSON_GRAMMAR

    if is_sidecar:
        if (
            value.paired_target_bytes is None
            or value.paired_target_expected_file_size_bytes is None
            or value.paired_target_expected_file_sha256 is None
        ):
            return ValidationResult(
                code=I0AResultCode.ERR_PAIRED_TARGET_PHYSICAL_PROOF_REQUIRED,
                established_assurances=(),
            )
        try:
            sidecar_obj = _parse_canonical_json_strict(value.payload_bytes)
        except (ValueError, UnicodeDecodeError):
            return ValidationResult(
                code=I0AResultCode.ERR_CANONICAL_JSON_INVALID,
                established_assurances=(),
            )
        paired_physical = reconcile_physical_payload(
            value.paired_target_expected_file_size_bytes,
            value.paired_target_expected_file_sha256,
            value.paired_target_bytes,
        )
        if paired_physical.code != I0AResultCode.I0A_VALID_A3_EXACT:
            return ValidationResult(code=paired_physical.code, established_assurances=())

        grammar_id = _SIDECAR_SIBLING_JSON_GRAMMAR[value.member_name]
        template, _placeholders = _registry._FROZEN_TARGET_GRAMMARS[grammar_id]
        derived_path = (
            template.replace("<run_id>", value.run_id)
            .replace("<unit_kind>", value.unit_context.unit_kind.value)
            .replace("<prepared_unit_id>", value.prepared_unit_id)
        )
        if not isinstance(sidecar_obj, dict) or set(sidecar_obj.keys()) != {
            "target_path",
            "target_file_sha256",
        }:
            return ValidationResult(
                code=I0AResultCode.ERR_CANONICAL_JSON_INVALID,
                established_assurances=(),
            )
        if (
            sidecar_obj.get("target_path") != derived_path
            or sidecar_obj.get("target_file_sha256") != value.paired_target_expected_file_sha256
        ):
            return ValidationResult(
                code=I0AResultCode.ERR_SELECTED_SCHEMA_INVALID,
                established_assurances=(),
            )
        code, assurances = _STRUCTURAL_SIDECAR_SUCCESS
        return ValidationResult(code=code, established_assurances=assurances)

    try:
        parsed = _parse_canonical_json_strict(value.payload_bytes)
    except (ValueError, UnicodeDecodeError):
        return ValidationResult(
            code=I0AResultCode.ERR_CANONICAL_JSON_INVALID,
            established_assurances=(),
        )
    if not isinstance(parsed, dict):
        return ValidationResult(
            code=I0AResultCode.ERR_CANONICAL_JSON_INVALID,
            established_assurances=(),
        )

    closed_keys = _STRUCTURAL_MEMBER_CLOSED_TOP_LEVEL_KEYS.get(value.member_name)
    if closed_keys is not None and set(parsed.keys()) != closed_keys:
        return ValidationResult(
            code=I0AResultCode.ERR_SELECTED_SCHEMA_INVALID,
            established_assurances=(),
        )

    # Predecessor rule: sequence 0 requires null predecessor commit;
    # sequence > 0 requires non-null predecessor commit.
    sequence_field = None
    predecessor_field = None
    if value.member_name in (
        StructuralMemberName.CLAIM_SCOPE_JSON,
        StructuralMemberName.PREPARATION_PLAN_JSON,
        StructuralMemberName.PREPARED_UNIT_JSON,
    ):
        sequence_field, predecessor_field = "subject_sequence", "expected_predecessor_commit_sha256"
    elif value.member_name == StructuralMemberName.CLAIM_SEMANTIC_JSON:
        sequence_field, predecessor_field = "snapshot_sequence", "previous_publication_commit_file_sha256"

    if sequence_field is not None:
        sequence_value = parsed.get(sequence_field)
        predecessor_value = parsed.get(predecessor_field)
        if not isinstance(sequence_value, int) or isinstance(sequence_value, bool):
            return ValidationResult(
                code=I0AResultCode.ERR_PREDECESSOR_RULE_INVALID,
                established_assurances=(),
            )
        if sequence_value == 0 and predecessor_value is not None:
            return ValidationResult(
                code=I0AResultCode.ERR_PREDECESSOR_RULE_INVALID,
                established_assurances=(),
            )
        if sequence_value > 0 and predecessor_value is None:
            return ValidationResult(
                code=I0AResultCode.ERR_PREDECESSOR_RULE_INVALID,
                established_assurances=(),
            )

    if value.member_name == StructuralMemberName.CLAIM_SEMANTIC_JSON:
        coverage_state = parsed.get("capture_coverage_state")
        if coverage_state not in (
            "NOT_CAPTURE",
            "CAPTURE_EMPTY_PREFIX_ORIGIN",
            "CAPTURE_THROUGH_FENCE_SEQUENCE",
        ):
            return ValidationResult(
                code=I0AResultCode.ERR_COVERAGE_STATE_INVALID,
                established_assurances=(),
            )
        covered_through = parsed.get("covered_through_fence_sequence")
        if coverage_state == "CAPTURE_THROUGH_FENCE_SEQUENCE" and covered_through is None:
            return ValidationResult(
                code=I0AResultCode.ERR_COVERAGE_STATE_INVALID,
                established_assurances=(),
            )
        if coverage_state != "CAPTURE_THROUGH_FENCE_SEQUENCE" and covered_through is not None:
            return ValidationResult(
                code=I0AResultCode.ERR_COVERAGE_STATE_INVALID,
                established_assurances=(),
            )
        partition_entries = parsed.get("partition_entries")
        if not isinstance(partition_entries, list):
            return ValidationResult(
                code=I0AResultCode.ERR_LOGICAL_ROWS_INVALID,
                established_assurances=(),
            )
        # Partition entries use the pinned seven-cell relation, not one of
        # the three internal StructuralRelationSchemaId row shapes; verify
        # ordinal sequencing directly and recompute via the seven declared
        # fields in ordinal order.
        for i, entry in enumerate(partition_entries):
            if not isinstance(entry, dict) or entry.get("partition_ordinal") != i:
                return ValidationResult(
                    code=I0AResultCode.ERR_ORDINAL_SEQUENCE_INVALID,
                    established_assurances=(),
                )
        # Accepted partition_entries_semantic_logical_sha256 projection
        # (I0A_HASH_PROJECTION_CONTRACT.json): seven canonical typed-cell
        # (n/t/v) rows in partition_ordinal order, joined by a single 0x0A,
        # no trailing LF; zero rows hash the empty byte string. Nullable
        # first/last key cells carry the NULL tag iff row_count=0. This is
        # the same typed-cell encoding as canonical rows -- NOT a plain
        # positional JSON array -- and reproduces the pinned one-partition
        # value bef068f484d8b9c230dae13031b96c4e4b7ae58a16fd08ff348f6f0d0299b58c.
        if partition_entries:
            rows_bytes = b"\n".join(
                _partition_entry_typed_row_bytes(e) for e in partition_entries
            )
        else:
            rows_bytes = b""
        semantic_logical = hashlib.sha256(rows_bytes).hexdigest()
        if semantic_logical != parsed.get("partition_entries_semantic_logical_sha256"):
            return ValidationResult(
                code=I0AResultCode.ERR_LOGICAL_SHA256_MISMATCH,
                established_assurances=(),
            )
        code, assurances = _STRUCTURAL_MEMBER_SUCCESS[value.member_name]
        return ValidationResult(code=code, established_assurances=assurances)

    if value.member_name == StructuralMemberName.CLAIM_SCOPE_JSON:
        object_claims = parsed.get("object_claims")
        if not isinstance(object_claims, list):
            return ValidationResult(
                code=I0AResultCode.ERR_LOGICAL_ROWS_INVALID,
                established_assurances=(),
            )
        recomputed, err = _recompute_relation_logical_sha256(
            StructuralRelationSchemaId.PREPARED_CLAIM_OBJECT_RELATION, object_claims
        )
        if err is not None:
            return ValidationResult(code=err, established_assurances=())
        if recomputed != parsed.get("object_claims_logical_sha256"):
            return ValidationResult(
                code=I0AResultCode.ERR_LOGICAL_SHA256_MISMATCH,
                established_assurances=(),
            )
        code, assurances = _STRUCTURAL_MEMBER_SUCCESS[value.member_name]
        return ValidationResult(code=code, established_assurances=assurances)

    if value.member_name == StructuralMemberName.PREPARATION_PLAN_JSON:
        if parsed.get("claim_semantic_schema_id") != "local_curl_snapshot_publication_claim_semantic.v23":
            return ValidationResult(
                code=I0AResultCode.ERR_CLAIM_SEMANTIC_SCHEMA_MISMATCH,
                established_assurances=(),
            )
        planned_objects = parsed.get("planned_objects")
        if not isinstance(planned_objects, list):
            return ValidationResult(
                code=I0AResultCode.ERR_LOGICAL_ROWS_INVALID,
                established_assurances=(),
            )
        recomputed, err = _recompute_relation_logical_sha256(
            StructuralRelationSchemaId.PREPARED_PLANNED_OBJECT_RELATION, planned_objects
        )
        if err is not None:
            return ValidationResult(code=err, established_assurances=())
        if recomputed != parsed.get("planned_objects_logical_sha256"):
            return ValidationResult(
                code=I0AResultCode.ERR_LOGICAL_SHA256_MISMATCH,
                established_assurances=(),
            )
        code, assurances = _STRUCTURAL_MEMBER_SUCCESS[value.member_name]
        return ValidationResult(code=code, established_assurances=assurances)

    if value.member_name == StructuralMemberName.PREPARED_UNIT_JSON:
        if parsed.get("prepared_unit_id") != value.prepared_unit_id:
            return ValidationResult(
                code=I0AResultCode.ERR_PREPARED_UNIT_ID_MISMATCH,
                established_assurances=(),
            )
        objects = parsed.get("objects")
        if not isinstance(objects, list):
            return ValidationResult(
                code=I0AResultCode.ERR_LOGICAL_ROWS_INVALID,
                established_assurances=(),
            )
        recomputed, err = _recompute_relation_logical_sha256(
            StructuralRelationSchemaId.PREPARED_OBJECT_DESCRIPTOR_RELATION, objects
        )
        if err is not None:
            return ValidationResult(code=err, established_assurances=())
        if recomputed != parsed.get("objects_logical_sha256"):
            return ValidationResult(
                code=I0AResultCode.ERR_LOGICAL_SHA256_MISMATCH,
                established_assurances=(),
            )
        code, assurances = _STRUCTURAL_MEMBER_SUCCESS[value.member_name]
        return ValidationResult(code=code, established_assurances=assurances)

    return ValidationResult(
        code=I0AResultCode.ERR_CANONICAL_JSON_INVALID,
        established_assurances=(),
    )


_REQUIRED_STRUCTURAL_MEMBER_SET = frozenset(StructuralMemberName)

_CLAIM_SEMANTIC_SCHEMA_CONST = "local_curl_snapshot_publication_claim_semantic.v23"


def validate_prepared_unit_structure(value: PreparedUnitStructureInput) -> ValidationResult:
    """Validates exact eight-member structure and cross-member invariants,
    derives descriptor set from PREPARED_UNIT plus exact CLAIM_SEMANTIC
    bytes, then validates object payloads in ordinal order. A complete
    snapshot unit stops at first non-sidecar selected schema outside I0A."""
    if value.unit_context.unit_kind != PreparedUnitKind.SNAPSHOT_PUBLICATION:
        return ValidationResult(
            code=I0AResultCode.STOP_UNIT_KIND_NOT_ACCEPTED_I0A,
            established_assurances=(),
        )

    if frozenset(value.structural_members.keys()) != _REQUIRED_STRUCTURAL_MEMBER_SET:
        return ValidationResult(
            code=I0AResultCode.ERR_STRUCTURAL_MEMBER_SET_INVALID,
            established_assurances=(),
        )

    from .finding4_registry import build_accepted_registry_schema_definition_index as _build_index

    registry_result = _build_index(value.accepted_registry_bytes)
    if registry_result.code != I0AResultCode.I0A_REGISTRY_INDEX_MATERIALIZED_A3H:
        return ValidationResult(
            code=I0AResultCode.ERR_GOVERNING_PACKAGE_BYTES_MISMATCH,
            established_assurances=(),
        )

    parsed_members = {}
    for name in (
        StructuralMemberName.CLAIM_SCOPE_JSON,
        StructuralMemberName.CLAIM_SEMANTIC_JSON,
        StructuralMemberName.PREPARATION_PLAN_JSON,
        StructuralMemberName.PREPARED_UNIT_JSON,
    ):
        try:
            parsed_members[name] = _parse_canonical_json_strict(
                value.structural_members[name]
            )
        except (ValueError, UnicodeDecodeError):
            return ValidationResult(
                code=I0AResultCode.ERR_CANONICAL_JSON_INVALID,
                established_assurances=(),
            )
        if not isinstance(parsed_members[name], dict):
            return ValidationResult(
                code=I0AResultCode.ERR_CANONICAL_JSON_INVALID,
                established_assurances=(),
            )

    claim_scope = parsed_members[StructuralMemberName.CLAIM_SCOPE_JSON]
    claim_semantic = parsed_members[StructuralMemberName.CLAIM_SEMANTIC_JSON]
    plan = parsed_members[StructuralMemberName.PREPARATION_PLAN_JSON]
    prepared_unit = parsed_members[StructuralMemberName.PREPARED_UNIT_JSON]

    # Ordered precedence pinned by the static matrix: cross-member
    # consistency (T057/T079) precedes the claim-semantic schema check
    # (T061/T081), which precedes prepared-unit-id derivation (T060/T080);
    # per-member predecessor and coverage checks follow.
    #
    # Accepted cross_member_hash_rules.plan_unit_cross_member
    # (I0A_HASH_PROJECTION_CONTRACT.json): run_id, unit_kind,
    # subject_sequence, subject_family, expected predecessor, claim-scope
    # hashes, and claim-semantic schema/file/digest are typed-equal
    # between the plan and unit copies; claim_scope_file_sha256 and
    # claim_semantic_file_sha256 additionally equal the SHA-256 of the
    # exact CLAIM_SCOPE.json / CLAIM_SEMANTIC.json member bytes. The
    # claim-scope member's run_id must also match. claim_scope_sha256 is a
    # distinct top-level digest field and is NEVER compared against the
    # claim-scope member's object_claims_logical_sha256.
    claim_scope_file_sha256 = hashlib.sha256(
        value.structural_members[StructuralMemberName.CLAIM_SCOPE_JSON]
    ).hexdigest()
    claim_semantic_file_sha256 = hashlib.sha256(
        value.structural_members[StructuralMemberName.CLAIM_SEMANTIC_JSON]
    ).hexdigest()
    if (
        plan.get("run_id") != prepared_unit.get("run_id")
        or plan.get("run_id") != claim_scope.get("run_id")
        or plan.get("unit_kind") != prepared_unit.get("unit_kind")
        or plan.get("subject_sequence") != prepared_unit.get("subject_sequence")
        or plan.get("subject_family") != prepared_unit.get("subject_family")
        or plan.get("expected_predecessor_commit_sha256")
        != prepared_unit.get("expected_predecessor_commit_sha256")
        or plan.get("claim_scope_file_sha256")
        != prepared_unit.get("claim_scope_file_sha256")
        or plan.get("claim_scope_sha256") != prepared_unit.get("claim_scope_sha256")
        or plan.get("claim_semantic_schema_id")
        != prepared_unit.get("claim_semantic_schema_id")
        or plan.get("claim_semantic_file_sha256")
        != prepared_unit.get("claim_semantic_file_sha256")
        or plan.get("claim_semantic_sha256")
        != prepared_unit.get("claim_semantic_sha256")
        or plan.get("claim_scope_file_sha256") != claim_scope_file_sha256
        or plan.get("claim_semantic_file_sha256") != claim_semantic_file_sha256
    ):
        return ValidationResult(
            code=I0AResultCode.ERR_PLAN_UNIT_CROSS_MEMBER_MISMATCH,
            established_assurances=(),
        )

    if plan.get("claim_semantic_schema_id") != _CLAIM_SEMANTIC_SCHEMA_CONST:
        return ValidationResult(
            code=I0AResultCode.ERR_CLAIM_SEMANTIC_SCHEMA_MISMATCH,
            established_assurances=(),
        )

    expected_prepared_unit_id = "prep_" + hashlib.sha256(
        value.structural_members[StructuralMemberName.PREPARATION_PLAN_JSON]
    ).hexdigest()
    prepared_unit_id = prepared_unit.get("prepared_unit_id")
    if prepared_unit_id != expected_prepared_unit_id:
        return ValidationResult(
            code=I0AResultCode.ERR_PREPARED_UNIT_ID_MISMATCH,
            established_assurances=(),
        )

    for parsed, seq_field, pred_field in (
        (claim_scope, "subject_sequence", "expected_predecessor_commit_sha256"),
        (plan, "subject_sequence", "expected_predecessor_commit_sha256"),
        (prepared_unit, "subject_sequence", "expected_predecessor_commit_sha256"),
        (claim_semantic, "snapshot_sequence", "previous_publication_commit_file_sha256"),
    ):
        seq_val = parsed.get(seq_field)
        pred_val = parsed.get(pred_field)
        if not isinstance(seq_val, int) or isinstance(seq_val, bool):
            return ValidationResult(
                code=I0AResultCode.ERR_PREDECESSOR_RULE_INVALID,
                established_assurances=(),
            )
        if (seq_val == 0) != (pred_val is None):
            return ValidationResult(
                code=I0AResultCode.ERR_PREDECESSOR_RULE_INVALID,
                established_assurances=(),
            )

    coverage_state = claim_semantic.get("capture_coverage_state")
    if coverage_state not in (
        "NOT_CAPTURE",
        "CAPTURE_EMPTY_PREFIX_ORIGIN",
        "CAPTURE_THROUGH_FENCE_SEQUENCE",
    ):
        return ValidationResult(
            code=I0AResultCode.ERR_COVERAGE_STATE_INVALID,
            established_assurances=(),
        )

    objects = prepared_unit.get("objects")
    if not isinstance(objects, list):
        return ValidationResult(
            code=I0AResultCode.ERR_DESCRIPTOR_CLOSED_FIELD_INVALID,
            established_assurances=(),
        )

    descriptors = []
    for row in objects:
        if not isinstance(row, dict):
            return ValidationResult(
                code=I0AResultCode.ERR_DESCRIPTOR_CLOSED_FIELD_INVALID,
                established_assurances=(),
            )
        try:
            descriptors.append(
                PreparedObjectDescriptor(
                    object_ordinal=row["object_ordinal"],
                    object_role=PreparedObjectRole(row["object_role"]),
                    content_schema_id=row["content_schema_id"],
                    publication_mode=PublicationMode(row["publication_mode"]),
                    durable_source_path=row["durable_source_path"],
                    canonical_target_path=row["canonical_target_path"],
                    file_size_bytes=row["file_size_bytes"],
                    file_sha256=row["file_sha256"],
                    logical_sha256=row.get("logical_sha256"),
                    sidecar_of_object_ordinal=row.get("sidecar_of_object_ordinal"),
                )
            )
        except (KeyError, ValueError):
            return ValidationResult(
                code=I0AResultCode.ERR_DESCRIPTOR_CLOSED_FIELD_INVALID,
                established_assurances=(),
            )

    set_result = validate_prepared_descriptor_set(
        DescriptorSetInput(
            unit_context=value.unit_context,
            descriptors=tuple(descriptors),
            snapshot_claim_semantic_bytes=value.structural_members[
                StructuralMemberName.CLAIM_SEMANTIC_JSON
            ],
        )
    )
    if set_result.code != I0AResultCode.I0A_VALID_A2_SET:
        return set_result

    descriptor_by_ordinal = {d.object_ordinal: d for d in descriptors}
    # Validate object payloads in exact descriptor ordinal order. Every
    # descriptor's object payload is required: an absent ordinal or missing
    # payload is not silently skipped. The complete canonical unit clears
    # all A3 checks and terminates at ordinal 0 (table:capture_events) with
    # STOP_CONTENT_SCHEMA_NOT_IMPLEMENTED_I0A.
    for ordinal in sorted(descriptor_by_ordinal.keys()):
        descriptor = descriptor_by_ordinal[ordinal]
        if ordinal not in value.object_payload_bytes_by_ordinal:
            return ValidationResult(
                code=I0AResultCode.ERR_PHYSICAL_EXPECTATION_INVALID,
                established_assurances=(),
            )
        payload = value.object_payload_bytes_by_ordinal[ordinal]
        physical = reconcile_physical_payload(
            descriptor.file_size_bytes, descriptor.file_sha256, payload
        )
        if physical.code != I0AResultCode.I0A_VALID_A3_EXACT:
            return ValidationResult(code=physical.code, established_assurances=())

        schema_id = descriptor.content_schema_id
        if schema_id == "json:sha256_sidecar":
            continue
        if schema_id not in registry_result.index.schema_ids:
            return ValidationResult(
                code=I0AResultCode.STOP_SCHEMA_REFERENCE_UNRESOLVED,
                established_assurances=(),
            )
        return ValidationResult(
            code=I0AResultCode.STOP_CONTENT_SCHEMA_NOT_IMPLEMENTED_I0A,
            established_assurances=(),
        )

    # Contract: validate_prepared_unit_structure has no success code
    # (success: none); every accepted traversal terminates at the first
    # non-sidecar selected schema with STOP_CONTENT_SCHEMA_NOT_IMPLEMENTED_I0A.
    # For an accepted eight-member unit the earlier structural, role-
    # cardinality, and descriptor-set checks guarantee a non-sidecar
    # PARTITION_PAYLOAD at ordinal 0, so the loop above always returns; this
    # terminal is only reached by an all-sidecar payload set, which is
    # unreachable for accepted inputs. It returns the same in-domain
    # terminal STOP rather than any out-of-domain success code.
    return ValidationResult(
        code=I0AResultCode.STOP_CONTENT_SCHEMA_NOT_IMPLEMENTED_I0A,
        established_assurances=(),
    )


def dispatch_i0a_unit_validation(value: PreparedUnitStructureInput) -> ValidationResult:
    """Owned by prepared_evidence.py; unit-kind gate precedes delegation to
    validate_prepared_unit_structure; no registry-to-prepared import."""
    if value.unit_context.unit_kind != PreparedUnitKind.SNAPSHOT_PUBLICATION:
        return ValidationResult(
            code=I0AResultCode.STOP_UNIT_KIND_NOT_ACCEPTED_I0A,
            established_assurances=(),
        )
    return validate_prepared_unit_structure(value)


def validate_filesystem_facts(request: FilesystemValidationRequest) -> ValidationResult:
    """Always returns typed out-of-scope stop; caller booleans do not
    establish filesystem facts."""
    return ValidationResult(
        code=I0AResultCode.STOP_FILESYSTEM_FACTS_OUT_OF_SCOPE,
        established_assurances=(),
    )


def validate_full_prepared_object(
    request: FullPreparedObjectValidationRequest,
) -> ValidationResult:
    """A7 unreachable because independent filesystem facts are
    unauthorized."""
    unit_context = request.selected_input.descriptor_set_input.unit_context
    if unit_context.unit_kind != PreparedUnitKind.SNAPSHOT_PUBLICATION:
        return ValidationResult(
            code=I0AResultCode.STOP_UNIT_KIND_NOT_ACCEPTED_I0A,
            established_assurances=(),
        )
    return ValidationResult(
        code=I0AResultCode.STOP_FILESYSTEM_FACTS_OUT_OF_SCOPE,
        established_assurances=(),
    )


def validate_full_prepared_unit(
    request: FullPreparedUnitValidationRequest,
) -> ValidationResult:
    """A8 unreachable because independent filesystem facts and
    unimplemented selected schemas remain outside I0A."""
    if request.unit_input.unit_context.unit_kind != PreparedUnitKind.SNAPSHOT_PUBLICATION:
        return ValidationResult(
            code=I0AResultCode.STOP_UNIT_KIND_NOT_ACCEPTED_I0A,
            established_assurances=(),
        )
    return ValidationResult(
        code=I0AResultCode.STOP_FILESYSTEM_FACTS_OUT_OF_SCOPE,
        established_assurances=(),
    )
