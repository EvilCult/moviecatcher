# -*- mode: python -*-

block_cipher = None


a = Analysis(['bl\\app.py'],
             pathex=['C:\\Users\\lwpo2\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages','C:\\Users\\lwpo2\\Downloads\\moviecatcher-master'],
             binaries=None,
             datas=[('Resources\\logo.png', 'RES'), ('Resources\\biticon.ico', 'RES'), ('Resources\\chromedriver.exe', 'RES')],
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
          console=False , icon='Resources\\icon.ico')
