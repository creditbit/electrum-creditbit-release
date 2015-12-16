# -*- mode: python -*-

# We don't put these files in to actually include them in the script but to make the Analysis method scan them for imports
a = Analysis(['electrum-creditbit', 'gui/qt/main_window.py', 'gui/qt/lite_window.py', 'gui/text.py',
              'lib/util.py', 'lib/wallet.py', 'lib/simple_config.py','gui/gtk.py',
              'lib/bitcoin.py','lib/interface.py', 'packages/trezorctl.py',
              ],
             hiddenimports=["PyQt4","lib","gui","plugins","trezorlib","hid"],
             pathex=['lib','gui','plugins','packages'],
             hookspath=None)

##### include mydir in distribution #######
def extra_datas(mydir):
    def rec_glob(p, files):
        import os
        import glob
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            rec_glob("%s/*" % d, files)
    files = []
    rec_glob("%s/*" % mydir, files)
    extra_datas = []
    for f in files:
        extra_datas.append((f, f, 'DATA'))

    return extra_datas
###########################################

# append dirs

# Theme data
a.datas += extra_datas('data')

# Localization
a.datas += extra_datas('locale')

# Py folders that are needed because of the magic import finding
a.datas += extra_datas('gui')
a.datas += extra_datas('lib')
a.datas += extra_datas('plugins')
a.datas += [ ('packages/requests/cacert.pem', 'packages/requests/cacert.pem', 'DATA') ]
a.datas += [ ('packages/trezorctl.py', 'packages/trezorctl.py', 'DATA') ]

# Dependencies
a.datas += extra_datas('packages')

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.datas,
          name=os.path.join('build/electrum-creditbit/electrum-creditbit', 'electrum-creditbit_osx.bin'),
          debug=True,
          strip=None,
          upx=False,
          icon='icons/electrum-creditbit.ico',
          console=True)
          # The console True makes an annoying black box pop up, but it does make electrum-creditbit output command line commands, with this turned off no output will be given but commands can still be used

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               debug=True,
               icon='icons/electrum-creditbit.ico',
               console=True,
               name=os.path.join('dist', 'electrum-creditbit'))

app = BUNDLE(coll,
        name=os.path.join('dist', 'Encompass.app'),
        appname="Encompass",
	 icon='electrum-creditbit.icns',
        version = 'ELECTRUM_VERSION'
        )
