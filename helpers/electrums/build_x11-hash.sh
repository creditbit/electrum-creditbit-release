#!/bin/bash
set -xeo pipefail
source build-config.sh
source helpers/build-common.sh

check_vars
## this will be integrated into the main build in a later release
echo "Building x11_hash for Windows"
test -f x11_hash-master.tar.gz || wget https://github.com/mmitech/x11_hash/archive/master.tar.gz
tar -xpzvf x11_hash-master.tar.gz
docker run -ti --rm \
  -e WINEPREFIX="/wine/wine-py2.7.8-32" \
  -v $(pwd)/x11_hash-master:/code \
  -v $(pwd)/helpers:/helpers \
  ogrisel/python-winbuilder wineconsole --backend=curses  Z:\\helpers\\x11_hash-build.bat
cp x11_hash-master/build/lib.win32-2.7/x11_hash.pyd helpers/x11_hash.pyd
