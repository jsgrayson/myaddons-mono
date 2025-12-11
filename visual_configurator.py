import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import threading
import sys
from PIL import Image, ImageDraw
import pystray

CONFIG_FILE = "visual_config.json"

DEFAULT_CONFIG = {
    "regions": {},
    "keybinds": {
        "party1": "f1", "party2": "f2", "party3": "f3", "party4": "f4", "party5": "f5",
        "heal_spell": "1", "dps_spell": "2", "active_mitigation": "3", "execute": "4",
        "defensive_major": "5", "self_heal": "6", "interrupt": "f", "target_cycle": "tab"
    },
    "thresholds": {
        "heal_at": 0.70,
        "critical_at": 0.40
    },
    "reaction_time_min": 0.15,
    "reaction_time_max": 0.25
}

class ConfiguratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SkillWeaver Configurator")
        self.root.geometry("500x700")
        
        # Handle Window Close -> Minimize to Tray
        self.root.protocol('WM_DELETE_WINDOW', self.hide_window)
        
        self.config = self.load_config()
        self.entries = {}
        
        self.create_widgets()
        self.setup_tray()

    def create_icon_image(self):
        # Generate a simple icon
        width = 64
        height = 64
        color1 = "black"
        color2 = "white"
        
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
        dc.rectangle((0, height // 2, width // 2, height), fill=color2)
        
        return image

    def setup_tray(self):
        image = self.create_icon_image()
        menu = pystray.Menu(
            pystray.MenuItem('Open', self.show_window),
            pystray.MenuItem('Quit', self.quit_app)
        )
        self.icon = pystray.Icon("SkillWeaver", image, "SkillWeaver Config", menu)
        
        # Run tray icon in separate thread to not block Tkinter
        threading.Thread(target=self.icon.run, daemon=True).start()

    def hide_window(self):
        self.root.withdraw()
        
    def show_window(self, icon=None, item=None):
        self.root.after(0, self.root.deiconify)

    def quit_app(self, icon=None, item=None):
        self.icon.stop()
        self.root.after(0, self.root.quit)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    # Ensure defaults exist
                    for k, v in DEFAULT_CONFIG["keybinds"].items():
                        if k not in data["keybinds"]:
                            data["keybinds"][k] = v
                    return data
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load config: {e}")
                return DEFAULT_CONFIG
        return DEFAULT_CONFIG

    def create_widgets(self):
        # Main Container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        ttk.Label(main_frame, text="SkillWeaver Settings", font=("Helvetica", 16, "bold")).pack(pady=(0, 20))
        
        # Notebook (Tabs)
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Keybinds
        self.keybind_frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.keybind_frame, text="Keybinds")
        
        # Tab 2: Thresholds & Logic
        self.logic_frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.logic_frame, text="Logic & Thresholds")
        
        # Tab 3: Regions
        self.region_frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.region_frame, text="Regions")

        # Tab 4: Integrations (NEW)
        self.integrations_frame = ttk.Frame(notebook, padding="10")
        notebook.add(self.integrations_frame, text="Integrations")
        
        self.build_keybinds_tab()
        self.build_logic_tab()
        self.build_regions_tab()
        self.build_integrations_tab()
        
        # Save Button
        ttk.Button(main_frame, text="Save Configuration", command=self.save_config).pack(pady=20, fill=tk.X)

    def build_keybinds_tab(self):
        # Group: Party Targeting
        self.create_section(self.keybind_frame, "Party Targeting", [
            ("Party 1", "party1"),
            ("Party 2", "party2"),
            ("Party 3", "party3"),
            ("Party 4", "party4"),
            ("Party 5", "party5"),
        ])
        
        # Group: Combat
        self.create_section(self.keybind_frame, "Combat Actions", [
            ("Heal Spell (Spam)", "heal_spell"),
            ("DPS Spell (Rotation)", "dps_spell"),
            ("Active Mitigation", "active_mitigation"),
            ("Execute / Kill Shot", "execute"),
            ("Major Defensive", "defensive_major"),
            ("Self Heal / Potion", "self_heal"),
            ("Interrupt", "interrupt"),
            ("Target Cycle", "target_cycle"),
        ])

    def build_logic_tab(self):
        # Group: Thresholds
        lbl_frame = ttk.LabelFrame(self.logic_frame, text="Health Thresholds (0.0 - 1.0)", padding="10")
        lbl_frame.pack(fill=tk.X, pady=5)
        
        self.add_entry(lbl_frame, "Heal Ally At", "thresholds.heal_at")
        self.add_entry(lbl_frame, "Critical Health At", "thresholds.critical_at")
        
        # Group: Reaction Time
        lbl_frame2 = ttk.LabelFrame(self.logic_frame, text="Humanizer (Seconds)", padding="10")
        lbl_frame2.pack(fill=tk.X, pady=5)
        
        self.add_entry(lbl_frame2, "Min Reaction Time", "reaction_time_min")
        self.add_entry(lbl_frame2, "Max Reaction Time", "reaction_time_max")

    def build_regions_tab(self):
        # ... (existing code) ...
        for label_text, key in regions:
            self.create_region_row(scrollable_frame, label_text, key)

    def build_integrations_tab(self):
        # WoW Settings
        wow_frame = ttk.LabelFrame(self.integrations_frame, text="World of Warcraft Settings", padding="10")
        wow_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(wow_frame, text="SavedVariables Path:").pack(anchor="w")
        
        path_row = ttk.Frame(wow_frame)
        path_row.pack(fill=tk.X, pady=2)
        
        self.add_entry(path_row, "", "integrations.wow_path")
        ttk.Button(path_row, text="Browse", command=self.browse_wow_path).pack(side=tk.RIGHT, padx=5)
        ttk.Button(path_row, text="Auto-Detect", command=self.auto_detect_wow_path).pack(side=tk.RIGHT, padx=5)
        
        ttk.Label(wow_frame, text="(e.g. .../WTF/Account/NAME/SavedVariables)", font=("Helvetica", 8, "italic")).pack(anchor="w")

        # Discord
        discord_frame = ttk.LabelFrame(self.integrations_frame, text="Discord Integration", padding="10")
        discord_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(discord_frame, text="Webhook URL:").pack(anchor="w")
        self.add_entry(discord_frame, "", "integrations.discord_webhook")
        ttk.Label(discord_frame, text="(Leave empty to disable)", font=("Helvetica", 8, "italic")).pack(anchor="w")

        # Windows iCUE Bridge
        icue_frame = ttk.LabelFrame(self.integrations_frame, text="Windows iCUE Bridge", padding="10")
        icue_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(icue_frame, text="Windows PC IP Address:").pack(anchor="w")
        self.add_entry(icue_frame, "", "integrations.windows_ip")
        ttk.Label(icue_frame, text="(e.g., 192.168.1.50 - Leave empty to disable)", font=("Helvetica", 8, "italic")).pack(anchor="w")

    def browse_wow_path(self):
        from tkinter import filedialog
        path = filedialog.askdirectory(title="Select SavedVariables Directory")
        if path:
            self.update_entry("integrations.wow_path", path)

    def auto_detect_wow_path(self):
        import platform
        system = platform.system()
        candidates = []
        
        if system == "Darwin": # macOS
            candidates = [
                "/Applications/World of Warcraft/_retail_/WTF/Account",
                "/Applications/World of Warcraft/_classic_/WTF/Account"
            ]
        elif system == "Windows":
            candidates = [
                "C:\\Program Files (x86)\\World of Warcraft\\_retail_\\WTF\\Account",
                "C:\\Program Files\\World of Warcraft\\_retail_\\WTF\\Account",
                "D:\\World of Warcraft\\_retail_\\WTF\\Account"
            ]
            
        found_path = None
        
        for base_path in candidates:
            if os.path.exists(base_path):
                # Iterate accounts
                try:
                    for account in os.listdir(base_path):
                        sv_path = os.path.join(base_path, account, "SavedVariables")
                        if os.path.exists(sv_path):
                            # Check for SkillWeaver.lua or just take the first valid one
                            if os.path.exists(os.path.join(sv_path, "SkillWeaver.lua")):
                                found_path = sv_path
                                break
                            # Fallback: just take the first one that exists
                            if not found_path:
                                found_path = sv_path
                    if found_path: break
                except Exception as e:
                    print(f"Error scanning {base_path}: {e}")
                    
        if found_path:
            self.update_entry("integrations.wow_path", found_path)
            messagebox.showinfo("Auto-Detect", f"Found WoW Path:\n{found_path}")
        else:
            messagebox.showwarning("Auto-Detect", "Could not find World of Warcraft installation automatically.\nPlease browse manually.")

    def update_entry(self, key, value):
        entry = self.entries.get(key)
        if entry:
            entry.delete(0, tk.END)
            entry.insert(0, value)

    def create_region_row(self, parent, label_text, key):
        frame = ttk.LabelFrame(parent, text=label_text, padding="5")
        frame.pack(fill=tk.X, pady=5, padx=5)
        
        # Grid layout for Top, Left, Width, Height
        ttk.Label(frame, text="Top:").grid(row=0, column=0, padx=5)
        top_entry = ttk.Entry(frame, width=8)
        top_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(frame, text="Left:").grid(row=0, column=2, padx=5)
        left_entry = ttk.Entry(frame, width=8)
        left_entry.grid(row=0, column=3, padx=5)
        
        ttk.Label(frame, text="W:").grid(row=0, column=4, padx=5)
        w_entry = ttk.Entry(frame, width=6)
        w_entry.grid(row=0, column=5, padx=5)
        
        ttk.Label(frame, text="H:").grid(row=0, column=6, padx=5)
        h_entry = ttk.Entry(frame, width=6)
        h_entry.grid(row=0, column=7, padx=5)
        
        # Select Button
        btn = ttk.Button(frame, text="Select", command=lambda k=key: self.start_selection(k))
        btn.grid(row=0, column=8, padx=10)
        
        # Load values
        r_data = self.config.get("regions", {}).get(key, {})
        top_entry.insert(0, str(r_data.get("top", 0)))
        left_entry.insert(0, str(r_data.get("left", 0)))
        w_entry.insert(0, str(r_data.get("width", 0)))
        h_entry.insert(0, str(r_data.get("height", 0)))
        
        # Store entries
        self.entries[f"regions.{key}.top"] = top_entry
        self.entries[f"regions.{key}.left"] = left_entry
        self.entries[f"regions.{key}.width"] = w_entry
        self.entries[f"regions.{key}.height"] = h_entry

    def start_selection(self, region_key):
        # Hide main window
        self.root.withdraw()
        
        # Create fullscreen overlay
        self.overlay = tk.Toplevel(self.root)
        self.overlay.attributes("-fullscreen", True)
        self.overlay.attributes("-alpha", 0.3) # Semi-transparent
        self.overlay.configure(bg="black")
        self.overlay.lift()
        self.overlay.focus_force()
        
        self.start_x = None
        self.start_y = None
        self.rect_id = None
        
        # Canvas for drawing
        self.canvas = tk.Canvas(self.overlay, cursor="cross", bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", lambda event: self.on_release(event, region_key))
        
        # Escape to cancel
        self.overlay.bind("<Escape>", self.cancel_selection)

    def on_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.rect_id = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red", width=2)

    def on_drag(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.rect_id, self.start_x, self.start_y, cur_x, cur_y)

    def on_release(self, event, region_key):
        end_x, end_y = (event.x, event.y)
        
        # Calculate geometry
        left = min(self.start_x, end_x)
        top = min(self.start_y, end_y)
        width = abs(end_x - self.start_x)
        height = abs(end_y - self.start_y)
        
        # Update entries
        self.entries[f"regions.{region_key}.top"].delete(0, tk.END)
        self.entries[f"regions.{region_key}.top"].insert(0, str(top))
        
        self.entries[f"regions.{region_key}.left"].delete(0, tk.END)
        self.entries[f"regions.{region_key}.left"].insert(0, str(left))
        
        self.entries[f"regions.{region_key}.width"].delete(0, tk.END)
        self.entries[f"regions.{region_key}.width"].insert(0, str(width))
        
        self.entries[f"regions.{region_key}.height"].delete(0, tk.END)
        self.entries[f"regions.{region_key}.height"].insert(0, str(height))
        
        # Close overlay and restore window
        self.overlay.destroy()
        self.root.deiconify()

    def cancel_selection(self, event):
        self.overlay.destroy()
        self.root.deiconify()

    def create_section(self, parent, title, items):
        frame = ttk.LabelFrame(parent, text=title, padding="10")
        frame.pack(fill=tk.X, pady=5)
        
        for label_text, key in items:
            self.add_entry(frame, label_text, f"keybinds.{key}")

    def add_entry(self, parent, label_text, key_path):
        row = ttk.Frame(parent)
        row.pack(fill=tk.X, pady=2)
        
        ttk.Label(row, text=label_text, width=20).pack(side=tk.LEFT)
        
        entry = ttk.Entry(row)
        entry.pack(side=tk.RIGHT, expand=True, fill=tk.X)
        
        # Get value from config
        val = self.get_config_value(key_path)
        entry.insert(0, str(val))
        
        self.entries[key_path] = entry

    def get_config_value(self, path):
        keys = path.split('.')
        val = self.config
        for k in keys:
            val = val.get(k, "")
        return val

    def set_config_value(self, path, value):
        keys = path.split('.')
        target = self.config
        for k in keys[:-1]:
            target = target.setdefault(k, {})
        
        # Type conversion for numbers
        if keys[-1] in ["heal_at", "critical_at", "reaction_time_min", "reaction_time_max"]:
            try:
                target[keys[-1]] = float(value)
            except ValueError:
                pass # Keep as string or ignore if invalid
        # Type conversion for region coords
        elif keys[-1] in ["top", "left", "width", "height"]:
             try:
                target[keys[-1]] = int(value)
             except ValueError:
                pass
        else:
            target[keys[-1]] = value


    def save_config(self):
        # Update config object from entries
        for path, entry in self.entries.items():
            self.set_config_value(path, entry.get())
        
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
            messagebox.showinfo("Success", "Configuration saved successfully!\nRestart visual_weaver.py to apply changes.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    # Set theme if available, otherwise default
    try:
        root.tk.call("source", "azure.tcl") # Optional: Load a theme if you have one
        root.tk.call("set_theme", "dark")
    except:
        pass
        
    app = ConfiguratorApp(root)
    root.mainloop()
