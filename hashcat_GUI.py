import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import subprocess
import threading
import os
import sys
import logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s')

# Set the appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue") # Themes: "blue" (default), "green", "dark-blue"

class HashcatGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Universal Hashcat GUI")
        self.geometry("800x650") # Increased height for new fields

        # --- CONFIGURATION (Now handled by the GUI) ---
        self.process = None
        self.hashcat_dir = tk.StringVar()
        self.hash_file_path = tk.StringVar()
        self.wordlist_file_path = tk.StringVar()
        self.output_file = tk.StringVar(value="cracked_passwords.txt") # Default output file name
        self.hash_mode = tk.StringVar(value="0") # Default to MD5



        # --- Main Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Input Frame ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)

        # --- NEW: Hashcat Directory ---
        ctk.CTkLabel(self.input_frame, text="Hashcat Folder:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkEntry(self.input_frame, textvariable=self.hashcat_dir, width=400).grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkButton(self.input_frame, text="Browse...", command=self.select_hashcat_dir).grid(row=0, column=2, padx=10, pady=5)

        # Hash File
        ctk.CTkLabel(self.input_frame, text="Hash File:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkEntry(self.input_frame, textvariable=self.hash_file_path, width=400).grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkButton(self.input_frame, text="Browse...", command=self.select_hash_file).grid(row=1, column=2, padx=10, pady=5)

        # Wordlist File
        ctk.CTkLabel(self.input_frame, text="Wordlist:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkEntry(self.input_frame, textvariable=self.wordlist_file_path, width=400).grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkButton(self.input_frame, text="Browse...", command=self.select_wordlist_file).grid(row=2, column=2, padx=10, pady=5)

        # Options Frame (for Hash Mode and Output File)
        self.options_frame = ctk.CTkFrame(self.input_frame)
        self.options_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.options_frame.grid_columnconfigure(1, weight=1)
        self.options_frame.grid_columnconfigure(3, weight=1)



        # Hash Mode
        ctk.CTkLabel(self.options_frame, text="Hash Mode (-m):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkEntry(self.options_frame, textvariable=self.hash_mode, width=80).grid(row=0, column=1, padx=0, pady=5, sticky="w")

        # --- NEW: Output File Name ---
        ctk.CTkLabel(self.options_frame, text="Output File (-o):").grid(row=0, column=2, padx=(20, 10), pady=5, sticky="w")
        ctk.CTkEntry(self.options_frame, textvariable=self.output_file).grid(row=0, column=3, padx=0, pady=5, sticky="ew")


        # --- Control Frame ---
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.control_frame.grid_columnconfigure((0, 1), weight=1)
        self.clear_button = ctk.CTkButton(self.control_frame,text="Clear Output",command=self.clear_output)
        self.clear_button.grid(row=0,column=2,padx=10,pady=10, sticky="ew")

        self.start_button = ctk.CTkButton(self.control_frame, text="Start Attack", command=self.start_hashcat_thread)
        self.start_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.stop_button = ctk.CTkButton(self.control_frame, text="Stop Attack", command=self.stop_hashcat, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # --- Output Text Box ---
        self.output_text = ctk.CTkTextbox(self, state="disabled", wrap="word")
        self.output_text.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")


    def clear_output(self):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0",tk.END)
        self.output_text.configure(state="disabled")

    def select_hashcat_dir(self):
        # Use askdirectory to select a folder
        path = filedialog.askdirectory(title="Select Hashcat Folder")
        if path:
            self.hashcat_dir.set(path)

    def select_hash_file(self):
        path = filedialog.askopenfilename(title="Select Hash File")
        if path:
            self.hash_file_path.set(path)

    def select_wordlist_file(self):
        path = filedialog.askopenfilename(title="Select Wordlist File")
        if path:
            self.wordlist_file_path.set(path)

    def log(self, message):
        """ Safely appends a message to the output textbox from any thread. """
        self.output_text.configure(state="normal")
        self.output_text.insert(tk.END, message)
        self.output_text.see(tk.END)
        self.output_text.configure(state="disabled")

    def start_hashcat_thread(self):
        """ Validates inputs and starts the hashcat process in a separate thread. """
        # --- Input Validation ---
        if not self.hashcat_dir.get():
            self.log("ERROR: Please select the Hashcat folder.\n")
            return
        if not self.hash_file_path.get():
            self.log("ERROR: Please select a hash file.\n")
            return
        if not self.wordlist_file_path.get():
            self.log("ERROR: Please select a wordlist file.\n")
            return

        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

        # Clear previous output
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.configure(state="disabled")

        self.hashcat_thread = threading.Thread(target=self.run_hashcat, daemon=True)
        self.hashcat_thread.start()

    def run_hashcat(self):
        """ Constructs and runs the hashcat command. """
        hashcat_dir = self.hashcat_dir.get()
        hash_file = self.hash_file_path.get()
        wordlist = self.wordlist_file_path.get()
        mode = self.hash_mode.get()
        output_filename = self.output_file.get()

        # Determine the correct executable name based on OS
        if sys.platform == "win32":
            executable_name = "hashcat.exe"
        else: # Linux, macOS, etc.
            executable_name = "hashcat.bin" # Common in portable downloads

        executable_path = os.path.join(hashcat_dir, executable_name)

        if not os.path.exists(executable_path):
            # Fallback for systems where it might just be 'hashcat' (e.g., from a package manager)
            if sys.platform != "win32" and os.path.exists(os.path.join(hashcat_dir, "hashcat")):
                 executable_path = os.path.join(hashcat_dir, "hashcat")
            else:
                self.log(f"Error: Hashcat executable ('{executable_name}') not found in '{hashcat_dir}'.\n")
                self.process_finished()
                return

        self.log(f"--- Starting Hashcat ---\n")
        self.log(f"Executable: {executable_path}\n")
        self.log(f"Mode: {mode}, Hash File: {hash_file}, Wordlist: {wordlist}\n")
        self.log(f"Results will be saved to: {os.path.join(hashcat_dir, output_filename)}\n\n")

        try:
            cmd = [
                executable_path, # Use the full path to the executable
                '-m', mode,
                '-a', '0', # Standard dictionary attack
                '--force', # Useful for running in non-optimal environments like VMs
                '-o', output_filename,
                hash_file,
                wordlist
            ]

            # Run the command from within hashcat directory using 'cwd'
            # This is crucial for hashcat to find its files (e.g., OpenCL kernels)
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, # Redirect stderr to stdout
                text=True,
                encoding='utf-8',
                errors='replace', # Prevents errors from non-UTF8 characters
                bufsize=1,
                cwd=hashcat_dir
            )

            # Read output line by line in real-time
            for line in iter(self.process.stdout.readline, ''):
                self.log(line)

            self.process.stdout.close()
            self.process.wait()

        except Exception as e:
            self.log(f"An unexpected error occurred: {e}\n")

        self.log("\n--- Hashcat process finished ---\n")
        self.show_cracked_passwords()
        self.process_finished()

    def stop_hashcat(self):
        if self.process and self.process.poll() is None:
            self.log("\n--- Terminating Hashcat process... ---\n")
            self.process.terminate() # A more forceful way to stop
            try:
                # Give it a moment to terminate gracefully
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.log("--- Process did not terminate, killing it. ---\n")
                self.process.kill() # The last resort
            self.log("--- Hashcat process stopped by user ---\n")
        self.process_finished()

    def process_finished(self):
        """ Resets the UI buttons to their initial state. """
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.process = None

    def show_cracked_passwords(self):
        """ Reads and displays the contents of the output file. """
        output_path = os.path.join(self.hashcat_dir.get(), self.output_file.get())

        self.log(f"\n--- Checking for results in {output_path} ---\n")
        try:
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                with open(output_path, 'r', encoding='utf-8') as f:
                    cracked = f.read()
                self.log("Cracked Passwords Found:\n")
                self.log("------------------------\n")
                self.log(cracked)
                self.log("------------------------\n")
            else:
                self.log("No passwords were cracked or the output file is empty.\n")
        except Exception as e:
            self.log(f"Could not read the output file: {e}\n")


if __name__ == "__main__":
    try:
        app = HashcatGUI()
        app.mainloop()
    except Exception as e:
        logging.error("An error has occured while running the app",exc_info=True)
else:
    logging.info("HashcatGUI app did not start because this script was imported, not run directly.")