# Hashcat GUI

## V1.1

![Hashcat GUI Interface](https://github.com/user-attachments/assets/00047a06-b102-4b90-b7af-bee12925277a)

## What's New in V1.2

<img width="787" height="673" alt="image" src="https://github.com/user-attachments/assets/a397b30e-a976-4d58-be6f-126ac41045b4" />

- Added hash mode dropdown with common presets
- Added automatic synchronization between dropdown and manual mode input
- Added reverse hash mode mapping
- Added live hash mode updates while typing
- Improved hash mode selection workflow

> **Note:** Windows (.exe) and macOS (.dmg) installer releases are coming soon.

A graphical interface for Hashcat that removes the complexity of command-line password recovery operations.

## Overview

This application provides a streamlined approach to using Hashcat through an intuitive GUI. Built for security professionals who need efficient hash cracking without memorizing syntax.

## Key Features

- Clean interface using tkinter and customtkinter frameworks
- File browser integration for hash files and wordlists
- Hash mode dropdown with automatic synchronization
- Process management with start/stop controls
- Automatic logging and result capture
- Manual hash mode configuration

## Setup

Clone the repository:

```bash
git clone https://github.com/Felix3214g/hashcat-gui.git
cd hashcat-gui
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Ensure Hashcat is installed and available in your system PATH. Download it from **https://hashcat.net**.

## Operation

Launch the application:

```bash
python src/hashcat_GUI.py
```

Select your hash file and wordlist using the browse buttons. Choose a hash mode from the dropdown or manually enter a Hashcat mode number (e.g. `0` for MD5). Click **Start Attack** to begin processing. Use **Stop Attack** to terminate the attack if needed. Results are automatically saved to `cracked_passwords.txt`.

## Development

Contributions are welcome through pull requests. Report bugs or request features via the GitHub issue tracker.

## License

MIT License – see the `LICENSE` file for details.
