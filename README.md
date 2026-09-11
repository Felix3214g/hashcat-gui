


# Hashcat GUI

A cross-platform graphical interface for Hashcat built with Python and CustomTkinter.

Hashcat GUI provides a cleaner way to use common Hashcat features without having to remember command-line syntax.

## Hashcat GUI v1.4.0
<img width="990" height="847" alt="image" src="https://github.com/user-attachments/assets/b746a305-63ce-47dd-a5ca-d9cc2951cd9b" />


### What's New in v1.4.0

- Added Light, Dark, and System appearance modes
- Added a new appearance selector
- Added customizable color themes
- Improved theme consistency across buttons, switches, and dropdowns
- Added Teal theme
- Fixed default Blue theme restoration
- Improved dropdown appearance and arrow colors
- Added version number to the application title
- Added Windows installer support
- Added macOS Apple Silicon DMG support

## Features

- Clean CustomTkinter interface
- Windows and macOS support
- Light, Dark, and System appearance modes
- Multiple selectable color themes
- Hash file browser
- Wordlist browser
- Hashcat folder selection
- Common hash mode presets
- Manual hash mode configuration
- Automatic synchronization between presets and manual mode input
- Force mode support
- Optimized kernel support
- Start and stop attack controls
- Live Hashcat output
- Automatic result saving
- Configurable output file

## Download

Prebuilt installers are available from the GitHub Releases page.

### Windows

Download:

`HashcatGUI-v1.4.0-windows-x64-setup.exe`

The Windows installer includes the application and can create Start Menu and desktop shortcuts.

### macOS

For Apple Silicon Macs, download:

`HashcatGUI-v1.4.0-macos-arm64.dmg`

> The current builds are not digitally signed or notarized, so Windows SmartScreen or macOS Gatekeeper may display a warning.

## Running From Source

Clone the repository:

```bash
git clone https://github.com/Felix3214g/hashcat-gui.git
cd hashcat-gui
````

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python src/hashcat_GUI.py
```

Hashcat must also be installed on your system.

You can download Hashcat from:

[https://hashcat.net/hashcat/](https://hashcat.net/hashcat/)

## Usage

1. Select your Hashcat folder.
2. Select a hash file.
3. Select a wordlist.
4. Choose a hash mode from the preset dropdown or enter one manually.
5. Configure optional settings such as Force or Optimized Kernel.
6. Choose your preferred color theme and appearance mode.
7. Click **Start Attack**.
8. Results are written to the selected output file.

The default output file is:

```text
cracked_passwords.txt
```

Use **Stop Attack** to terminate a running Hashcat process.

## Supported Hash Presets

The GUI currently includes common presets such as:

* MD5
* SHA1
* SHA256
* SHA512
* NTLM

Other Hashcat modes can be entered manually.

## Project Structure

```text
hashcat-gui/
├── src/
│   └── hashcat_GUI.py
├── installer/
├── requirements.txt
├── build.py
└── README.md
```

## Development

The project is actively being improved.

Bug reports, feature requests, and contributions are welcome through GitHub Issues and Pull Requests.

## Disclaimer

Use Hashcat GUI only with hashes and systems that you own or have explicit permission to test.

## License

MIT License.


