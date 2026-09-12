#!/bin/bash
set -euo pipefail

VERSION="1.4.1"
APP_NAME="HashcatGUI"
DMG_NAME="HashcatGUI-v${VERSION}-macos-arm64.dmg"
ICON_SOURCE="assets/hashcatgui-icon.png"
ICONSET="assets/hashcatgui.iconset"
ICNS="assets/hashcatgui.icns"

rm -rf build dist dmg-root installer-output "$ICONSET" "$ICNS"
mkdir -p installer-output "$ICONSET"

sips -z 16 16 "$ICON_SOURCE" --out "$ICONSET/icon_16x16.png" >/dev/null
sips -z 32 32 "$ICON_SOURCE" --out "$ICONSET/icon_16x16@2x.png" >/dev/null
sips -z 32 32 "$ICON_SOURCE" --out "$ICONSET/icon_32x32.png" >/dev/null
sips -z 64 64 "$ICON_SOURCE" --out "$ICONSET/icon_32x32@2x.png" >/dev/null
sips -z 128 128 "$ICON_SOURCE" --out "$ICONSET/icon_128x128.png" >/dev/null
sips -z 256 256 "$ICON_SOURCE" --out "$ICONSET/icon_128x128@2x.png" >/dev/null
sips -z 256 256 "$ICON_SOURCE" --out "$ICONSET/icon_256x256.png" >/dev/null
sips -z 512 512 "$ICON_SOURCE" --out "$ICONSET/icon_256x256@2x.png" >/dev/null
sips -z 512 512 "$ICON_SOURCE" --out "$ICONSET/icon_512x512.png" >/dev/null
cp "$ICON_SOURCE" "$ICONSET/icon_512x512@2x.png"
iconutil -c icns "$ICONSET" -o "$ICNS"

python -m PyInstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name "$APP_NAME" \
  --icon "$ICNS" \
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
