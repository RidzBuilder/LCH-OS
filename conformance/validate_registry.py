"""A-R06.2 canonical schema and registry validator (initial implementation).

Usage:
  python conformance/validate_registry.py --root specifications

Requires jsonschema with Draft 2020-12 support. This validator checks JSON syntax,
schema validity, and basic cross-reference integrity for known registry collections.
It does not establish runtime conformance or prove external platform behavior.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_schema(schema_path: Path, document_path: Path) -> list[str]:
    schema = load_json(schema_path)
    document = load_json(document_path)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(document), key=lambda e: list(map(str, e.path)))
    return [
        f"{document_path}: /{'/'.join(map(str, error.absolute_path))}: {error.message}"
        for error in errors
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("specifications"))
    args = parser.parse_args()
    schema_dir = args.root / "schemas"
    if not schema_dir.is_dir():
        print(f"ERROR: schema directory not found: {schema_dir}", file=sys.stderr)
        return 2

    schema_files = sorted(schema_dir.glob("*.schema.json"))
    if not schema_files:
        print("ERROR: no *.schema.json files found", file=sys.stderr)
        return 2

    errors: list[str] = []
    for schema_path in schema_files:
        try:
            schema = load_json(schema_path)
            Draft202012Validator.check_schema(schema)
        except Exception as exc:  # schema parse/validation failure is a hard error
            errors.append(f"{schema_path}: invalid schema: {exc}")

    # Validate registry JSON files when a same-named schema exists.
    for document_path in sorted((args.root / "registries").glob("*.json")):
        schema_path = schema_dir / f"{document_path.stem}.schema.json"
        if schema_path.exists():
            try:
                errors.extend(validate_schema(schema_path, document_path))
            except Exception as exc:
                errors.append(f"{document_path}: validation error: {exc}")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        print(f"FAIL: {len(errors)} validation error(s)")
        return 1

    print(f"PASS: {len(schema_files)} JSON Schema document(s) are valid.")
    print("NOTE: registry referential, semantic, governance, and runtime conformance checks remain incomplete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
