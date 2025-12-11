Module: "The Mirror" - Hardware-Aware Configuration Sync

1. Executive Summary

This module solves the "Cross-Platform" problem of playing World of Warcraft on multiple devices with different input methods (e.g., Desktop Keyboard vs. Steam Deck Controller).

It enables Device-Specific Profiles for Keybinds, Macros, and CVars that automatically load based on which physical machine launches the game.

2. Feature Specification

2.1 Device Recognition

Automatic Detection: The system identifies the device by its OS Hostname (e.g., DESKTOP-MAIN vs. STEAMDECK-01).

Context Switching: When the Bridge Script launches on a Handheld, it flags the session as MODE: HANDHELD.

2.2 The "Virtual Binding" System

Instead of a single bindings-cache.wtf, the Server stores multiple versions per character:

Profile A (Desktop): Standard Mouse/Keyboard binds (1 through =, Shift modifiers).

Profile B (Handheld): Controller-specific binds (ConsolePort settings, target scan macros).

2.3 Config Variable (CVar) Sync

Syncs graphics and interface settings that must differ between devices.

Desktop: 4K resolution, UI Scale 0.64, Max Graphics.

Handheld: 800p resolution, UI Scale 1.0, "Liquid Detail: Low" (for battery life).

2.4 Macro Virtualization

Automatically swaps macro text based on input method.

Desktop Macro: /cast [@cursor] Blizzard (Fast mouse aiming).

Handheld Macro: /cast [@player] Blizzard (Auto-cast at feet for controller ease).

3. Implementation Plan

Phase 1: Database Schema Update

We need to register your devices and link profiles to them.

SQL (Run on R720):

-- 1. REGISTER DEVICES
CREATE TABLE trusted_devices (
    device_id SERIAL PRIMARY KEY,
    hostname VARCHAR(100) UNIQUE NOT NULL, -- e.g. "STEAMDECK"
    device_type VARCHAR(20) DEFAULT 'DESKTOP', -- 'DESKTOP', 'HANDHELD', 'LAPTOP'
    description VARCHAR(100)
);

-- 2. STORE PROFILES
CREATE TABLE config_profiles (
    profile_id SERIAL PRIMARY KEY,
    character_guid VARCHAR(50), -- 'GLOBAL' for account-wide
    device_type VARCHAR(20), -- Matches trusted_devices.device_type
    file_type VARCHAR(50), -- 'BINDINGS', 'MACROS', 'CONFIG'
    file_content TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. SEED DATA (Example)
INSERT INTO trusted_devices (hostname, device_type) VALUES ('DESKTOP-PC', 'DESKTOP');
INSERT INTO trusted_devices (hostname, device_type) VALUES ('STEAMDECK', 'HANDHELD');


Phase 2: The Bridge Script Update (bridge.py)

We modify the Python script running on your PC/Handheld to declare its identity.

Updated Logic:

Startup: bridge.py gets socket.gethostname().

Handshake: Sends GET /api/device_check?hostname=[NAME] to R720.

Server Response: "You are a HANDHELD."

Download: Bridge requests GET /api/config/macros?type=HANDHELD.

Overwrite: Bridge replaces WTF/.../macros-cache.txt before WoW launches (or while closed).

Phase 3: The Server Logic (Python)

Add these endpoints to your Flask server.py.

@app.route('/api/config/sync', methods=['GET'])
def sync_config():
    hostname = request.args.get('hostname')
    char_guid = request.args.get('guid')
    
    # 1. Lookup Device Type
    device_type = db.query("SELECT device_type FROM trusted_devices WHERE hostname = %s", (hostname,))
    
    # 2. Fetch specific profile for this device type
    config_data = db.query("""
        SELECT file_content FROM config_profiles 
        WHERE character_guid = %s AND device_type = %s
    """, (char_guid, device_type))
    
    return jsonify({"config": config_data})


Phase 4: "Safe Mode" Backup

Since overwriting config files is risky, the Bridge script must create a local backup before every sync.

Location: WTF/Backups/[YYYY-MM-DD]_bindings.bak

Retention: Keep last 5 backups.

4. User Experience Walkthrough

Scenario: Switching from Desktop to Steam Deck.

On Desktop: You change a keybind (F to Interrupt). You log out.

Bridge (Desktop): Detects change. Uploads file to Server tagged as DESKTOP profile.

On Deck: You turn it on. bridge.py runs on boot.

Bridge (Deck): Checks Server.

Server: "I have a new Desktop profile, but you are Handheld. Do NOT sync the keybinds. DO sync the shared Macros."

Result: Your specific controller binds remain untouched, but your new Macro logic updates automatically.