# -*- mode: python -*-

import sys
import os
sys.path.insert(0, os.path.join(SPECPATH, 'metatictactoe'))
from const import VERSION

datas = [
    ('metatictactoe/resources', 'resources')
]

block_cipher = None


a = Analysis(['metatictactoe/mtttgui.py'],
             pathex=['./MetaTicTacToe'],
             binaries=[],
             datas=datas,
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
          name=f'metatictactoe-{VERSION}',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
