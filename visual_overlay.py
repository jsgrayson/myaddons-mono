from flask import Flask, jsonify, render_template_string
import threading
import logging
import time

# Suppress Flask logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class WebHUD:
    def __init__(self):
        self.app = Flask(__name__)
        self.state = {
            "status": "STARTING",
            "role": "DPS",
            "action": "Waiting...",
            "toggles": "Initializing..."
        }
        self.running = False
        self.thread = None
        self.command_queue = []

        # Define Routes
        @self.app.route('/')
        def index():
            return render_template_string(self.HTML_TEMPLATE)

        @self.app.route('/status')
        def get_status():
            return jsonify(self.state)
            
        @self.app.route('/dashboard')
        def dashboard():
            return render_template_string(self.DASHBOARD_TEMPLATE)
            
        @self.app.route('/cmd/<cmd_name>')
        def receive_command(cmd_name):
            self.command_queue.append(cmd_name)
            return jsonify({"status": "ok", "cmd": cmd_name})

        @self.app.route('/status/simple')
        def get_simple_status():
            # Returns just the status text for Stream Deck "Title" updaters
            return self.state["status"]

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()
        print("\n[Stealth HUD] Running at http://localhost:5001")
        print("[Stealth HUD] Open this on your phone or second monitor!\n")

    def stop(self):
        self.running = False
        # Flask doesn't have a clean stop without a complex setup, 
        # but daemon thread will die with main process.
        pass

    def update(self, status=None, role=None, action=None, toggles=None):
        if status: self.state["status"] = status
        if role: self.state["role"] = role
        if action: self.state["action"] = action
        if toggles: self.state["toggles"] = toggles
        
    def get_command(self):
        if self.command_queue:
            return self.command_queue.pop(0)
        return None

    def _run_server(self):
        try:
            self.app.run(host='0.0.0.0', port=5003, debug=False, use_reloader=False)
        except Exception as e:
            print(f"Failed to start Web HUD: {e}")

    # --- TEMPLATES ---

    # 1. SkillWeaver HUD (Touch Optimized)
    HTML_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>SkillWeaver Touch</title>
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
        <style>
            body { 
                background-color: #000; color: #fff; font-family: 'Segoe UI', sans-serif; 
                margin: 0; padding: 10px; height: 100vh; display: flex; flex-direction: column;
                overflow: hidden;
            }
            .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
            .status-box { 
                background: #222; padding: 10px 20px; border-radius: 8px; 
                font-size: 24px; font-weight: bold; text-align: center; flex-grow: 1; margin-right: 10px;
            }
            .role-box {
                background: #222; padding: 10px 20px; border-radius: 8px;
                font-size: 24px; font-weight: bold; color: #00ffff;
            }
            .running { color: #00ff00; border: 2px solid #00ff00; }
            .paused { color: #ff0000; border: 2px solid #ff0000; }
            .action-display {
                font-size: 18px; color: #ffff00; text-align: center; margin-bottom: 15px;
                background: #111; padding: 5px; border-radius: 4px;
            }
            .grid-container {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                grid-template-rows: 1fr 1fr;
                gap: 10px;
                flex-grow: 1;
            }
            button {
                background: #333; color: white; border: none; border-radius: 12px;
                font-size: 20px; font-weight: bold; cursor: pointer;
                display: flex; flex-direction: column; justify-content: center; align-items: center;
                transition: background 0.1s, transform 0.1s;
                touch-action: manipulation;
            }
            button:active { transform: scale(0.95); background: #555; }
            .btn-pause { grid-column: 1 / span 2; grid-row: 1 / span 2; background: #442222; font-size: 32px; }
            .btn-role { background: #224455; }
            .btn-int { background: #554422; }
            .btn-cycle { background: #225522; }
            .btn-surv { background: #442255; }
            .icon { font-size: 32px; margin-bottom: 5px; }
            .nav-bar { margin-top: 10px; display: flex; justify-content: center; }
            .nav-btn { background: #111; padding: 10px 20px; border-radius: 20px; text-decoration: none; color: #888; font-size: 14px; }
        </style>
        <script>
            function updateStatus() {
                fetch('/status')
                    .then(response => {
                        if (!response.ok) throw new Error('Network response was not ok');
                        return response.json();
                    })
                    .then(data => {
                        document.getElementById('connection').style.backgroundColor = '#00ff00';
                        document.getElementById('status').innerText = data.status;
                        document.getElementById('status').className = 'status-box ' + (data.status === 'RUNNING' ? 'running' : 'paused');
                        document.getElementById('role').innerText = data.role;
                        document.getElementById('action').innerText = "Last: " + data.action;
                    })
                    .catch(error => {
                        document.getElementById('connection').style.backgroundColor = '#ff0000';
                        document.getElementById('status').innerText = "DISCONNECTED";
                        document.getElementById('status').className = 'status-box paused';
                    });
            }
            function sendCmd(cmd) {
                fetch('/cmd/' + cmd).catch(e => console.error(e));
                if (window.navigator && window.navigator.vibrate) window.navigator.vibrate(50);
            }
            setInterval(updateStatus, 500);
        </script>
    </head>
    <body>
        <div class="header">
            <div id="connection" style="width: 15px; height: 15px; border-radius: 50%; background-color: #ff0000; margin-right: 10px; border: 1px solid #555;"></div>
            <div id="status" class="status-box running">STARTING</div>
            <div id="role" class="role-box">DPS</div>
        </div>
        <div id="action" class="action-display">Waiting...</div>
        <div class="grid-container">
            <button class="btn-pause" onclick="sendCmd('pause')"><span class="icon">⏯</span><span>PAUSE</span></button>
            <button class="btn-role" onclick="sendCmd('role')"><span class="icon">🔄</span><span>ROLE</span></button>
            <button class="btn-int" onclick="sendCmd('interrupt')"><span class="icon">⚡</span><span>KICK</span></button>
            <button class="btn-cycle" onclick="sendCmd('cycle')"><span class="icon">🎯</span><span>TAB</span></button>
            <button class="btn-surv" onclick="sendCmd('survival')"><span class="icon">🛡</span><span>SURV</span></button>
        </div>
        <div class="nav-bar">
            <a href="/dashboard" class="nav-btn">🏠 Home</a>
        </div>
    </body>
    </html>
    """

    # 2. Goblin Dashboard (Unified Launcher)
    DASHBOARD_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Goblin OS</title>
        <meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no">
        <style>
            body { 
                background-color: #050505; color: #fff; font-family: 'Segoe UI', sans-serif; 
                margin: 0; padding: 20px; height: 100vh; display: flex; flex-direction: column;
                overflow: hidden;
            }
            h1 { text-align: center; color: #00ff99; margin-bottom: 30px; font-size: 28px; text-transform: uppercase; letter-spacing: 2px; }
            
            .app-grid {
                display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 30px;
            }
            
            .app-card {
                background: #111; border: 1px solid #333; border-radius: 15px;
                height: 120px; display: flex; flex-direction: column; justify-content: center; align-items: center;
                text-decoration: none; color: white; transition: all 0.2s;
            }
            .app-card:active { transform: scale(0.95); background: #222; }
            
            .app-icon { font-size: 40px; margin-bottom: 10px; }
            .app-name { font-size: 18px; font-weight: bold; }
            .app-status { font-size: 12px; color: #666; margin-top: 5px; }
            
            .skillweaver { border-color: #00ffff; box-shadow: 0 0 10px rgba(0, 255, 255, 0.2); }
            .holocron { border-color: #ffaa00; box-shadow: 0 0 10px rgba(255, 170, 0, 0.2); }
            .petweaver { border-color: #00ff00; box-shadow: 0 0 10px rgba(0, 255, 0, 0.2); }
            .diplomat { border-color: #ff55ff; box-shadow: 0 0 10px rgba(255, 85, 255, 0.2); }
            .mirror { border-color: #aaaaaa; box-shadow: 0 0 10px rgba(170, 170, 170, 0.2); }
            .ledger { border-color: #ffd700; box-shadow: 0 0 10px rgba(255, 215, 0, 0.2); }
            
            .chat-container {
                flex-grow: 1; background: #111; border-radius: 15px; border: 1px solid #333;
                display: flex; flex-direction: column; overflow: hidden;
            }
            .chat-history {
                flex-grow: 1; padding: 15px; overflow-y: auto; font-size: 14px; color: #ddd;
            }
            .chat-input-area {
                display: flex; padding: 10px; background: #0a0a0a; border-top: 1px solid #333;
            }
            input {
                flex-grow: 1; background: #222; border: none; color: white; padding: 10px; border-radius: 8px;
                font-size: 16px; outline: none;
            }
            .send-btn {
                background: #00ff99; color: black; border: none; padding: 0 20px; margin-left: 10px;
                border-radius: 8px; font-weight: bold; cursor: pointer;
            }
            
            .msg-user { color: #00ffff; margin-bottom: 5px; }
            .msg-ai { color: #00ff99; margin-bottom: 10px; }
        </style>
        <script>
            async function sendMessage() {
                const input = document.getElementById('chatInput');
                const text = input.value;
                if (!text) return;
                
                const history = document.getElementById('chatHistory');
                history.innerHTML += `<div class="msg-user">You: ${text}</div>`;
                input.value = '';
                
                // Mock AI Response for now
                setTimeout(() => {
                    let response = "I'm listening, boss. (Backend integration pending)";
                    if (text.toLowerCase().includes("status")) response = "All systems operational.";
                    history.innerHTML += `<div class="msg-ai">Goblin Brain: ${response}</div>`;
                    history.scrollTop = history.scrollHeight;
                }, 500);
            }
        </script>
    </head>
    <body>
        <h1>Goblin OS v1.0</h1>
        
        <div class="app-grid">
            <a href="/" class="app-card skillweaver">
                <div class="app-icon">⚔️</div>
                <div class="app-name">SkillWeaver</div>
                <div class="app-status">Combat Bot</div>
            </a>
            <a href="http://localhost:5001" class="app-card holocron" target="_blank">
                <div class="app-icon">📜</div>
                <div class="app-name">Holocron</div>
                <div class="app-status">ERP System</div>
            </a>
            <a href="http://localhost:5002" class="app-card petweaver" target="_blank">
                <div class="app-icon">🐾</div>
                <div class="app-name">PetWeaver</div>
                <div class="app-status">Battle Bot</div>
            </a>
            <a href="http://localhost:5001/diplomat" class="app-card diplomat" target="_blank">
                <div class="app-icon">🕊️</div>
                <div class="app-name">Diplomat</div>
                <div class="app-status">Reputation</div>
            </a>
            <a href="http://localhost:5001/mirror" class="app-card mirror" target="_blank">
                <div class="app-icon">🪞</div>
                <div class="app-name">Mirror</div>
                <div class="app-status">Config Sync</div>
            </a>
            <a href="http://localhost:5001/ledger" class="app-card ledger" target="_blank">
                <div class="app-icon">💰</div>
                <div class="app-name">Ledger</div>
                <div class="app-status">Economy</div>
            </a>
        </div>
        
        <div class="chat-container">
            <div id="chatHistory" class="chat-history">
                <div class="msg-ai">Goblin Brain: Welcome back, Boss. Systems are green.</div>
            </div>
            <div class="chat-input-area">
                <input type="text" id="chatInput" placeholder="Talk to the Brain..." onkeypress="if(event.key==='Enter') sendMessage()">
                <button class="send-btn" onclick="sendMessage()">SEND</button>
            </div>
        </div>
    </body>
    </html>
    """

# Singleton instance
hud = WebHUD()
