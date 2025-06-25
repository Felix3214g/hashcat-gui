import PyInstaller.__main__
import os

# Get the absolute path to the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    os.path.join(script_dir, 'hashcat_GUI.py'),
    '--onefile',
    '--windowed',
    '--name', 'HashcatGUI',
    # You can specify an icon file here
    # '--icon', os.path.join(script_dir, 'icon.ico'),
])
