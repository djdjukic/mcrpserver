# -*- mode: python -*-

block_cipher = None

added_files = [
    ('font\*.*', 'font'),
    ('r_values.txt', '.'),
    ('logo.png', '.'),
    ('icon.ico', '.'),
    ('about.gif', '.')
]

a = Analysis(['mcrpserver.py'],
             pathex=['H:\\Dropbox\\Microsemi CRP server\\mcrpserver'],
             binaries=None,
             datas=added_files,
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
          exclude_binaries=True,
          name='mcrpserver',
          icon='icon.ico',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='mcrpserver')
