#!/usr/bin/env python3
"""Fail closed on secrets, local state, release artifacts and unsupported paths."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TEXT_SUFFIXES = {'.c', '.cc', '.cpp', '.h', '.hpp', '.cs', '.csproj', '.sln', '.axaml', '.md', '.py', '.txt', '.ini', '.yml', '.yaml', '.json', '.csv', '.xml', '.svg', '.sh'}
FORBIDDEN_SUFFIXES = {'.apk', '.aab', '.bin', '.elf', '.hex', '.map', '.o', '.a', '.so', '.dll', '.exe', '.zip', '.7z', '.tar', '.gz', '.pem', '.key', '.p12', '.jks', '.keystore', '.log', '.db', '.sqlite', '.db3'}
FORBIDDEN_NAMES = {'.env', 'app.config', 'config.local.h', 'credentials.h', 'secrets.h', 'local.properties', 'google-services.json', 'googleService-info.plist', 'id_rsa', 'id_ed25519'}
FORBIDDEN_DIRS = {'.pio', '.idea', '.vscode', '.vs', 'bin', 'obj', 'build', 'dist', 'release', 'coverage', '__pycache__', '.gradle', '.dart_tool', '.kotlin', '.pub', '.pub-cache'}
PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ('private key', re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----')),
    ('GitHub token', re.compile(r'\b(?:gh[opusr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b')),
    ('AWS access key', re.compile(r'\bAKIA[0-9A-Z]{16}\b')),
    ('OpenAI-style key', re.compile(r'\bsk-[A-Za-z0-9_-]{16,}\b')),
    ('private LAN literal', re.compile(r'\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|169\.254\.\d{1,3}\.\d{1,3})\b')),
    ('local absolute path', re.compile(r'/(?:home|Users|mnt)/[^\s`"\']+')),
    ('Windows user path', re.compile(r'(?i)\b[A-Z]:\\Users\\[^\\\s]+')),
    ('assigned secret', re.compile(r'''(?ix)\b(api[_-]?key|access[_-]?token|auth[_-]?token|secret|password|passwd|pwd)\b\s*[:=]\s*["'](?!YOUR_|EXAMPLE|REPLACE|CHANGEME|REDACTED|\[REDACTED\]|<YOUR_)([A-Za-z0-9+/=_!@#$%^&*.-]{8,})["']''')),
]


def files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob('*') if path.is_file() and '.git' not in path.relative_to(root).parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='.')
    root = Path(parser.parse_args().root).resolve()
    errors: list[str] = []
    for path in files(root):
        rel = path.relative_to(root)
        lower_name = path.name.lower()
        if lower_name in FORBIDDEN_NAMES or lower_name.startswith('.env.'):
            errors.append(f'{rel}: forbidden local/config file')
        if any(part.lower() in FORBIDDEN_DIRS for part in rel.parts):
            errors.append(f'{rel}: forbidden generated/release directory')
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f'{rel}: forbidden binary/archive/key artifact')
        if path.stat().st_size > 5 * 1024 * 1024:
            errors.append(f'{rel}: file exceeds 5 MiB publication limit')
        if path.resolve() == Path(__file__).resolve() or path.suffix.lower() not in TEXT_SUFFIXES or path.stat().st_size > 2_000_000:
            continue
        try:
            content = path.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError):
            continue
        for number, line in enumerate(content.splitlines(), 1):
            for label, pattern in PATTERNS:
                if pattern.search(line):
                    errors.append(f'{rel}:{number}: {label}')
    if errors:
        print('Secret/publication scan: FAIL', file=sys.stderr)
        print('\n'.join(sorted(set(errors))), file=sys.stderr)
        return 1
    print(f'Secret/publication scan: PASS ({len(files(root))} files checked)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
