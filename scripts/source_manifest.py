#!/usr/bin/env python3
"""Hash only explicit reviewed paths from an authorized read-only source tree."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST = ROOT / 'docs/source-allowlist.txt'
FORBIDDEN_NAMES = {'app.config', 'config.local.h', 'credentials.h', 'secrets.h', '.env', 'local.properties'}
FORBIDDEN_PARTS = {'.pio', 'bin', 'obj', 'build', '.idea', '.vscode', '.git'}


def safe_paths() -> list[str]:
    rows: list[str] = []
    for raw in ALLOWLIST.read_text(encoding='utf-8').splitlines():
        value = raw.strip()
        if not value or value.startswith('#'):
            continue
        candidate = Path(value)
        if candidate.is_absolute() or '..' in candidate.parts:
            raise ValueError(f'unsafe allowlist path: {value}')
        if candidate.name.lower() in FORBIDDEN_NAMES or any(part in FORBIDDEN_PARTS for part in candidate.parts):
            raise ValueError(f'local/generated path in allowlist: {value}')
        rows.append(value)
    if rows != sorted(rows):
        raise ValueError('allowlist paths must be sorted')
    if len(rows) != len(set(rows)):
        raise ValueError('allowlist paths must be unique')
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', required=True)
    source = Path(parser.parse_args().source).resolve()
    if not source.is_dir():
        raise SystemExit(f'not a directory: {source}')
    digest = hashlib.sha256()
    paths = safe_paths()
    for rel in paths:
        path = source / rel
        if not path.is_file():
            raise SystemExit(f'missing allowlisted source file: {rel}')
        digest.update(rel.encode('utf-8')); digest.update(b'\0')
        digest.update(path.read_bytes()); digest.update(b'\0')
    print(f'files={len(paths)}')
    print(f'sha256={digest.hexdigest()}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
