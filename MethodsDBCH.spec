# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['MethodsDBCH.py'],
    pathex=['AuthWindow.py', 'GlobalAppParams.py', 'MainWindow.py', 'MethodClass.py', 'MethodWindow.py', 'NewValWindow.py', 'RegWindow.py', 'TaskAreaClass.py', 'TheoremClass.py', 'UserClass.py', 'Design_py\\log_wind.py', 'Design_py\\main_wind.py', 'Design_py\\meth_info_wind.py', 'Design_py\\new_val_wind.py', 'Design_py\\reg_wind.py', 'Config.py', 'Dialogs.py', 'Params\\BDConnectParams.prm'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MethodsDBCH',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
