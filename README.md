Hashcat GUI

A graphical interface for Hashcat that removes the complexity of command-line password recovery operations.
Overview
This application provides a streamlined approach to using Hashcat through an intuitive GUI. Built for security professionals who need efficient hash cracking without memorizing syntax.
Key Features

Clean interface using tkinter and customtkinter frameworks
File browser integration for hash files and wordlists
Process management with start/stop controls
Automatic logging and result capture
Hash mode configuration

Setup
Clone the repository:
git clone https://github.com/yourusername/hashcat-gui.git
cd hashcat-gui
Install dependencies:
pip install -r requirements.txt
Ensure Hashcat is installed and available in your system PATH. Download from hashcat.net.
Operation
Launch the application:
python src/hashcat_GUI.py
Select hash file and wordlist using the browse buttons. Enter the appropriate hash mode value (e.g., 0 for MD5). Click "Start Attack" to begin processing. Use "Stop Attack" to terminate early if needed. Results are automatically saved to cracked_passwords.txt.
Development
Contributions accepted through pull requests. Report issues via the GitHub issue tracker.
License
MIT License - see LICENSE file for details.
