"""Confidence → probability calibration (isotonic regression, PAVA).

Hand-rolled pool-adjacent-violators so phase 1 needs no sklearn. Fit on
(raw_confidence, was_correct) pairs from RESOLVED signals only; `apply`
interpolates the fitted monotone step curve. Until `min_samples` resolved
signals exist, `ready` is False and sizing must stay in bootstrap mode.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field

import numpy as np


def _pava(y: np.ndarray, w: np.ndarray) -> np.ndarray:
    """Pool adjacent violators: weighted isotonic (non-decreasing) fit."""
    y = y.astype(float).copy()
    w = w.astype(float).copy()
    blocks = [[i] for i in range(len(y))]
    vals = list(y)
    wts = list(w)
    i = 0
    while i < len(vals) - 1:
        if vals[i] > vals[i + 1] + 1e-12:
            tw = wts[i] + wts[i + 1]
            vals[i] = (vals[i] * wts[i] + vals[i + 1] * wts[i + 1]) / tw
            wts[i] = tw
            blocks[i] += blocks[i + 1]
            del vals[i + 1], wts[i + 1], blocks[i + 1]
            i = max(i - 1, 0)
        else:
            i += 1
    out = np.empty_like(y)
    for v, idxs in zip(vals, blocks):
        out[idxs] = v
    return out


@dataclass
class IsotonicCalibrator:
    min_samples: int = 200
    _x: np.ndarray = field(default=None, repr=False)
    _y: np.ndarray = field(default=None, repr=False)

    @property
    def ready(self) -> bool:
        return self._x is not None

    def fit(self, raw_confidence: np.ndarray, was_correct: np.ndarray) -> "IsotonicCalibrator":
        raw_confidence = np.asarray(raw_confidence, dtype=float)
        was_correct = np.asarray(was_correct, dtype=float)
        if len(raw_confidence) < self.min_samples:
            raise ValueError(
                f"need >= {self.min_samples} resolved signals to calibrate, "
                f"got {len(raw_confidence)} — stay in bootstrap sizing")
        order = np.argsort(raw_confidence, kind="stable")
        x = raw_confidence[order]
        y = was_correct[order]
        # collapse duplicate x to weighted points, then PAVA
        ux, inv, counts = np.unique(x, return_inverse=True, return_counts=True)
        sums = np.zeros_like(ux)
        np.add.at(sums, inv, y)
        means = sums / counts
        fitted = _pava(means, counts.astype(float))
        self._x, self._y = ux, np.clip(fitted, 0.0, 1.0)
        return self

    def apply(self, raw_confidence: float | np.ndarray) -> np.ndarray:
        if not self.ready:
            raise RuntimeError("calibrator not fitted")
        return np.interp(np.asarray(raw_confidence, dtype=float),
                         self._x, self._y,
                         left=float(self._y[0]), right=float(self._y[-1]))

    # ---- diagnostics & persistence ----
    @staticmethod
    def brier(p: np.ndarray, y: np.ndarray) -> float:
        p, y = np.asarray(p, float), np.asarray(y, float)
        return float(np.mean((p - y) ** 2))

    def to_json(self) -> str:
        return json.dumps({"x": self._x.tolist(), "y": self._y.tolist(),
                           "min_samples": self.min_samples})

    @classmethod
    def from_json(cls, s: str) -> "IsotonicCalibrator":
        d = json.loads(s)
        c = cls(min_samples=d["min_samples"])
        c._x, c._y = np.array(d["x"]), np.array(d["y"])
        return c
