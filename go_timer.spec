# -*- mode: python -*-

import pathlib

block_cipher = None

a = Analysis(['go_timer.py'],
             pathex=['C:\\Users\\csm10495\\Desktop\\GoTimer'],
             binaries=[],
             datas=[
                 (pathlib.Path('listener') / 'gamestate_integration_go_timer.cfg', './listener/',)
             ],
             hiddenimports=[],
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
          name='go_timer',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
