#!/bin/sh

if [ -d /usr/lib/enigma2/python/Plugins/Extensions/DD_RSS ]; then
echo "> removing package please wait..."
sleep 3s 
rm -rf /usr/lib/enigma2/python/Plugins/Extensions/DD_RSS > /dev/null 2>&1

status='/var/lib/opkg/status'
package='enigma2-plugin-extensions-ddrssreader'

if grep -q $package $status; then
opkg remove $package > /dev/null 2>&1
fi
echo "************************"
echo "*   Uninstall DD_RSS   *"
echo "************************"
sleep 3s

#check install deps
# Check python
status='/var/lib/opkg/status'

package='libc6'
if grep -q $package $status; then
rm -rf /run/opkg.lock
opkg install $package > /dev/null 2>&1
fi
package='libgcc1'
if grep -q $package $status; then
rm -rf /run/opkg.lock
opkg install $package > /dev/null 2>&1
fi
package='libstdc++6'
rm -rf /run/opkg.lock
if grep -q $package $status; then
opkg install $package > /dev/null 2>&1
fi

#change version NO. only manualy
plugin=DD_RSS
version=0.4
url=https://github.com/Belfagor2005/DDRSSReader/raw/main/$plugin-$version.tar.gz
package=/var/volatile/tmp/$plugin-$version.tar.gz
#download & install
echo "> Downloading $plugin-$version package  please wait ..."
sleep 3s
wget -O $package --no-check-certificate $url
tar -xf $package -C /
extract=$?
rm -rf $package >/dev/null 2>&1

echo ''
if [ $extract -eq 0 ]; then
echo "> $plugin-$version package installed successfully"
echo "> adapted for py3 & added fhd screens By Lululla"
sleep 3s
else
echo "> $plugin-$version package installation failed"
sleep 3s
fi
fi

exit 0

