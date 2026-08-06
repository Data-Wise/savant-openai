#!/usr/bin/env python3
"""Deterministic symbolic CAS check for a stated proof residual.

Reduces the supplied residual expression with SymPy. A residual that
simplifies to exactly zero reports `PASS`; a nonzero residual reports
`FAIL`; an unparseable expression or missing backend reports `UNVERIFIED`.
The status vocabulary mirrors `verification-status.md` check statuses.
"""

from __future__ import annotations

import argparse
import json
import sys

BACKEND_NAME = "sympy"


def check(residual: str, positive_symbols: tuple[str, ...] = ()) -> dict[str, object]:
    try:
        import sympy as sp
    except ImportError:
        return {
            "status": "UNVERIFIED",
            "backend": None,
            "backend_version": None,
            "residual": residual,
            "reason": "symbolic backend unavailable",
        }
    try:
        symbols = {}
        for name in positive_symbols:
            symbols[name] = sp.Symbol(name, positive=True)
        expr = sp.sympify(residual, locals=symbols)
        simplified = sp.simplify(expr)
    except Exception as exc:
        return {
            "status": "UNVERIFIED",
            "backend": BACKEND_NAME,
            "backend_version": sp.__version__,
            "residual": residual,
            "reason": f"expression could not be evaluated: {exc}",
        }
    return {
        "status": "PASS" if simplified == 0 else "FAIL",
        "backend": BACKEND_NAME,
        "backend_version": sp.__version__,
        "residual": residual,
        "positive_symbols": list(positive_symbols),
        "simplified": str(simplified),
    }


def render(result: dict[str, object]) -> str:
    lines = [f"STATUS: {result['status']}"]
    if result["backend"]:
        lines.append(f"BACKEND: {result['backend']} {result['backend_version']}")
    lines.append(f"RESIDUAL: {result['residual']}")
    if result.get("positive_symbols"):
        lines.append(f"DOMAIN: positive {', '.join(result['positive_symbols'])}")
    if result.get("simplified") is not None:
        lines.append(f"SIMPLIFIED: {result['simplified']}")
    if result.get("reason"):
        lines.append(f"REASON: {result['reason']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("residual", help="sympy expression to simplify (e.g. 'log(exp(x)) - x')")
    parser.add_argument(
        "--positive",
        metavar="SYMBOLS",
        default="",
        help="comma-separated symbols to declare positive, matching the claim's domain",
    )
    parser.add_argument("--json", action="store_true", help="emit a JSON object instead of text")
    args = parser.parse_args(argv)

    positive = tuple(
        name.strip() for name in args.positive.split(",") if name.strip()
    )
    result = check(args.residual, positive)
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else render(result))
    return {"PASS": 0, "FAIL": 1, "UNVERIFIED": 2}[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
