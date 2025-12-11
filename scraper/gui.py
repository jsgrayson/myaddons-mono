#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import threading
import os

class ScraperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SkillWeaver Scraper Manager")
        self.root.geometry("600x400")
        
        # Header
        header = tk.Label(root, text="SkillWeaver Scraper Manager", 
                         font=("Arial", 16, "bold"), fg="#4af2f8")
        header.pack(pady=10)
        
        # Button Frame
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        
        # Buttons
        self.btn_rotations = tk.Button(btn_frame, text="Update Rotations", 
                                       command=self.run_rotation_scraper,
                                       width=20, height=2, bg="#4CAF50", fg="white")
        self.btn_rotations.grid(row=0, column=0, padx=5)
        
        self.btn_interrupts = tk.Button(btn_frame, text="Update Interrupts", 
                                        command=self.run_interrupt_scraper,
                                        width=20, height=2, bg="#2196F3", fg="white")
        self.btn_interrupts.grid(row=0, column=1, padx=5)
        
        self.btn_all = tk.Button(btn_frame, text="Update All", 
                                command=self.run_all_scrapers,
                                width=20, height=2, bg="#FF9800", fg="white")
        self.btn_all.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Progress Bar
        self.progress = ttk.Progressbar(root, mode='indeterminate')
        self.progress.pack(pady=10, padx=20, fill='x')
        
        # Log Output
        log_label = tk.Label(root, text="Output Log:", font=("Arial", 10, "bold"))
        log_label.pack(anchor='w', padx=20)
        
        self.log_text = scrolledtext.ScrolledText(root, height=15, state='disabled',
                                                  bg="#1e1e1e", fg="#00ff00", 
                                                  font=("Courier", 9))
        self.log_text.pack(pady=5, padx=20, fill='both', expand=True)
        
    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
        
    def run_scraper(self, script_name, label):
        def task():
            self.progress.start()
            self.log(f"Starting {label}...")
            
            try:
                # Get the script directory
                script_dir = os.path.dirname(os.path.abspath(__file__))
                script_path = os.path.join(script_dir, script_name)
                
                # Run scraper
                process = subprocess.Popen(
                    ['python3', script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    cwd=os.path.dirname(script_dir)
                )
                
                # Stream output
                for line in process.stdout:
                    self.log(line.rstrip())
                
                process.wait()
                
                if process.returncode == 0:
                    self.log(f"✓ {label} completed successfully!")
                else:
                    self.log(f"✗ {label} failed with error code {process.returncode}")
                    
            except Exception as e:
                self.log(f"✗ Error: {str(e)}")
            finally:
                self.progress.stop()
                
        thread = threading.Thread(target=task, daemon=True)
        thread.start()
        
    def run_rotation_scraper(self):
        self.run_scraper("scraper.py", "Rotation Scraper")
        
    def run_interrupt_scraper(self):
        self.run_scraper("interrupt_scraper.py", "Interrupt Scraper")
        
    def run_all_scrapers(self):
        def task():
            self.progress.start()
            self.log("Starting ALL scrapers...")
            
            try:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                
                # Run rotations
                self.log("\n=== ROTATIONS ===")
                proc1 = subprocess.run(
                    ['python3', os.path.join(script_dir, 'scraper.py')],
                    capture_output=True, text=True,
                    cwd=os.path.dirname(script_dir)
                )
                self.log(proc1.stdout)
                
                # Run interrupts
                self.log("\n=== INTERRUPTS ===")
                proc2 = subprocess.run(
                    ['python3', os.path.join(script_dir, 'interrupt_scraper.py')],
                    capture_output=True, text=True,
                    cwd=os.path.dirname(script_dir)
                )
                self.log(proc2.stdout)
                
                self.log("\n✓ All scrapers completed! Type /reload in WoW to apply changes.")
                
            except Exception as e:
                self.log(f"✗ Error: {str(e)}")
            finally:
                self.progress.stop()
                
        thread = threading.Thread(target=task, daemon=True)
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = ScraperGUI(root)
    root.mainloop()
