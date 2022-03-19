# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['main.py'],
             pathex=[],
             binaries=[],
             datas= [],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
a.datas +=[("./src/icon.png", "src/icon.png","DATA"),("./ReadMe.txt", "./src/ReadMe.txt","DATA"),("./grib/go_grib.so", "./grib/go_grib.so","DATA")] 
exe = EXE(pyz,
          a.scripts, 
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='wx2pfpx',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx_exclude=[],
           runtime_tmpdir=None,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon = "src/icon_file.ico" )



