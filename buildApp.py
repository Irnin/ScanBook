import PyInstaller.__main__
import shutil
import os

if os.path.exists('dist'):
    shutil.rmtree('dist')
if os.path.exists('build'):
    shutil.rmtree('build')

PyInstaller.__main__.run([
    'controller.py',
    '--windowed',
    '--console',
    '--icon=icon.icns',
	'--name=ScanBooks',
	'--onefile'
])