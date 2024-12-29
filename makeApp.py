import PyInstaller.__main__

PyInstaller.__main__.run([
	'controller.py',
	'--windowed',
	#'--noconsole',
	'--icon=icon.icns'
])