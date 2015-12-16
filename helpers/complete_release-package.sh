#!/bin/bash
set -xeo pipefail
source build-config.sh
source helpers/build-common.sh

sign_release () {
         sha1sum ${release} > ${1}.sha1
         md5sum ${release} > ${1}.md5
         gpg --sign --armor --detach  ${1}
         gpg --sign --armor --detach  ${1}.md5
         gpg --sign --armor --detach  ${1}.sha1
}

  mv $(pwd)/helpers/release-packages/* $(pwd)/releases/
  if [ "${TYPE}" = "rc" ]; then export TYPE=SIGNED ; fi
  if [ "${TYPE}" = "SIGNED" ] ; then
    ${DOCKERBIN} push creditbit/electrum-creditbit-winbuild:${VERSION}
    ${DOCKERBIN} push creditbit/electrum-creditbit-release:${VERSION}
#    ${DOCKERBIN} push creditbit/electrum-creditbit32-release:${VERSION}
    ${DOCKERBIN} tag -f ogrisel/python-winbuilder creditbit/python-winbuilder:${VERSION}
    ${DOCKERBIN} push creditbit/python-winbuilder:${VERSION}
    cd releases
    for release in * 
    do
      if [ ! -d ${release} ]; then
         sign_release ${release}
      else
         cd ${release}
         for i in * 
         do 
           if [ ! -d ${i} ]; then
              sign_release ${i}
	   fi
         done
         cd ..
      fi
    done
  fi
  echo "You can find your Encompasss $VERSION binaries in the releases folder."
