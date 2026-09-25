#!/bin/sh
# Build python3-mediatools_<version>_all.deb
# Usage: packaging/deb/build.sh
set -eu

cd "$(dirname "$0")/../.."
REPO_ROOT="$(pwd)"
VERSION="0.$(git rev-list --count HEAD)"
sed -i "s/^Version: .*/Version: $VERSION/" packaging/deb/control
sed -i "s/^version = .*/version = \"$VERSION\"/" pyproject.toml

PKG_DIR="$REPO_ROOT/debian-pkg"
rm -rf "$PKG_DIR"
mkdir -p "$PKG_DIR/DEBIAN" "$PKG_DIR/usr/lib/python3/dist-packages" \
	"$PKG_DIR/usr/share/doc/python3-mediatools"
cp packaging/deb/control "$PKG_DIR/DEBIAN/control"
cp Media.py Services.py "$PKG_DIR/usr/lib/python3/dist-packages/"
cp GPL-3 "$PKG_DIR/usr/share/doc/python3-mediatools/copyright"
dpkg-deb --build --root-owner-group "$PKG_DIR" "python3-mediatools_${VERSION}_all.deb"
rm -rf "$PKG_DIR"
echo "Built python3-mediatools_${VERSION}_all.deb"
