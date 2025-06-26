import PyInstaller.__main__
import os


script_dir = os.path.dirname(os.path.abspath(__file__))

PyInstaller.__main__.run([
    os.path.join(script_dir, 'hashcat_GUI.py'),
    '--onefile',
    '--windowed',
    '--name', 'HashcatGUI',
    
])
