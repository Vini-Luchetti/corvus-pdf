# -*- mode: python ; coding: utf-8 -*-
# CorvusPDF.spec — PyInstaller spec para Corvus PDF V6.0
# Gerado por Corvus Labs / GeralZona

import os

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        (os.path.join('app', 'assets', 'icons', 'corvo_logo.png'),
         os.path.join('app', 'assets', 'icons')),
        (os.path.join('app', 'assets', 'icons', 'corvo_logo.ico'),
         os.path.join('app', 'assets', 'icons')),
    ],
    hiddenimports=[
        'pypdf',
        'pypdf._reader',
        'pypdf._writer',
        'pypdf.filters',
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
    ],
    hookspath=[], hooksconfig={}, runtime_hooks=[],
    excludes=['matplotlib','numpy','pandas','PIL','tkinter','PyQt5','PyQt6'],
    win_no_prefer_redirects=False, win_private_assemblies=False,
    cipher=block_cipher, noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz, a.scripts, a.binaries, a.zipfiles, a.datas, [],
    name='CorvusPDF', debug=False, bootloader_ignore_signals=False,
    strip=False, upx=True, upx_exclude=[], runtime_tmpdir=None,
    console=False, disable_windowed_traceback=False, target_arch=None,
    codesign_identity=None, entitlements_file=None,
    icon=os.path.join('app', 'assets', 'icons', 'corvo_logo.ico'),
)
