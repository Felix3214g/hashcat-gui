import tkinter as tk
from idlelib.configdialog import changes
from tkinter import filedialog, OptionMenu
import customtkinter as ctk
import subprocess
import threading
import os
import sys
import logging

from customtkinter import CTkEntry
from customtkinter.windows.widgets.core_widget_classes import dropdown_menu

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s')

# Set the appearance mode and default color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class HashcatGUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Hashcat GUI")
        self.geometry("800x650")  # Increased height for new fields

        self.process = None
        self.hashcat_dir = tk.StringVar()
        self.hash_file_path = tk.StringVar()
        self.wordlist_file_path = tk.StringVar()
        self.output_file = tk.StringVar(value="cracked_passwords.txt")  # Default output file name
        self.hash_mode = tk.StringVar(value="0")  # Uses MD5 as default

        # Main layout
        self.status_label = ctk.CTkLabel(self, text="Status: Idle")
        self.status_label.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # Frame for the input
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.input_frame.grid_columnconfigure(1, weight=1)

        # select the hash cat directory
        ctk.CTkLabel(self.input_frame, text="Hashcat Folder:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkEntry(self.input_frame, textvariable=self.hashcat_dir, width=400).grid(row=0, column=1, padx=10, pady=5,
                                                                                      sticky="ew")
        ctk.CTkButton(self.input_frame, text="Browse...", command=self.select_hashcat_dir).grid(row=0, column=2,
                                                                                                padx=10, pady=5)

        # Hash File
        ctk.CTkLabel(self.input_frame, text="Hash File:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkEntry(self.input_frame, textvariable=self.hash_file_path, width=400).grid(row=1, column=1, padx=10,
                                                                                         pady=5, sticky="ew")
        ctk.CTkButton(self.input_frame, text="Browse...", command=self.select_hash_file).grid(row=1, column=2, padx=10,
                                                                                              pady=5)

        # Wordlist File
        ctk.CTkLabel(self.input_frame, text="Wordlist:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        ctk.CTkEntry(self.input_frame, textvariable=self.wordlist_file_path, width=400).grid(row=2, column=1, padx=10,
                                                                                             pady=5, sticky="ew")
        ctk.CTkButton(self.input_frame, text="Browse...", command=self.select_wordlist_file).grid(row=2, column=2,
                                                                                                  padx=10, pady=5)

        # Options Frame (for Hash Mode and Output File)
        self.options_frame = ctk.CTkFrame(self.input_frame)
        self.options_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="ew")
        self.options_frame.grid_columnconfigure(1, weight=1)
        self.options_frame.grid_columnconfigure(3, weight=1)


        self.hash_presets = {
            "MD5": "0",
            "SHA1": "100",
            "SHA256": "1400",
            "SHA512": "1700",
            "NTLM": "1000"

        }
        self.reverse_hash_presets = {
            "0": "MD5",
            "100": "SHA1",
            "1400": "SHA256",
            "1700": "SHA512",
            "1000": "NTLM"
        }

        self.dropdown = ctk.CTkOptionMenu(
            self.options_frame,
            values=list(self.hash_presets.keys()),
            command = self.change_choice
        )


        self.dropdown.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.get_mode()
        self.hash_mode.trace_add("write", self.get_mode)

        # Hash Mode
        ctk.CTkLabel(self.options_frame, text="Hash Mode (-m):").grid(row=0, column=1, padx=10, pady=5, sticky="w")
        CTkEntry(self.options_frame, textvariable=self.hash_mode, width=80).grid(row=0, column=1, padx=0, pady=5,
                                                                                     sticky="w")

        # Output filename
        ctk.CTkLabel(self.options_frame, text="Output File (-o):").grid(row=0, column=2, padx=(20, 10), pady=5,
                                                                        sticky="w")
        ctk.CTkEntry(self.options_frame, textvariable=self.output_file).grid(row=0, column=3, padx=0, pady=5,
                                                                             sticky="ew")

        # Control frame
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")
        self.control_frame.grid_columnconfigure((0, 1), weight=1)
        self.clear_button = ctk.CTkButton(self.control_frame, text="Clear Output", command=self.clear_output)
        self.clear_button.grid(row=0, column=2, padx=10, pady=10, sticky="ew")

        self.start_button = ctk.CTkButton(self.control_frame, text="Start Attack", command=self.start_hashcat_thread)
        self.start_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.stop_button = ctk.CTkButton(self.control_frame, text="Stop Attack", command=self.stop_hashcat,
                                         state="disabled")
        self.stop_button.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Output box
        self.output_text = ctk.CTkTextbox(self, state="disabled", wrap="word")
        self.output_text.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="nsew")


    def change_choice(self,mode):
        mode = self.dropdown.get()
        choice = self.hash_presets[mode]
        self.hash_mode.set(choice)


    def get_mode(self, *args):
        current_mode = self.hash_mode.get()
        if current_mode == "0":
            self.dropdown.set(self.reverse_hash_presets["0"])
        elif current_mode == "100":
             self.dropdown.set(self.reverse_hash_presets["100"])

        elif current_mode == "1400":
             self.dropdown.set(self.reverse_hash_presets["1400"])

        elif current_mode == "1700":
             self.dropdown.set(self.reverse_hash_presets["1700"])



    def clear_output(self):
        self.output_text.configure(state="normal")
        self.output_text.delete("1.0", tk.END)
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

        self.output_text.configure(state="normal")
        self.output_text.insert(tk.END, message)
        self.output_text.see(tk.END)
        self.output_text.configure(state="disabled")

    def start_hashcat_thread(self):

        # Validates inputs
        hashcat_dir = self.hashcat_dir.get()
        hash_file = self.hash_file_path.get()
        wordlist = self.wordlist_file_path.get()

        if not hashcat_dir or not os.path.isdir(hashcat_dir):
            self.log("ERROR: Please select a valid Hashcat directory.\n")
            self.status_label.configure(text="Status: Error",text_color="red")
            return
        if not hash_file or not os.path.isfile(hash_file):
            self.log("ERROR: Please select a valid hash file.\n")
            self.status_label.configure(text="Status: Error",text_color="red")
            return
        if not wordlist or not os.path.isfile(wordlist):
            self.log("ERROR: Please select a valid wordlist file.\n")
            self.status_label.configure(text="Status: Error",text_color="red")
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
        # creates the hashcat command
        hashcat_dir = self.hashcat_dir.get()
        hash_file = self.hash_file_path.get()
        wordlist = self.wordlist_file_path.get()
        mode = self.hash_mode.get()
        output_filename = self.output_file.get()


        # Chooses the correct executable name for the right operating system
        if sys.platform == "win32":
            executable_name = "hashcat.exe"
        else:  # Linux, macOS, etc
            executable_name = "hashcat.bin"

        executable_path = os.path.join(hashcat_dir, executable_name)

        if not os.path.exists(executable_path):
            # Fallback for systems where it might just be hashcat
            if sys.platform != "win32" and os.path.exists(os.path.join(hashcat_dir, "hashcat")):
                executable_path = os.path.join(hashcat_dir, "hashcat")
            else:

                self.log(f"Error: Hashcat executable ('{executable_name}') not found in '{hashcat_dir}'.\n")
                self.status_label.configure(text="Status: Error",text_color="red")
                self.process_finished()

                return

        self.log(f"--- Starting Hashcat ---\n")
        self.status_label.configure(text="Status: Running",text_color="orange")
        self.log(f"Executable: {executable_path}\n")
        self.log(f"Mode: {mode}, Hash File: {hash_file}, Wordlist: {wordlist}\n")
        self.log(f"Results will be saved to: {os.path.join(hashcat_dir, output_filename)}\n\n")


        try:
            cmd = [
                executable_path,  # Use the full path to the executable
                '-m', mode,
                '-a', '0',  # Standard dictionary attack
                '--force',
                '-o', output_filename,
                hash_file,
                wordlist
            ]



            # Run the command from within hashcat directory using cwd
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',
                bufsize=1,
                cwd=hashcat_dir
            )

            # Read output line by line in real-time
            for line in iter(self.process.stdout.readline, ''):
                self.log(line)

            self.process.stdout.close()
            return_code = self.process.wait()
            if return_code != 0:
                self.log(f"\n--- Hashcat process exited with error code: {return_code} ---\n")
                self.status_label.configure(text="Status: Error",text_color="red")
                self.process_finished()
                return

        # Error handling for a file not found error
        except FileNotFoundError:
            self.log(f"ERROR: Could not find the hashcat executable at '{executable_path}'.\n"

                     f"Please ensure the path is correct and the file has execute permissions.\n")
            self.status_label.configure(text="Status: Error",text_color="red")
            self.process_finished()


        except Exception as e:
            self.log(f"An unexpected error occurred while trying to run hashcat: {e}\n")
            self.status_label.configure(text="Status: Error",text_color="red")
            self.process_finished()
            return

        self.log("\n--- Hashcat process finished ---\n")
        self.status_label.configure(text="Status: Finished",text_color="green")
        self.show_cracked_passwords()
        self.process_finished()

    def stop_hashcat(self):
        if self.process and self.process.poll() is None:
            self.log("\n--- Terminating Hashcat process... ---\n")
            self.process.terminate()  # A more forceful way to stop

            try:
                # Terminates the process gracefully
                self.process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.log("--- Process did not terminate, killing it. ---\n")
                self.process.kill()  # last resort
            self.log("--- Hashcat process stopped by user ---\n")
            self.status_label.configure(text="Status: Stopped",text_color= None)
        self.process_finished()

    def process_finished(self):
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.process = None

    def show_cracked_passwords(self):

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
        logging.error("An error has occurred while running the app", exc_info=True)
else:
    logging.info("HashcatGUI app did not start because this script was imported, not run directly.")