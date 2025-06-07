# Hashcat GUI

Hashcat GUI is a graphical user interface for Hashcat, a powerful password recovery tool. This application simplifies the process of using Hashcat by providing an intuitive interface for selecting hash files, wordlists, and configuring hash modes.

## Features

- User-friendly interface built with `tkinter` and `customtkinter`.
- Easy selection of hash files and wordlists.
- Ability to start and stop Hashcat processes.
- Logs output and displays cracked passwords.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/hashcat-gui.git
   cd hashcat-gui
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Ensure that Hashcat is installed and accessible in your system's PATH. You can download it from [Hashcat's official website](https://hashcat.net/hashcat/).

## Usage

1. Run the application:
   ```
   python src/hashcat_GUI.py
   ```

2. Use the "Browse..." buttons to select your hash file and wordlist.

3. Enter the hash mode (e.g., `0` for MD5) in the provided field.

4. Click "Start Attack" to begin the cracking process. You can stop the process at any time by clicking "Stop Attack".

5. The results will be saved to `cracked_passwords.txt` in the Hashcat directory.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any bugs or feature requests.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.