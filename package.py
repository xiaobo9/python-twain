import PyInstaller.__main__

PyInstaller.__main__.run([
    '--noconfirm',
    # '-w',
    '--add-data=resources;resources',
    '--hidden-import=tk_geometry',
    '--icon=resources/favicon.ico',
    'twain_scanner.py',
])
