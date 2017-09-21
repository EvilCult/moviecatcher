# -*- mode: python -*-

block_cipher = None


a = Analysis(['Bl/App.py'],
             pathex=['/Users/Ray/Python/MovieSearch'],
             binaries=None,
             datas=[('Resources/logo.png', 'RES'), ('Resources/chromedriver', 'RES')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='Movie Catcher',
          debug=False,
          strip=False,
          upx=True,
          console=True )
app = BUNDLE(exe,
          name='Movie Catcher.app',
          icon='Resources/icon.icns',
          bundle_identifier=None,
          info_plist={
            'NSHighResolutionCapable': 'True'
            },
         )