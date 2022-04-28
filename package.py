import PyInstaller.__main__

PyInstaller.__main__.run([
    '--noconfirm',
    '-w',
    '--add-data=extras;extras',
    '--add-data=scanner/resources;scanner/resources',
    '--hidden-import=tk_geometry',
    '--icon=scanner/resources/favicon.ico',
    'scanner/main.py',
])
