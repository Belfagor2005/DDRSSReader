#!/bin/bash
## setup command=wget -q --no-check-certificate https://raw.githubusercontent.com/Belfagor2005/DDRSSReader/main/installer.sh -O - | /bin/sh

version='0.7'
changelog='\nAdd Sat-universe\nRecode python style'
TMPPATH=/tmp/DDRSSReader-main
FILEPATH=/tmp/ddrssreader.tar.gz

if [ ! -d /usr/lib64 ]; then
    PLUGINPATH=/usr/lib/enigma2/python/Plugins/Extensions/DD_RSS
else
    PLUGINPATH=/usr/lib64/enigma2/python/Plugins/Extensions/DD_RSS
fi

if [ -f /var/lib/dpkg/status ]; then
    STATUS=/var/lib/dpkg/status
    OSTYPE=DreamOs
else
    STATUS=/var/lib/opkg/status
    OSTYPE=Dream
fi

if ! command -v wget >/dev/null; then
    if [ "$OSTYPE" = "DreamOs" ]; then
        apt-get update && apt-get install -y wget || { echo "Failed to install wget"; exit 1; }
    else
        opkg update && opkg install wget || { echo "Failed to install wget"; exit 1; }
    fi
fi

if python --version 2>&1 | grep -q '^Python 3\.'; then
    PYTHON=PY3
    Packagerequests=python3-requests
else
    PYTHON=PY2
    Packagerequests=python-requests
fi

if ! grep -qs "Package: $Packagerequests" "$STATUS"; then
    echo "Installing $Packagerequests..."
    if [ "$OSTYPE" = "DreamOs" ]; then
        apt-get update && apt-get install -y "$Packagerequests" || { echo "Failed to install $Packagerequests"; exit 1; }
    else
        opkg update && opkg install "$Packagerequests" || { echo "Failed to install $Packagerequests"; exit 1; }
    fi
fi

[ -d "$TMPPATH" ] && rm -rf "$TMPPATH"
[ -f "$FILEPATH" ] && rm -f "$FILEPATH"
[ -d "$PLUGINPATH" ] && rm -rf "$PLUGINPATH"

mkdir -p "$TMPPATH" || { echo "Failed to create temp directory"; exit 1; }
cd "$TMPPATH" || exit 1

wget --no-check-certificate 'https://github.com/Belfagor2005/DDRSSReader/archive/refs/heads/main.tar.gz' -O "$FILEPATH" || {
    echo "Download failed"; exit 1;
}

tar -xzf "$FILEPATH" -C /tmp/ || {
    echo "Extraction failed"; exit 1;
}

cp -r /tmp/DDRSSReader-main/usr/ / || {
    echo "Copy failed"; exit 1;
}

if [ ! -d "$PLUGINPATH" ]; then
    echo "Installation failed: $PLUGINPATH missing"
    exit 1
fi

rm -rf "$TMPPATH" "$FILEPATH" /tmp/DDRSSReader-main
sync

box_type=$(head -n 1 /etc/hostname 2>/dev/null || echo "Unknown")
FILE="/etc/image-version"
distro_value=$(grep '^distro=' "$FILE" 2>/dev/null | awk -F '=' '{print $2}')
distro_version=$(grep '^version=' "$FILE" 2>/dev/null | awk -F '=' '{print $2}')
python_vers=$(python --version 2>&1)

echo "#########################################################
#          DDRSSReader $version INSTALLED SUCCESSFULLY      #
#########################################################
BOX MODEL: $box_type
PYTHON: $python_vers
IMAGE: ${distro_value:-Unknown} ${distro_version:-Unknown}"

sleep 3
[ -f /usr/bin/enigma2 ] && killall -9 enigma2 || init 4 && sleep 2 && init 3
exit 0