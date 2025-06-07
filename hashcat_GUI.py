import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
import subprocess
import threading
import os

# Set the appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue") # Themes: "blue" (default), "green", "dark-blue"

class HashcatGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Hashcat GUI")
        self.geometry("800x600")

        # --- CONFIGURATION ---
        # IMPORTANT: Set this to the folder where your hashcat.exe is located!
        # Use forward slashes (/) for the path.
        self.hashcat_dir = "C:/Users/felix/Downloads/hashcat-6.2.6/hashcat-6.2.6/"

        self.process = None
        self.hash_file_path = tk.StringVar()
        self.wordlist_file_path = tk.StringVar()
        self.hash_mode = tk.StringVar(value="0") # Default to MD5
        self.output_file = "cracked_passwords.txt" # Name for the results file

        # --- Main Layout ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # --- Input Frame ---
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)

        # Hash File
        ctk.CTkLabel(self.input_frame, text="Hash File:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkEntry(self.input_frame, textvariable=self.hash_file_path, width=400).grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkButton(self.input_frame, text="Browse...", command=self.select_hash_file).grid(row=0, column=2, padx=10, pady=5)

        # Wordlist File
        ctk.CTkLabel(self.input_frame, text="Wordlist:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkEntry(self.input_frame, textvariable=self.wordlist_file_path, width=400).grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkButton(self.input_frame, text="Browse...", command=self.select_wordlist_file).grid(row=1, column=2, padx=10, pady=5)

        # Hash Mode
        ctk.CTkLabel(self.input_frame, text="Hash Mode (-m):").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkEntry(self.input_frame, textvariable=self.hash_mode).grid(row=2, column=1, padx=(10, 0), pady=5, sticky="w")

        # --- Control Frame ---
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.control_frame.grid_columnconfigure((0, 1), weight=1)

        self.start_button = ctk.CTkButton(self.control_frame, text="Start Attack", command=self.start_hashcat_thread)
        self.start_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.stop_button = ctk.CTkButton(self.control_frame, text="Stop Attack", command=self.stop_hashcat, state="disabled")
        self.stop_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # --- Output Text Box ---
        self.output_text = ctk.CTkTextbox(self, state="disabled", wrap="word")
        self.output_text.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")

    def select_hash_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.hash_file_path.set(path)

    def select_wordlist_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.wordlist_file_path.set(path)

    def log(self, message):
        self.output_text.configure(state="normal")
        self.output_text.insert(tk.END, message)
        self.output_text.see(tk.END)
        self.output_text.configure(state="disabled")

    def start_hashcat_thread(self):
        self.hashcat_thread = threading.Thread(target=self.run_hashcat, daemon=True)
        self.hashcat_thread.start()
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")

    def run_hashcat(self):
        hash_file = self.hash_file_path.get()
        wordlist = self.wordlist_file_path.get()
        mode = self.hash_mode.get()

        if not os.path.exists(self.hashcat_dir):
            self.log(f"Error: Hashcat directory not found at '{self.hashcat_dir}'. Please check the path in the script.\n")
            self.process_finished()
            return
            
        if not os.path.exists(hash_file) or not os.path.exists(wordlist):
            self.log("Error: Hash file or wordlist not found.\n")
            self.process_finished()
            return

        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.configure(state="disabled")

        self.log(f"--- Starting Hashcat ---\n")
        self.log(f"Working Directory: {self.hashcat_dir}\n")
        self.log(f"Mode: {mode}, Hash File: {hash_file}, Wordlist: {wordlist}\n")
        self.log(f"Results will be saved to: {os.path.join(self.hashcat_dir, self.output_file)}\n\n")

        try:
            cmd = [
                'hashcat',
                '-m', mode,
                '-a', '0',
                '--force',
                '-o', self.output_file,
                hash_file,
                wordlist
            ]
            
            # THE KEY FIX: Run the command from within hashcat's directory using 'cwd'
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                bufsize=1,
                cwd=self.hashcat_dir  # This makes hashcat find its files (like OpenCL)
            )

            for line in iter(self.process.stdout.readline, ''):
                self.log(line)
            
            self.process.stdout.close()
            self.process.wait()

        except FileNotFoundError:
            self.log("Error: 'hashcat' command not found. Make sure it's in your system's PATH.\n")
        except Exception as e:
            self.log(f"An error occurred: {e}\n")
        
        self.log("\n--- Hashcat process finished ---\n")
        self.show_cracked_passwords()
        self.process_finished()

    def stop_hashcat(self):
        if self.process and self.process.poll() is None:
            self.process.terminate()
            self.log("\n--- Hashcat process terminated by user ---\n")
        self.process_finished()

    def process_finished(self):
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.process = None

    def show_cracked_passwords(self):
        # The output file will be in the hashcat directory because we set 'cwd'
        output_path = os.path.join(self.hashcat_dir, self.output_file)

        self.log(f"\n--- Checking for cracked passwords in {output_path} ---\n")
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
    app = HashcatGUI()
    app.mainloop()