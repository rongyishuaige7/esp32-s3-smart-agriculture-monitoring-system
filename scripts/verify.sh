#!/usr/bin/env bash
# Public-release gate. All builds happen in isolated copies outside the candidate tree.
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
BASE="${XDG_CACHE_HOME:-$HOME/.cache}/smart-agriculture-public-verify-$$"
PYCACHE="$BASE/pycache"
DESKTOP_WORK="$BASE/desktop"
FIRMWARE_WORK="$BASE/firmware"
NUGET_PACKAGES="$BASE/nuget"
cleanup() { rm -rf -- "$BASE" "$ROOT/tests/__pycache__"; }
trap cleanup EXIT
mkdir -p "$PYCACHE" "$DESKTOP_WORK" "$FIRMWARE_WORK" "$NUGET_PACKAGES"
export PYTHONPYCACHEPREFIX="$PYCACHE"

python3 "$ROOT/scripts/secret_scan.py" --root "$ROOT"
python3 "$ROOT/scripts/check_repo.py" --root "$ROOT"
python3 -m unittest discover -s "$ROOT/tests" -p 'test_*.py' -v

rsync -a --delete --exclude='.git/' --exclude='bin/' --exclude='obj/' "$ROOT/desktop/" "$DESKTOP_WORK/"
cp "$ROOT/SmartAgriculture.sln" "$BASE/SmartAgriculture.sln"
sed -i 's#desktop\\\\SmartAgriculture.csproj#desktop\\\\SmartAgriculture.csproj#' "$BASE/SmartAgriculture.sln"
(
  cd "$BASE"
  NUGET_PACKAGES="$NUGET_PACKAGES" dotnet restore SmartAgriculture.sln --verbosity minimal
  NUGET_PACKAGES="$NUGET_PACKAGES" dotnet build SmartAgriculture.sln --no-restore --configuration Release --verbosity minimal
)

rsync -a --delete --exclude='.git/' --exclude='.pio/' --exclude='.vscode/' "$ROOT/hardware/firmware/" "$FIRMWARE_WORK/"
pio run -d "$FIRMWARE_WORK" -e esp32-s3-public-default -e esp32-s3-network-telemetry-compile -e esp32-s3-actuator-compile

python3 "$ROOT/scripts/secret_scan.py" --root "$ROOT"
python3 "$ROOT/scripts/check_repo.py" --root "$ROOT"
echo 'Verification: PASS (static and isolated build evidence only; no desktop UI, database, hardware, sensor, OLED, network, actuator or electrical-safety claim)'
