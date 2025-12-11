"""
Companion App Dashboard - Visual status for the desktop app
"""
import tkinter as tk
from tkinter import ttk
import threading
import time
from app import CompanionApp # Import the logic we built earlier

class DashboardApp:
    def __init__(self, root, wtf_path):
        self.root = root
        self.root.title("Goblin AI Companion")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Header
        header = tk.Frame(root, bg="#1a1a1a", height=50)
        header.pack(fill="x")
        title = tk.Label(header, text="Goblin AI", fg="#00ff00", bg="#1a1a1a", font=("Helvetica", 16, "bold"))
        title.pack(pady=10)
        
        # Status Area
        self.status_frame = ttk.LabelFrame(root, text="Sync Status")
        self.status_frame.pack(padx=10, pady=10, fill="x")
        
        self.status_label = ttk.Label(self.status_frame, text="Status: Idle", font=("Helvetica", 10))
        self.status_label.pack(pady=5)
        
        self.last_sync_label = ttk.Label(self.status_frame, text="Last Sync: Never", font=("Helvetica", 10))
        self.last_sync_label.pack(pady=5)
        
        # Stats Area
        self.stats_frame = ttk.LabelFrame(root, text="Quick Stats")
        self.stats_frame.pack(padx=10, pady=10, fill="x")
        
        self.gold_label = ttk.Label(self.stats_frame, text="Total Gold: --", font=("Helvetica", 10))
        self.gold_label.pack(pady=5)
        
        # Controls
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        
        self.start_btn = ttk.Button(btn_frame, text="Start Watcher", command=self.start_watcher)
        self.start_btn.pack(side="left", padx=5)
        
        self.stop_btn = ttk.Button(btn_frame, text="Stop", command=self.stop_watcher, state="disabled")
        self.stop_btn.pack(side="left", padx=5)
        
        # Logic
        self.wtf_path = wtf_path
        self.app_logic = CompanionApp(wtf_path)
        self.running = False
        self.thread = None

    def start_watcher(self):
        self.running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status_label.config(text="Status: Watching for changes...", foreground="green")
        
        # Start thread
        self.thread = threading.Thread(target=self._run_logic)
        self.thread.daemon = True
        self.thread.start()

    def stop_watcher(self):
        self.running = False
        self.app_logic.observer.stop()
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_label.config(text="Status: Stopped", foreground="red")

    def _run_logic(self):
        # Override the app's loop to work with our GUI
        self.app_logic.observer.start()
        try:
            while self.running:
                time.sleep(1)
                # Update GUI with mock stats for now (real app would read from logic)
                # self.last_sync_label.config(text=f"Last Sync: {time.strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.app_logic.observer.stop()
            self.app_logic.observer.join()

if __name__ == "__main__":
    WTF_PATH = "/Applications/World of Warcraft/_retail_/WTF/Account/YOUR_ACCOUNT/SavedVariables"
    
    root = tk.Tk()
    app = DashboardApp(root, WTF_PATH)
    root.mainloop()
