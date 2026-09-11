#!/bin/bash
set -euo pipefail

VERSION="1.4.0"
APP_NAME="HashcatGUI"
DMG_NAME="HashcatGUI-v${VERSION}-macos-arm64.dmg"

rm -rf build dist dmg-root installer-output
mkdir -p installer-output

python -m PyInstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name "$APP_NAME" \
  src/hashcat_GUI.py

mkdir -p dmg-root
cp -R "dist/${APP_NAME}.app" dmg-root/
ln -s /Applications dmg-root/Applications

hdiutil create \
  -volname "Hashcat GUI ${VERSION}" \
  -srcfolder dmg-root \
  -ov \
  -format UDZO \
  "installer-output/${DMG_NAME}"

echo "Created installer-output/${DMG_NAME}"
