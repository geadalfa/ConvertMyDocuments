# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules

datas = [
    ('static', 'static'),
    ('backend', 'backend'),
    ('app_icon.ico', '.')
]
datas += collect_data_files('rapidocr_onnxruntime')
datas += collect_data_files('pymupdf')
datas += collect_data_files('pdf2docx')

hiddenimports = [
    'rapidocr_onnxruntime',
    'pdf2docx',
    'fitz',
    'pymupdf',
    'docx',
    'pikepdf',
    'cv2',
    'PIL',
    'numpy',
    'backend.updater'
]
hiddenimports += collect_submodules('rapidocr_onnxruntime')
hiddenimports += collect_submodules('pdf2docx')

a = Analysis(
    ['server.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ConvertMyDocuments',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['app_icon.ico'],
    uac_admin=False,
    uac_uiaccess=False,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ConvertMyDocuments',
)
