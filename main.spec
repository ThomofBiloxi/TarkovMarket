# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(['main.py'],
             pathex=['B:\\Important School and Tax Documents\\TarkovMarketApp'],  # Replace with the path where your python files are located
             binaries=[],
             datas=[('items_db.py', '.'), ('tarkov_market.py', '.')],  # Include the necessary Python files
             hiddenimports=['sys', 'sqlite3', 'os', 'pandas', 'PyQt5.QtWidgets', 'PyQt5.QtCore', 'PyQt5.QtGui'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='Tarkov_Market',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False)
