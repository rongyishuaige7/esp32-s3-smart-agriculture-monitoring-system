#!/usr/bin/env python3
"""Static public-release contracts; never treats a build as hardware verification."""
from __future__ import annotations

import argparse
import csv
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REQUIRED = [
    '.github/workflows/validate.yml', '.gitattributes', '.gitignore', '.markdownlint-cli2.jsonc',
    'HARDWARE.md', 'LICENSE', 'README.md', 'SECURITY.md', 'THIRD_PARTY_NOTICES.md',
    'LICENSES/ACD10-MIT.txt', 'SmartAgriculture.sln', 'desktop/SmartAgriculture.csproj',
    'docs/GITHUB_METADATA.md', 'docs/HARDWARE_LAB_CARD.md', 'docs/PROJECT_STATUS.md',
    'docs/PROTOCOL.md', 'docs/SOURCE_PROVENANCE.md', 'docs/VERIFICATION.md', 'docs/source-allowlist.txt',
    'hardware/BOM.csv', 'hardware/wiring-diagram.svg', 'hardware/wiring.md',
    'hardware/firmware/platformio.ini', 'hardware/firmware/src/config.h',
    'hardware/firmware/src/config.local.example.h', 'hardware/firmware/src/main.cpp',
    'hardware/firmware/lib/ACD10/ACD10.cpp', 'hardware/firmware/lib/ACD10/ACD10.h',
    'scripts/check_repo.py', 'scripts/secret_scan.py', 'scripts/source_manifest.py', 'scripts/verify.sh',
    'tests/test_source_contracts.py',
]
FORBIDDEN_NAMES = {'app.config', 'config.local.h', 'credentials.h', 'secrets.h', '.env', 'local.properties', 'google-services.json'}
FORBIDDEN_DIRS = {'.pio', '.idea', '.vscode', '.vs', 'bin', 'obj', 'build', 'dist', 'release', 'coverage', '__pycache__'}
FORBIDDEN_SUFFIXES = {'.o', '.a', '.elf', '.bin', '.map', '.pyc', '.dll', '.exe', '.apk', '.aab', '.so', '.pem', '.key', '.p12', '.jks', '.zip', '.7z', '.tar', '.gz', '.ipa'}


def files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob('*') if path.is_file() and '.git' not in path.relative_to(root).parts)


def text(root: Path, rel: str) -> str:
    return (root / rel).read_text(encoding='utf-8')


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='.')
    root = Path(parser.parse_args().root).resolve()
    errors: list[str] = []
    for rel in REQUIRED:
        if not (root / rel).is_file():
            errors.append(f'missing required file: {rel}')
    for path in files(root):
        rel = path.relative_to(root)
        if path.name.lower() in FORBIDDEN_NAMES:
            errors.append(f'forbidden local/config file: {rel}')
        if any(part in FORBIDDEN_DIRS for part in rel.parts):
            errors.append(f'forbidden generated/release directory: {rel}')
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            errors.append(f'forbidden binary/archive/key artifact: {rel}')
        if path.stat().st_size > 5 * 1024 * 1024:
            errors.append(f'file exceeds 5 MiB: {rel}')
    contracts = {
        'README.md': ['公开默认', '不是农业自动化产品'],
        'desktop/SmartAgriculture.csproj': ['<TargetFramework>net8.0</TargetFramework>', 'Avalonia'],
        'desktop/ViewModels/MonitorViewModel.cs': ['示例数据（非真机）', 'TryImportTeachingJson', 'no\n    /// account, database, TCP listener'],
        'desktop/Services/TelemetryParser.cs': ['Network listening and device commands are intentionally absent', 'json.Length > 4096'],
        'hardware/firmware/platformio.ini': [
            'platform = espressif32@6.13.0',
            '[env:esp32-s3-public-default]',
            '-D ENABLE_EXPERIMENTAL_WIFI_TCP=0',
            '-D ENABLE_EXPERIMENTAL_ACTUATORS=0',
            'esp32-s3-network-telemetry-compile',
            'esp32-s3-actuator-compile',
        ],
        'hardware/firmware/src/config.h': ['#if __has_include("config.local.h")', 'ENABLE_EXPERIMENTAL_WIFI_TCP == 1', 'ENABLE_EXPERIMENTAL_ACTUATORS == 1'],
        'hardware/firmware/src/main.cpp': ['Do not configure actuator pins as output in the public default build', 'no downlink commands', 'digitalWrite(FAN_PIN_A, LOW)'],
        'docs/PROTOCOL.md': ['没有', '下行命令', 'ACK'],
        'SECURITY.md': ['没有 TCP listener', '不实现 TLS'],
        'THIRD_PARTY_NOTICES.md': ['ACD10', 'Rob Tillaart', 'FastLED'],
    }
    for rel, values in contracts.items():
        path = root / rel
        if path.is_file():
            content = text(root, rel)
            for value in values:
                if value not in content:
                    errors.append(f'fact contract missing in {rel}: {value}')
    try:
        ET.parse(root / 'hardware/wiring-diagram.svg')
    except (ET.ParseError, OSError) as exc:
        errors.append(f'invalid wiring SVG: {exc}')
    try:
        rows = list(csv.DictReader((root / 'hardware/BOM.csv').open(newline='', encoding='utf-8')))
        if len(rows) < 10:
            errors.append('BOM must contain at least 10 component rows')
        if '来源或待确认' not in (rows[0] if rows else {}):
            errors.append('BOM must include 来源或待确认 column')
    except (OSError, csv.Error) as exc:
        errors.append(f'invalid BOM.csv: {exc}')
    sln = text(root, 'SmartAgriculture.sln') if (root / 'SmartAgriculture.sln').is_file() else ''
    if 'desktop\\SmartAgriculture.csproj' not in sln or 'WinForms' in sln:
        errors.append('solution must reference only the public desktop project')
    if (root / '.git').is_dir():
        try:
            tracked = set(subprocess.check_output(['git', '-C', str(root), 'ls-files'], text=True, stderr=subprocess.PIPE).splitlines())
            for rel in REQUIRED:
                if rel not in tracked:
                    errors.append(f'required publish file is not tracked: {rel}')
        except (OSError, subprocess.CalledProcessError) as exc:
            errors.append(f'cannot inspect tracked publish files: {exc}')
    forbidden_claims = ['system online', 'current hardware verified', 'hardware re-verified: pass', 'production ready']
    for rel in ['README.md', 'docs/PROJECT_STATUS.md', 'docs/HARDWARE_LAB_CARD.md', 'docs/GITHUB_METADATA.md']:
        path = root / rel
        if path.is_file():
            lowered = text(root, rel).lower()
            for claim in forbidden_claims:
                if claim in lowered:
                    errors.append(f'unsupported claim in {rel}: {claim}')
    if errors:
        print('Repository check: FAIL', file=sys.stderr)
        print('\n'.join(f'- {item}' for item in sorted(set(errors))), file=sys.stderr)
        return 1
    print(f'Repository check: PASS ({len(files(root))} files checked)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
