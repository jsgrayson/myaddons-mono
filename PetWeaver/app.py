from flask import Flask, render_template, jsonify, request
import os
import json
import threading
import time
from datetime import datetime
import automate
import requests
from simulator.strategy_manager import StrategyManager
import db_helper  # SQL database queries

# Load .env manually
if os.path.exists('.env'):
    with open('.env', 'r') as f:
        for line in f:
            if '=' in line:
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

app = Flask(__name__)

# Global state
state = {
    "status": "IDLE", # IDLE, RUNNING, COMPLETED, ERROR
    "log": [],
    "last_update": None,
    "stats": {
        "pets": 0,
        "strategies": 0,
        "ready": 0
    }
}

from blizzard_oauth import BlizzardOAuth

# Default WoW Addon Path (can be overridden by .env)
ADDON_PATH = os.environ.get('WOW_ADDON_PATH', '/Applications/World of Warcraft/_retail_/Interface/AddOns')

from market_manager import MarketManager
from combat_manager import CombatManager
from wishlist_manager import WishlistManager
from goblin_integrator import GoblinIntegrator

# Initialize Managers
strategy_manager = StrategyManager(os.path.join(os.path.dirname(__file__), "strategies_master.json"))
market_manager = MarketManager()
combat_manager = CombatManager()
wishlist_manager = WishlistManager()
goblin_integrator = GoblinIntegrator(market_manager)
goblin_integrator.start()

# ... (existing code) ...

@app.route('/api/wishlist', methods=['GET', 'POST', 'DELETE'])
def manage_wishlist():
    """Manage wishlist using SQL"""
    try:
        if request.method == 'GET':
            wishlist = db_helper.get_wishlist()
            return jsonify(wishlist)
            
        elif request.method == 'POST':
            data = request.json
            success = db_helper.add_to_wishlist(
                species_id=data.get('speciesId'),
                pet_name=data.get('petName'),
                breed_id=data.get('breedId'),
                breed_name=data.get('breedName')
            )
            return jsonify({"success": success})
            
        elif request.method == 'DELETE':
            data = request.json
            success = db_helper.remove_from_wishlist(
                species_id=data.get('speciesId')
            )
            return jsonify({"success": success})
            
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/scan_wild_pet', methods=['POST'])
def scan_wild_pet():
    data = request.json
    species_id = data.get('speciesId')
    breed_id = data.get('breedId')
    rarity = data.get('rarity', 'COMMON')
    
    # Check Wishlist
    match, item = wishlist_manager.check_match(species_id, breed_id)
    if match:
        return jsonify({
            "alert": True, 
            "message": f"Found {item['petName']} ({item['breedName']})!"
        })
        
    # Check Wild Monitor (Strategies/Mythicals)
    if species_id:
        monitor_alert = wild_monitor.check_wild_pet(int(species_id), rarity)
        if monitor_alert['alert']:
            return jsonify(monitor_alert)
            
    return jsonify({"alert": False})

@app.route('/api/alerts/active')
def get_active_alert():
    """Get current active alert for UI polling"""
    if wild_monitor.current_alert:
        # Only show alerts from last 15 seconds
        if time.time() - wild_monitor.current_alert.get('timestamp', 0) < 15:
            return jsonify(wild_monitor.current_alert)
    return jsonify({"alert": False})

@app.route('/wishlist')
def wishlist_page():
    return render_template('wishlist.html')

# Market Watcher API
@app.route('/api/market/update', methods=['POST'])
def update_market_price():
    data = request.json
    species_id = data.get('speciesId')
    price = data.get('price') # In gold or copper
    pet_name = data.get('petName', 'Unknown')
    
    if species_id and price is not None:
        market_manager.update_price(species_id, price, pet_name)
        
        # Check for deals immediately?
        # For now just log
        # log_message(f"Market Update: {pet_name} = {price}")
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Missing data"}), 400

@app.route('/api/market/deals', methods=['GET'])
def get_market_deals():
    # Default threshold 50% (0.5)
    threshold = float(request.args.get('threshold', 0.5))
    deals = market_manager.get_deals(threshold)
    return jsonify(deals)

@app.route('/api/market/missing')
def get_missing_deals():
    return jsonify(market_manager.get_missing_deals())

@app.route('/api/market/arbitrage')
def get_arbitrage_flips():
    return jsonify(market_manager.get_arbitrage_flips())

# --- Combat Logs ---
from combat_log_parser import CombatLogParser

combat_parser = CombatLogParser(
    saved_vars_path=os.path.join(ADDON_PATH, 'SavedVariables', 'PetWeaver.lua')
)

@app.route('/api/combat-logs')
def get_combat_logs():
    # In a real app, we'd cache this
    logs = combat_parser.parse_logs()
    return jsonify(logs)

@app.route('/api/combat-logs/latest')
def get_latest_combat_log():
    logs = combat_parser.parse_logs()
    if logs:
        return jsonify(logs[-1])
    return jsonify({})

@app.route('/combat-logs')
def combat_logs_page():
    return render_template('combat_log.html')

@app.route('/api/market/data', methods=['GET'])
def get_market_data():
    return jsonify(market_manager.get_all_data())

@app.route('/market')
def market_page():
    return render_template('market.html')

# Combat Log API
@app.route('/api/combat/log', methods=['POST'])
def log_combat_result():
    data = request.json
    result = data.get('result') # WIN/LOSS
    enemy = data.get('enemy', 'Unknown')
    my_team = data.get('myTeam', 'Unknown')
    rounds = data.get('rounds', 0)
    
    if result:
        combat_manager.log_battle(result, enemy, my_team, int(rounds))
        return jsonify({"status": "success"})
    return jsonify({"status": "error", "message": "Missing result"}), 400


@app.route('/combat')
def combat_page():
    return render_template('combat_log.html')

# Duplicate Consolidation API
@app.route('/get-duplicates')
def get_duplicates():
    """Get duplicate pets using fast SQL query"""
    try:
        import db_helper
        duplicates = db_helper.get_duplicates()
        
        # Format for frontend compatibility
        result = []
        for dup in duplicates:
            result.append({
                'speciesId': dup['species_id'],
                'name': dup['name'],
                'count': dup['count'],
                'bestQuality': dup['best_quality'],
                'bestLevel': dup['best_level']
            })
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Error loading duplicates: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/duplicates')
def duplicates_page():
    return render_template('duplicates.html')

# Collection Viewer API
@app.route('/api/collection/all', methods=['GET'])
def get_all_pets():
    """Get all pets using fast SQL query"""
    try:
        pets = db_helper.get_all_pets(limit=2000)  # Get all pets
        return jsonify(pets)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/collection')
def collection_page():
    return render_template('collection.html')

# Initialize Managers
from simulator.queue_manager import QueueManager
queue_manager = QueueManager(species_db={}, ability_db={}) # Data loaded internally

from simulator.wild_monitor import WildPetMonitor
wild_monitor = WildPetMonitor()

# --- DOJO ENGINE (Self-Play) ---
from dojo_engine import DojoEngine
dojo_engine = DojoEngine()

@app.route('/api/dojo/start', methods=['POST'])
def start_dojo():
    """Start a Dojo training session"""
    data = request.json
    generations = data.get('generations', 10)
    
    def run_dojo():
        dojo_engine.is_running = True
        dojo_engine.initialize_population()
        for _ in range(generations):
            if not dojo_engine.is_running: break
            dojo_engine.run_generation()
        dojo_engine.is_running = False
        
    thread = threading.Thread(target=run_dojo)
    thread.start()
    return jsonify({"message": "Dojo started"})

@app.route('/api/dojo/stop', methods=['POST'])
def stop_dojo():
    dojo_engine.is_running = False
    return jsonify({"message": "Dojo stopping..."})

@app.route('/api/dojo/status')
def dojo_status():
    return jsonify(dojo_engine.get_status())

@app.route('/dojo')
def dojo_page():
    return render_template('dojo.html')


@app.route('/api/queue/next', methods=['POST'])
def get_next_queue_team():
    data = request.json
    leveling_pet = data.get('leveling_pet')
    target_id = data.get('target_id')
    
    if not leveling_pet or not target_id:
        return jsonify({"error": "Missing leveling_pet or target_id"}), 400
    
    team = queue_manager.get_optimal_carry_team(leveling_pet, target_id)
    return jsonify(team)

@app.route('/api/queue/result', methods=['POST'])
def report_queue_result():
    data = request.json
    queue_manager.record_result(data)
    return jsonify({"efficiency": queue_manager.calculate_bandage_efficiency()})

@app.route('/api/alerts/wild', methods=['POST'])
def check_wild_alert():
    """Check if a wild pet seen in-game triggers an alert"""
    data = request.json
    pet_id = data.get('pet_id')
    rarity = data.get('rarity', 'COMMON')
    
    if not pet_id:
        return jsonify({"error": "Missing pet_id"}), 400
        
    alert = wild_monitor.check_wild_pet(int(pet_id), rarity)
    return jsonify(alert)

def get_blizzard_client():
    """Returns a requests session with authentication headers, refreshing token if needed"""
    client_id = os.getenv('BLIZZARD_CLIENT_ID')
    client_secret = os.getenv('BLIZZARD_CLIENT_SECRET')
    
    # Fallback to dummy if env vars missing (assuming token exists and is valid/refreshable)
    if not client_id or not client_secret:
        if os.path.exists('token.json'):
            client_id = "dummy"
            client_secret = "dummy"
        else:
            raise Exception("Missing credentials and no token found")
            
    oauth = BlizzardOAuth(client_id, client_secret)
    try:
        access_token = oauth.get_access_token()
    except Exception as e:
        raise Exception(f"Failed to get access token: {e}")
        
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {access_token}",
        "Battlenet-Namespace": "static-us",
        "Locale": "en_US"
    })
    return session

def log_message(msg):
    timestamp = datetime.now().strftime("%H:%M:%S")
    entry = f"[{timestamp}] {msg}"
    state["log"].append(entry)
    # Keep log size manageable
    if len(state["log"]) > 1000:
        state["log"] = state["log"][-1000:]
    print(entry)

def update_stats():
    try:
        if os.path.exists('my_pets.json'):
            with open('my_pets.json', 'r') as f:
                data = json.load(f)
                state["stats"]["pets"] = len(data.get('pets', []))
        
        if os.path.exists('strategies.json'):
            with open('strategies.json', 'r') as f:
                data = json.load(f)
                # Rough count of strategies
                count = 0
                for exp in data.values():
                    for cat in exp.values():
                        for enc in cat:
                            count += len(enc.get('strategies', []))
                state["stats"]["strategies"] = count

        if os.path.exists('my_ready_strategies.json'):
             with open('my_ready_strategies.json', 'r') as f:
                data = json.load(f)
                count = 0
                for exp in data.values():
                    count += len(exp)
                state["stats"]["ready"] = count # Changed to 'ready' as per context
    except Exception as e:
        print(f"Error updating stats: {e}")



def run_automation_thread(skip_fetch, force_scrape, addon_path):
    global state
    state["status"] = "RUNNING"
    state["log"] = [] # Clear log on new run
    log_message("🚀 Starting PetWeaver Automation...")
    
    try:
        # Capture stdout/stderr? For now, let's just manually log key steps
        # We need to adapt automate.py to be more library-friendly or just call its functions
        
        # 1. Auth/Fetch
        if not skip_fetch:
            log_message("🔐 Authenticating with Blizzard...")
            client_id = os.getenv('BLIZZARD_CLIENT_ID')
            client_secret = os.getenv('BLIZZARD_CLIENT_SECRET')
            
            if not client_id or not client_secret:
                if os.path.exists('token.json'):
                    log_message("⚠️  Using cached token (Env vars missing)")
                    client_id = "dummy"
                    client_secret = "dummy"
                else:
                    raise Exception("Missing Credentials")
            
            oauth = automate.BlizzardOAuth(client_id, client_secret)
            token = oauth.get_access_token()
            
            log_message("📥 Fetching Pet Collection...")
            fetcher = automate.PetCollectionFetcher(token)
            collection = fetcher.get_pet_collection()
            fetcher.save_collection(collection)
            log_message(f"✅ Fetched {len(collection.get('pets', []))} pets")
        else:
            log_message("⏭️  Skipping Fetch (Using local data)")

        # 2. Scrape
        if force_scrape or not os.path.exists('strategies.json'):
            log_message("🔄 Scraping Strategies (This may take time)...")
            scraper = automate.RobustXuFuScraper()
            scraper.scrape_all()
            if os.path.exists('strategies_final.json'):
                os.rename('strategies_final.json', 'strategies.json')
            log_message("✅ Scraping Complete")
        else:
            log_message("⏭️  Skipping Scrape (Data exists)")

        # 3. Match
        log_message("🎯 Matching Strategies...")
        matcher = automate.StrategyMatcher()
        matches = matcher.match_strategies()
        matcher.save_matches(matches)
        
        # 4. Export
        log_message(f"💾 Exporting to Addon: {addon_path}")
        lua_path = os.path.join(addon_path, 'PetWeaverData.lua')
        matcher.export_to_lua(matches, output_path=lua_path)
        
        state["status"] = "COMPLETED"
        state["last_update"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message("✅ Automation Successfully Completed!")
        update_stats()
        
    except Exception as e:
        state["status"] = "ERROR"
        log_message(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

CONFIG_FILE = 'config.json'

def load_config():
    default_path = automate.get_default_addon_path()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get('addon_path', default_path)
        except:
            pass
    return default_path

def save_config(addon_path):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump({'addon_path': addon_path}, f)
    except Exception as e:
        print(f"Error saving config: {e}")

@app.route('/')
def index():
    update_stats()
    current_path = load_config()
    return render_template('index.html', default_path=current_path)

@app.route('/api/status')
def get_status():
    """Get status with real-time SQL stats"""
    try:
        stats = db_helper.get_collection_stats()
        combat_today = db_helper.get_combat_stats(days=1)
        return jsonify({
            **state,
            "db_stats": stats,
            "combat_stats": combat_today
        })
    except Exception as e:
        return jsonify({**state, "stats_error": str(e)})

@app.route('/api/run', methods=['POST'])
def run_automation():
    if state["status"] == "RUNNING":
        return jsonify({"error": "Already running"}), 400
        
    data = request.json
    skip_fetch = data.get('skip_fetch', False)
    force_scrape = data.get('force_scrape', False)
    addon_path = data.get('addon_path', './PetWeaver')
    
    # Save the path for next time
    save_config(addon_path)
    
    thread = threading.Thread(target=run_automation_thread, args=(skip_fetch, force_scrape, addon_path))
    thread.start()
    
    return jsonify({"message": "Started"})

@app.route('/dashboard')
def dashboard():
    """Progress dashboard with charts and analytics"""
    return render_template('dashboard.html')

@app.route('/api/dashboard/charts')
def get_dashboard_charts():
    """Get detailed chart data for dashboard"""
    try:
        health_stats = db_helper.get_collection_health_stats()
        return jsonify({
            "collection_health": health_stats
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/collection/missing')
def get_missing_collection():
    """Get missing pets summary"""
    try:
        missing = db_helper.get_missing_pets(limit=10)
        return jsonify(missing)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/strategies')
def strategies():
    """Browse all strategies (mobile-optimized)"""
    return render_template('strategies.html')

@app.route('/hunting')
def hunting():
    """Pet hunting guide"""
    return render_template('hunting.html')

@app.route('/wizard')
def wizard():
    """Strategy Wizard for creating new strategies"""
    return render_template('wizard.html')

@app.route('/api/simulate/wizard', methods=['POST'])
def simulate_wizard_strategy():
    """Test a strategy from the wizard using Virtual Dojo"""
    try:
        from simulator import (
            BattleSimulator, BattleState, Team, Pet, Ability, 
            PetStats, PetFamily, PetQuality, TurnAction
        )
        
        data = request.json
        actions = data.get('actions', [])
        
        # 1. Create Dummy Teams (since we don't have full pet data yet)
        # Player: 3 Generic Pets
        player_pets = [
            Pet(
                species_id=1, name="My Pet 1", family=PetFamily.BEAST, quality=PetQuality.RARE,
                stats=PetStats(max_hp=1500, current_hp=1500, power=300, speed=280),
                abilities=[
                    Ability(id=1, name="Slot 1", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.BEAST),
                    Ability(id=2, name="Slot 2", power=25, accuracy=100, speed=0, cooldown=3, family=PetFamily.BEAST),
                    Ability(id=3, name="Slot 3", power=0, accuracy=100, speed=0, cooldown=0, family=PetFamily.BEAST, is_heal=True)
                ]
            ),
            Pet(
                species_id=2, name="My Pet 2", family=PetFamily.FLYING, quality=PetQuality.RARE,
                stats=PetStats(max_hp=1400, current_hp=1400, power=280, speed=320),
                abilities=[Ability(id=4, name="Peck", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.FLYING)]
            ),
            Pet(
                species_id=3, name="My Pet 3", family=PetFamily.MECHANICAL, quality=PetQuality.RARE,
                stats=PetStats(max_hp=1600, current_hp=1600, power=320, speed=260),
                abilities=[Ability(id=5, name="Zap", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.MECHANICAL)]
            )
        ]
        
        # Enemy: 3 Generic Pets (Target Dummies)
        enemy_pets = [
            Pet(
                species_id=101, name="Enemy Beast", family=PetFamily.BEAST, quality=PetQuality.RARE,
                stats=PetStats(max_hp=1500, current_hp=1500, power=280, speed=270),
                abilities=[Ability(id=10, name="Bite", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.BEAST)]
            ),
            Pet(
                species_id=102, name="Enemy Flyer", family=PetFamily.FLYING, quality=PetQuality.RARE,
                stats=PetStats(max_hp=1400, current_hp=1400, power=260, speed=300),
                abilities=[Ability(id=11, name="Swoop", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.FLYING)]
            ),
            Pet(
                species_id=103, name="Enemy Mech", family=PetFamily.MECHANICAL, quality=PetQuality.RARE,
                stats=PetStats(max_hp=1600, current_hp=1600, power=300, speed=250),
                abilities=[Ability(id=12, name="Laser", power=20, accuracy=100, speed=0, cooldown=0, family=PetFamily.MECHANICAL)]
            )
        ]
        
        player_team = Team(pets=player_pets)
        enemy_team = Team(pets=enemy_pets)
        
        initial_state = BattleState(
            player_team=player_team,
            enemy_team=enemy_team,
            turn_number=1,
            rng_seed=42
        )
        
        # 2. Create Agent Function from Wizard Actions
        def wizard_agent(state):
            # Simple interpreter for wizard actions
            # It tries actions in order until one is valid
            
            active_pet = state.player_team.get_active_pet()
            if not active_pet:
                return TurnAction(actor='player', action_type='pass')
            
            for action in actions:
                atype = action.get('type')
                
                if atype == 'ability':
                    slot = int(action.get('slot', 1)) - 1
                    if 0 <= slot < len(active_pet.abilities):
                        ability = active_pet.abilities[slot]
                        if active_pet.can_use_ability(ability):
                            return TurnAction(actor='player', action_type='ability', ability=ability)
                            
                elif atype == 'swap':
                    pet_idx = int(action.get('pet', 1)) - 1
                    if 0 <= pet_idx < len(state.player_team.pets):
                        target = state.player_team.pets[pet_idx]
                        if target.stats.is_alive() and pet_idx != state.player_team.active_pet_index:
                            return TurnAction(actor='player', action_type='swap', target_pet_index=pet_idx)
                            
                elif atype == 'conditional':
                    # Check condition
                    cond_type = action.get('condition_type')
                    cond_val = float(action.get('condition_value', 0))
                    
                    met = False
                    if cond_type == 'enemy_hp':
                        enemy = state.enemy_team.get_active_pet()
                        if enemy:
                            hp_pct = (enemy.stats.current_hp / enemy.stats.max_hp) * 100
                            if hp_pct < cond_val:
                                met = True
                    elif cond_type == 'my_hp':
                        hp_pct = (active_pet.stats.current_hp / active_pet.stats.max_hp) * 100
                        if hp_pct < cond_val:
                            met = True
                    elif cond_type == 'round':
                        if state.turn_number >= cond_val:
                            met = True
                            
                    # Execute Then or Else
                    chosen_slot = int(action.get('then_slot' if met else 'else_slot', 1)) - 1
                    if 0 <= chosen_slot < len(active_pet.abilities):
                        ability = active_pet.abilities[chosen_slot]
                        if active_pet.can_use_ability(ability):
                            return TurnAction(actor='player', action_type='ability', ability=ability)
            
            # Default fallback
            return TurnAction(actor='player', action_type='ability', ability=active_pet.abilities[0])

        # Enemy Agent (Simple AI)
        def enemy_agent(state):
            pet = state.enemy_team.get_active_pet()
            if pet:
                # Just use first available ability
                for ability in pet.abilities:
                    if pet.can_use_ability(ability):
                        return TurnAction(actor='enemy', action_type='ability', ability=ability)
            return TurnAction(actor='enemy', action_type='pass')

        # 3. Run Simulation
        simulator = BattleSimulator(rng_seed=42)
        result = simulator.simulate_battle(initial_state, wizard_agent, enemy_agent)
        
        # 4. Format Output
        log_lines = result['log'].get_full_log().split('\n')
        
        return jsonify({
            "winner": result['winner'],
            "turns": result['turns'],
            "log": log_lines,
            "message": f"Simulation complete! Winner: {result['winner'].upper()} in {result['turns']} turns."
        })
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# Genetic Evolution State
genetic_state = {
    "status": "IDLE",
    "generation": 0,
    "max_generations": 0,
    "best_fitness": 0,
    "avg_fitness": 0,
    "top_teams": [],
    "stop_flag": False,
    "log": []
}

def run_evolution_thread(target_name, pop_size, generations, my_pets_only=True, leveling_mode=0):
    global genetic_state
    genetic_state["status"] = "RUNNING"
    genetic_state["generation"] = 0
    genetic_state["max_generations"] = generations
    genetic_state["stop_flag"] = False
    genetic_state["log"] = []
    genetic_state["target_encounter"] = target_name  # Store target name for export
    genetic_state["leveling_mode"] = leveling_mode
    
    try:
        from genetic.evolution import EvolutionEngine
        from genetic.fitness import FitnessEvaluator
        from simulator import Team, Pet, PetStats, PetFamily, PetQuality, Ability
        
        # 1. Setup Target Team - Load real encounter data from encounters_full.json
        try:
            # Load from new complete encounters API endpoint
            # This merges encounters_full.json abilities with species stats
            import requests
            response = requests.get('http://127.0.0.1:5000/api/encounters')
            if response.status_code == 200:
                encounters = response.json()
                encounter_data = encounters.get(target_name)
            else:
                raise FileNotFoundError(f"API returned {response.status_code}")
            
            # Build target team from complete encounter data
            target_pets = []
            for npc_pet in encounter_data['npc_pets']:
                family_map = {
                    'Magic': PetFamily.MAGIC,
                    'Humanoid': PetFamily.HUMANOID,
                    'Undead': PetFamily.UNDEAD,
                    'Beast': PetFamily.BEAST,
                    'Aquatic': PetFamily.AQUATIC,
                    'Mechanical': PetFamily.MECHANICAL,
                    'Elemental': PetFamily.ELEMENTAL,
                    'Flying': PetFamily.FLYING,
                    'Dragonkin': PetFamily.DRAGONKIN,
                    'Critter': PetFamily.CRITTER,
                }
                family = family_map.get(npc_pet['family'], PetFamily.BEAST)
                
                abilities = []
                for ab_data in npc_pet['abilities']:
                    abilities.append(Ability(
                        id=ab_data['id'],
                        name=ab_data['name'],
                        power=ab_data['power'],
                        accuracy=ab_data['accuracy'],
                        speed=ab_data['speed'],
                        cooldown=ab_data['cooldown'],
                        family=family
                    ))
                
                quality_map = {
                    'poor': PetQuality.POOR,
                    'common': PetQuality.COMMON,
                    'uncommon': PetQuality.UNCOMMON,
                    'rare': PetQuality.RARE,
                    'epic': PetQuality.EPIC,
                    'legendary': PetQuality.LEGENDARY
                }
                quality = quality_map.get(npc_pet.get('quality', 'rare').lower(), PetQuality.RARE)

                target_pets.append(Pet(
                    species_id=npc_pet['species_id'],
                    name=npc_pet['name'],
                    family=family,
                    quality=quality,
                    stats=PetStats(
                        max_hp=npc_pet['health'],
                        current_hp=npc_pet['health'],
                        power=npc_pet['power'],
                        speed=npc_pet['speed']
                    ),
                    abilities=abilities
                ))
            
            target_team = Team(pets=target_pets)
            genetic_state["log"].append(f"Loaded encounter: {encounter_data['name']}")
            
        except FileNotFoundError:
            # NO MOCK DATA - require real encounters_complete.json
            genetic_state["log"].append("❌ ERROR: encounters_complete.json not found!")
            genetic_state["status"] = "ERROR"
            genetic_state["best_fitness"] = 0
            genetic_state["avg_fitness"] = 0
            raise FileNotFoundError("encounters_complete.json is required - no mock data allowed")
        
        # 2. Setup Data (Real Data + Manual Overrides)
        try:
            # Load Abilities from API (Base data)
            with open('abilities.json', 'r') as f:
                ability_data = json.load(f)
                real_abilities = ability_data.get('abilities', {})
                species_abilities = ability_data.get('species_abilities', {})
                
            # NEW: Load PetTracker Decoded Data (Primary Source)
            pt_species_abilities = {}
            pt_breeds = {}
            pt_base_stats = {}
            
            if os.path.exists('pettracker_decoded.json'):
                try:
                    with open('pettracker_decoded.json', 'r') as f:
                        pt_data = json.load(f)
                        pt_species_abilities = pt_data.get('species', {})
                        pt_breeds = pt_data.get('breeds', {})
                        pt_base_stats = pt_data.get('stats', {})
                        
                    genetic_state["log"].append(f"Loaded PetTracker data for {len(pt_species_abilities)} species")
                    
                    # Merge PetTracker abilities into species_abilities (Priority)
                    # PetTracker format: "species_id": {"1": [id], "2": [id]...}
                    # Target format: "species_id": [id1, id2, id3, id4, id5, id6]
                    for sid_str, slots in pt_species_abilities.items():
                        # Convert slots dict to list
                        ability_list = [0] * 6
                        for slot_idx, ability_ids in slots.items():
                            # PetTracker might have multiple options per slot? 
                            # The decoder returns a list of IDs. Usually it's just one.
                            # We'll take the first one for now as the default choice for that slot
                            if ability_ids:
                                idx = int(slot_idx) - 1
                                if 0 <= idx < 6:
                                    ability_list[idx] = ability_ids[0]
                        
                        # Only update if we have valid abilities
                        if any(aid > 0 for aid in ability_list):
                            species_abilities[sid_str] = ability_list
                            
                except Exception as e:
                    genetic_state["log"].append(f"Error loading PetTracker data: {e}")
            
            # Load manual ability stats override (since Blizzard API doesn't provide power/accuracy)
            try:
                with open('ability_stats_manual.json', 'r') as f:
                    manual_stats = json.load(f)
                    # Merge manual stats into real_abilities
                    # Merge manual stats into real_abilities
                    for ab_id, stats in manual_stats.get('abilities', {}).items():
                        if ab_id in real_abilities:
                            # Override with manual stats
                            real_abilities[ab_id].update(stats)
                        else:
                            # Add missing ability
                            real_abilities[ab_id] = stats.copy()
                            # Ensure minimal fields
                            if 'id' not in real_abilities[ab_id]:
                                real_abilities[ab_id]['id'] = int(ab_id)
                            if 'family_id' not in real_abilities[ab_id]:
                                real_abilities[ab_id]['family_id'] = 7 # Default Beast
                        
                        genetic_state["log"].append(f"Loaded {len(manual_stats.get('abilities', {}))} manual ability stats")
            except FileNotFoundError:
                genetic_state["log"].append("WARNING: ability_stats_manual.json not found, using API defaults")
                
            # Load User Collection
            with open('my_pets.json', 'r') as f:
                collection_data = json.load(f)
                
            # Extract available species IDs
            # Extract available species IDs
            available_species = []
            for pet in collection_data.get('pets', []):
                if 'species' in pet:
                    sid = pet['species']['id']
                    # Only include if we have ability data for it
                    # Note: species_abilities keys are strings in JSON
                    if str(sid) in species_abilities:
                        available_species.append(sid)
            
            # Pass collection to MarketManager for cross-referencing
            market_manager.set_collection(collection_data.get('pets', []))
            
            # Remove duplicates
            available_species = list(set(available_species))
            
            genetic_state["log"].append(f"Available species pool: {len(available_species)} pets")
            if my_pets_only:
                genetic_state["log"].append("Using ONLY your pets")
            
            # Load species data for display
            species_info_map = {}
            if os.path.exists('species_data.json'):
                with open('species_data.json', 'r') as f:
                    species_data = json.load(f)
                    for sid_str, data in species_data.items():
                        species_info_map[int(sid_str)] = data
                        
                        # Merge PetTracker Base Stats if available
                        if sid_str in pt_base_stats:
                             species_info_map[int(sid_str)]['base_stats'] = pt_base_stats[sid_str]
            
            if not available_species:
                raise Exception("No species data found. Please run fetch_ability_data.py first.")
                
            # Load NPC AI Priorities
            npc_priorities = {}
            try:
                if os.path.exists('npc_ai_priorities.json'):
                    with open('npc_ai_priorities.json', 'r') as f:
                        all_priorities = json.load(f)
                        # Find priorities for current target
                        # Try exact match first
                        if target_name in all_priorities:
                            npc_priorities = all_priorities[target_name]
                        else:
                            # Try fuzzy match
                            norm_target = target_name.lower().replace("'", "").replace(":", "").strip()
                            for tamer_name, priorities in all_priorities.items():
                                norm_tamer = tamer_name.lower().replace("'", "").replace(":", "").strip()
                                if norm_tamer in norm_target or norm_target in norm_tamer:
                                    npc_priorities = priorities
                                    genetic_state["log"].append(f"Loaded AI priorities for {tamer_name}")
                                    break
            except Exception as e:
                genetic_state["log"].append(f"Error loading AI priorities: {e}")

        except Exception as e:
            genetic_state["log"].append(f"Data load error: {str(e)}")
            print(f"Data load error: {e}")
            # Fallback or re-raise? Let's re-raise to be caught by main loop or just continue with what we have
            # For now, let's allow it to fall through to the main except if critical
            raise e

        # 3. Initialize Engine and build real pet stats map
        # Fix keys to be integers for the engine
        formatted_ability_db = {int(k): v for k, v in species_abilities.items()}
        
        # Build real pet stats map {species_id: {health, power, speed}}
        real_pet_stats = {}
        try:
            with open('my_pets.json') as f:
                collection = json.load(f)
                for pet in collection.get('pets', []):
                    if 'species' in pet and 'stats' in pet:
                        sid = pet['species']['id']
                        sid_str = str(sid)
                        
                        # Priority 1: Use actual stats from my_pets.json (if owned)
                        if sid not in real_pet_stats:  # Use first found (highest level)
                            real_pet_stats[sid] = {
                                'health': pet['stats'].get('health', 1400),
                                'power': pet['stats'].get('power', 280),
                                'speed': pet['stats'].get('speed', 280)
                            }
                        
                        # Priority 2: Calculate from PetTracker Base Stats + Breed (if available)
                        # This is useful if we want to simulate optimal breeds or if my_pets stats are missing
                        # For now, we stick to my_pets stats for owned pets.
                        
            # Fill in missing stats for species we don't own (if my_pets_only=False)
            # using PetTracker base stats assuming a standard breed (e.g. B/B or P/P)
            for sid in available_species:
                if sid not in real_pet_stats and str(sid) in pt_base_stats:
                    base = pt_base_stats[str(sid)]
                    # Assume Rare quality (1.3 multiplier approx? No, formula is different)
                    # Formula: (Base + Breed) * Level * Quality ...
                    # Simplified approximation for L25 Rare:
                    # Health = (Base + 0.5) * 25 * 1.3 + 100 ?? 
                    # Let's use a standard L25 Rare approximation:
                    # Power/Speed ~= Base * 12.5 ?
                    # Health ~= Base * 12.5 + 100 ?
                    # Actually, let's just use the raw multipliers scaled up to typical L25 values
                    # Typical Base is 8. 8 * X = 280 => X = 35
                    
                    real_pet_stats[sid] = {
                        'health': int(base['health'] * 180 + 100), # Approx
                        'power': int(base['power'] * 35),
                        'speed': int(base['speed'] * 35)
                    }
                    
        except Exception as e:
            print(f"Error building pet stats: {e}")
            pass  # Fallback to mock stats if file missing
        
        # Build species_db with family information for type advantage calculations
        species_db = {}
        # Initialize Fitness Evaluator
        evaluator = FitnessEvaluator(
            target_team=target_team,
            ability_db=real_abilities,
            species_db=species_info_map,
            npc_priorities=npc_priorities,
            target_name=target_name
        )
        
        # Monkey-patch real data into evaluator
        evaluator.real_abilities = real_abilities
        evaluator.real_pet_stats = real_pet_stats
        evaluator.pt_base_stats = pt_base_stats # Pass PetTracker base stats
        # 3. Initialize Evolution Engine
        engine = EvolutionEngine(
            fitness_evaluator=evaluator,
            population_size=pop_size,
            mutation_rate=0.5, # High mutation for exploration
            elitism_rate=0.1
        )
            
        # STRATEGY SEEDING: Check for known strategies
        seed_teams = []
        try:
            # Use global strategy_manager initialized at top of app.py
            recommended_ids = strategy_manager.get_recommended_team(target_name)
            if recommended_ids and all(pid > 0 for pid in recommended_ids):
                genetic_state["log"].append(f"💡 Found known strategy! Seeding: {recommended_ids}")
                seed_teams.append(recommended_ids)
            else:
                # Try similarity search (Placeholder for now)
                # similar_seeds = strategy_manager.find_similar_strategies(target_families=[p.family for p in target_team.pets])
                # if similar_seeds: seed_teams.extend(similar_seeds)
                pass
        except Exception as e:
            genetic_state["log"].append(f"⚠️ Strategy lookup failed: {e}")

        genetic_state["log"].append(f"🧬 Initializing Population (Size: {pop_size})...")
        engine.initialize_population(
            available_species, 
            real_abilities, # Use the merged ability DB
            seed_teams=seed_teams,
            npc_name=target_name,
            strategy_manager=strategy_manager
        )
        
        genetic_state["log"].append("🧬 Population Initialized")
        
        # 4a. Pre-Check: Evaluate Seeded Teams
        # We check the top few genomes (which are the seeds)
        genetic_state["log"].append("🔍 Pre-Checking Known Strategies...")
        pre_check_winners = []
        
        # Evaluate first 5 genomes (Seeds are at the front)
        for i in range(min(5, len(engine.population))):
            genome = engine.population[i]
            fitness = evaluator.evaluate(genome)
            genome.fitness = fitness
            
            # If fitness indicates a win (e.g., > 1000 or whatever our win threshold is)
            # Actually, let's look at the win flag in the stats if available, 
            # but evaluator returns a float. 
            # Assuming high fitness = win.
            # Better: Check if it's a "perfect" win (no deaths?) or just a win.
            # For now, just log high fitness ones.
            if fitness > 0:
                pre_check_winners.append(genome)
                
        if pre_check_winners:
            best_pre = max(pre_check_winners, key=lambda g: g.fitness)
            genetic_state["log"].append(f"✨ Found strong starting team! Fitness: {best_pre.fitness:.1f}")
            # We don't stop, but we ensure this team is preserved via elitism
        else:
            genetic_state["log"].append("No immediate wins from known strategies.")
        
        # 4b. Evolution Loop
        for gen in range(generations):
            if genetic_state["stop_flag"]:
                break
                
            stats = engine.evolve_generation(available_species)
            
            # Update State
            genetic_state["generation"] = gen + 1
            genetic_state["best_fitness"] = stats["best_fitness"]
            genetic_state["avg_fitness"] = stats["avg_fitness"]
            
            # Enhanced logging: show top 3 teams with win rates
            top_genomes = stats.get("top_genomes", [])
            
            # Build summary of top 3 teams
            team_summaries = []
            for i, genome in enumerate(top_genomes[:3]):
                species_ids = ",".join([str(p.species_id) for p in genome.pets])
                
                # Calculate wins and losses (5 battles per genome)
                num_battles = 5
                if hasattr(genome, 'stats') and genome.stats:
                    win_rate = genome.stats.get("win_rate", 0)
                    wins = int(win_rate * num_battles)
                    losses = num_battles - wins
                    record = f"{wins}W-{losses}L"
                else:
                    record = "0W-3L"
                
                team_summaries.append(f"#{i+1}:[{species_ids}] {record}")
            
            teams_str = " | ".join(team_summaries) if team_summaries else "No teams"
            
            # Log with detailed team info
            genetic_state["log"].append(
                f"Gen {gen+1}: Fitness {stats['best_fitness']:.0f} | {teams_str}"
            )
                
            time.sleep(0.1) # Yield to main thread
            
        # 5. Finish
        genetic_state["status"] = "COMPLETED"
        if 'stats' not in locals():
            genetic_state["log"].append("ERROR: Evolution loop did not run")
            return

        print(f"DEBUG: stats keys: {stats.keys()}")
        
        genetic_state["top_teams"] = []
        for idx, genome in enumerate(stats.get("top_genomes", [])):
            # Convert genome to full team to get stats and ability details
            full_team = evaluator._genome_to_team(genome)
            
            # Capture battle log for the #1 team only (to save bandwidth)
            battle_log = None
            if idx == 0:
                try:
                    # Re-run a single battle with logging enabled
                    result = evaluator.play_battle(genome, enable_logging=True)
                    if result and 'log' in result:
                        battle_log = result['log'].get_full_log()
                except Exception as e:
                    print(f"Error capturing battle log: {e}")
            
            team_data = {
                "fitness": genome.fitness,
                "stats": genome.stats,
                "battle_log": battle_log,
                "pets": []
            }
            
            for i, pet in enumerate(full_team.pets):
                pet_data = {
                    "species_id": pet.species_id,
                    "name": pet.name,
                    "family_id": pet.family.value,
                    "stats": {
                        "health": pet.stats.max_hp,
                        "power": pet.stats.power,
                        "speed": pet.stats.speed
                    },
                    "abilities": []
                }
                
                # Get active abilities (the 3 selected)
                for ability in pet.abilities:
                    pet_data["abilities"].append({
                        "id": ability.id,
                        "name": ability.name,
                        "power": ability.power,
                        "accuracy": ability.accuracy,
                        "cooldown": ability.cooldown,
                        "type": ability.family.name.capitalize()
                    })
                
                team_data["pets"].append(pet_data)
            
            genetic_state["top_teams"].append(team_data)
        
    except Exception as e:
        import traceback
        error_msg = f"Evolution error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)  # Print to server console
        genetic_state["log"].append(f"ERROR: {str(e)}")
        genetic_state["status"] = "ERROR"

@app.route('/test')
def test_page():
    return render_template('test.html')

@app.route('/api/hunting/missing')
def get_missing_pets():
    """Get important missing pets using SQL"""
    try:
        missing = db_helper.get_missing_pets(limit=50)
        return jsonify(missing)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/encounters')
def get_encounters():
    """Get all encounters using SQL"""
    try:
        encounters = db_helper.get_all_encounters()
        return jsonify(encounters)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/genetic')
def genetic_dashboard():
    # Load encounters from the new API endpoint which has complete ability data
    encounters = {}
    try:
        # Call our own API endpoint to get complete encounters
        import requests
        response = requests.get('http://127.0.0.1:5000/api/encounters')
        if response.status_code == 200:
            encounters = response.json()
    except:
        # Fallback to direct file loading if API not available
        if os.path.exists('encounters_complete.json'):
            with open('encounters_complete.json', 'r') as f:
                encounters = json.load(f) # Changed to encounters_complete.json and kept variable name as encounters
    return render_template('genetic.html', encounters=encounters)

@app.route('/genetic-simple')
def genetic_simple():
    return render_template('genetic_simple.html')

@app.route('/api/genetic/start', methods=['POST'])
def start_evolution():
    data = request.json
    if genetic_state["status"] == "RUNNING":
        return jsonify({"error": "Already running"}), 400
        
    # Reset state
    genetic_state["log"] = []
    genetic_state["top_teams"] = []
    genetic_state["stop_flag"] = False
    genetic_state["status"] = "RUNNING"
    
    thread = threading.Thread(target=run_evolution_thread, args=(
        data.get('target', 'squirt'),
        int(data.get('pop_size', 50)),
        int(data.get('generations', 20))
    ))
    thread.start()
    return jsonify({"message": "Started"})

@app.route('/api/genetic/status')
def get_evolution_status():
    # Return status and new logs
    offset = int(request.args.get('offset', 0))
    
    response = genetic_state.copy()
    # Send only new logs
    if offset < len(genetic_state["log"]):
        response["new_logs"] = genetic_state["log"][offset:]
        response["log_offset"] = len(genetic_state["log"])
    else:
        response["new_logs"] = []
        response["log_offset"] = offset
        
    # Don't send the full log in the response to save bandwidth
    del response["log"]
    
    return jsonify(response)

@app.route('/api/genetic/stop', methods=['POST'])
def stop_evolution():
    genetic_state["stop_flag"] = True
    return jsonify({"message": "Stopping..."})

@app.route('/api/goblin/protected')
def get_protected_pets():
    """Generate list of pets to protect (do not sell) for Goblin integration"""
    try:
        protected_pets = {} # pet_id -> reason
        
        # 1. Protect all pets used in strategies
        if os.path.exists('strategies_enhanced.json'):
            with open('strategies_enhanced.json', 'r') as f:
                strategies_data = json.load(f)
                
                for expansion, categories in strategies_data.items():
                    for category, encounters in categories.items():
                        for encounter in encounters:
                            for strategy in encounter.get('strategies', []):
                                for slot in strategy.get('pet_slots', []):
                                    for pet_option in slot:
                                        pet_id = pet_option.get('id')
                                        pet_name = pet_option.get('name', 'Unknown')
                                        
                                        if pet_id and pet_id != 0:
                                            if pet_id not in protected_pets:
                                                protected_pets[pet_id] = {
                                                    "name": pet_name,
                                                    "reasons": set()
                                                }
                                            protected_pets[pet_id]["reasons"].add("Used in strategy")

        # 2. Protect favorites (if we had a favorites system fully persisted)
        # For now, let's just stick to strategies
        
        # Convert sets to lists for JSON serialization
        export_list = []
        for pid, data in protected_pets.items():
            export_list.append({
                "id": pid,
                "name": data["name"],
                "reason": ", ".join(data["reasons"])
            })
            
        # Save to file for external access
        with open('protected_pets.json', 'w') as f:
            json.dump({"protected": export_list, "generated_at": datetime.now().isoformat()}, f, indent=2)
            
        return jsonify({
            "count": len(export_list),
            "file_path": os.path.abspath('protected_pets.json'),
            "protected_pets": export_list
        })
        
    except Exception as e:
        print(f"Error generating protected list: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/analytics')
def get_analytics():
    """Get analytics using fast SQL queries"""
    try:
        # Get collection stats from SQL
        stats = db_helper.get_collection_stats()
        
        # Get duplicates from SQL
        duplicates = db_helper.get_duplicates()
        
        return jsonify({
            'collection_stats': stats,
            'duplicates': len(duplicates),
            'duplicate_details': duplicates[:10]  # Top 10 duplicates
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/maintenance/fetch-species')
def trigger_species_fetch():
    """Fetch species data from Blizzard API to populate family info"""
    try:
        if not os.path.exists('my_pets.json'):
            return jsonify({"error": "my_pets.json not found"}), 404
            
        with open('my_pets.json', 'r') as f:
            pets_data = json.load(f)
            
        unique_species_ids = set()
        for pet in pets_data.get('pets', []):
            if 'species' in pet and 'id' in pet['species']:
                unique_species_ids.add(pet['species']['id'])
        
        # Load existing cache
        species_cache = {}
        if os.path.exists('species_data.json'):
            with open('species_data.json', 'r') as f:
                species_cache = json.load(f)
        
        # Identify missing
        missing_ids = [sid for sid in unique_species_ids if str(sid) not in species_cache]
        
        if not missing_ids:
            return jsonify({"message": "All species data already cached", "count": len(species_cache)})
            
        # Fetch missing (limit to 50 to avoid timeout/rate limits for now)
        client = get_blizzard_client()
        count = 0
        for sid in missing_ids[:50]: 
            try:
                # Fetch pet info
                # We need to use the Battle.net API client
                # Using the client directly if possible, or constructing the URL
                # The client object from OAuth2Session might not be enough if token expired
                # But let's assume it works or use a helper
                
                # We can use the token from the session if available, or get a new one
                # For simplicity, let's assume we have a valid token or client
                
                # Actually, get_blizzard_client returns an OAuth2Session. 
                # We need to make sure we have a token.
                
                resp = client.get(f"https://us.api.blizzard.com/data/wow/pet/{sid}?namespace=static-us&locale=en_US")
                if resp.status_code == 200:
                    data = resp.json()
                    species_cache[str(sid)] = {
                        "name": data.get("name"),
                        "family_id": data.get("battle_pet_type", {}).get("id"),
                        "family_name": data.get("battle_pet_type", {}).get("name")
                    }
                    count += 1
                    print(f"Fetched species {sid}: {data.get('name')}")
                else:
                    print(f"Failed to fetch species {sid}: {resp.status_code}")
                    
            except Exception as e:
                print(f"Error fetching species {sid}: {e}")
        
        # Save cache
        with open('species_data.json', 'w') as f:
            json.dump(species_cache, f, indent=2)
            
        return jsonify({
            "message": f"Fetched {count} new species", 
            "total_cached": len(species_cache),
            "remaining": len(missing_ids) - count
        })
        
    except Exception as e:
        print(f"Error in species fetch: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/analytics/collection-health')
def get_collection_health():
    """Analyze pet collection for strategic gaps and coverage using SQL"""
    try:
        family_stats = db_helper.get_collection_health_stats()
        
        # Calculate overall health score
        total_coverage = sum(f['coverage_pct'] for f in family_stats.values()) / len(family_stats) if family_stats else 0
        
        return jsonify({
            "health_score": round(total_coverage, 1),
            "family_coverage": family_stats,
            "gap_analysis": [] # TODO: Implement gap analysis in SQL later
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/leveling')
def leveling():
    """Leveling queue planner"""
    return render_template('leveling.html')

@app.route('/xp-encounters')
def xp_encounters():
    """Best XP encounters"""
    return render_template('xp_encounters.html')

@app.route('/api/progress')
def get_progress():
    """Get user progress data from saved files"""
    progress = {
        "favorites": [],
        "completed": {},
        "statistics": {
            "totalBattles": 0,
            "totalWins": 0,
            "totalLosses": 0,
            "winRate": 0
        }
    }
    
    # Would typically read from PetWeaverProgressDB if we had a sync
    # For now, return mock data or empty structure
    return jsonify(progress)

@app.route('/api/combat/history', methods=['GET'])
def get_combat_history():
    """Get combat history using SQL"""
    try:
        logs = db_helper.get_combat_logs(limit=100)
        return jsonify(logs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/recommendations')
def get_recommendations():
    """Get smart recommendations for next activities using SQL"""
    try:
        recommendations = db_helper.get_recommendations(limit=10)
        return jsonify(recommendations)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/strategies/all')
def get_all_strategies():
    try:
        strategies = db_helper.get_all_strategies()
        return jsonify(strategies)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/leveling/queue')
def get_leveling_queue():
    """Get priority list of pets to level"""
    try:
        pets_to_level = {}
        
        if os.path.exists('my_pets.json') and os.path.exists('my_ready_strategies.json'):
            # Load owned pets and their levels, mapped by NAME
            with open('my_pets.json', 'r') as f:
                pet_data = json.load(f)
                owned_pets = {}
                for pet in pet_data.get('pets', []):
                    if 'species' not in pet:
                        continue
                    
                    # Get name
                    name_data = pet['species'].get('name')
                    if isinstance(name_data, dict):
                        name = name_data.get('en_US')
                    else:
                        name = name_data
                        
                    if not name:
                        continue
                        
                    level = pet.get('level', 1)
                    quality = pet.get('quality', 0)
                    
                    # Track highest level/quality of each species (by name)
                    if name not in owned_pets or level > owned_pets[name]['level']:
                        owned_pets[name] = {
                            'level': level,
                            'quality': quality,
                            'name': name,
                            'id': pet['species'].get('id')
                        }
            
            # Find which owned pets are used in ready strategies but not max level
            with open('my_ready_strategies.json', 'r') as f:
                data = json.load(f)
                
                for exp_name, expansions in data.items():
                    for cat_name, encounters in expansions.items():
                        for encounter in encounters:
                            for strategy in encounter.get('strategies', []):
                                for slot in strategy.get('pet_slots', []):
                                    if slot and slot[0]:
                                        pet = slot[0]
                                        pet_id = int(pet.get('id'))
                                        pet_name = pet.get('name', 'Unknown')
                                        
                                        # Check if owned (by name) but needs work (Level < 25 OR Quality != RARE)
                                        if pet_name in owned_pets:
                                            pet_data = owned_pets[pet_name]
                                            current_level = pet_data['level']
                                            
                                            # Check quality
                                            quality_info = pet_data.get('quality')
                                            is_rare = False
                                            if isinstance(quality_info, dict):
                                                is_rare = quality_info.get('type') == 'RARE'
                                            
                                            needs_level = current_level < 25
                                            needs_rarity = not is_rare
                                            
                                            if needs_level or needs_rarity:
                                                if pet_id not in pets_to_level:
                                                    pets_to_level[pet_id] = {
                                                        'id': pet_id,
                                                        'name': pet_name,
                                                        'current_level': current_level,
                                                        'quality': quality_info,
                                                        'needs_level': needs_level,
                                                        'needs_rarity': needs_rarity,
                                                        'needed_for': [],
                                                        'priority': 0
                                                    }
                                                
                                                pets_to_level[pet_id]['needed_for'].append(encounter.get('encounter_name', 'Unknown'))
                                                pets_to_level[pet_id]['priority'] = len(pets_to_level[pet_id]['needed_for'])
        
        # Convert to list and sort by priority (most needed first)
        result = sorted(pets_to_level.values(), key=lambda x: x['priority'], reverse=True)
        return jsonify(result[:30])  # Top 30 pets to level
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/combat/stats', methods=['GET'])
def get_combat_stats():
    """Get combat stats using SQL"""
    try:
        stats = db_helper.get_combat_stats(days=30)
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/xp-encounters')
def get_xp_encounters():
    """Get best XP encounters (fast, repeatable)"""
    try:
        xp_encounters = []
        
        if os.path.exists('my_ready_strategies.json'):
            with open('my_ready_strategies.json', 'r') as f:
                data = json.load(f)
                
                for exp_name, expansions in data.items():
                    for cat_name, encounters in expansions.items():
                        for encounter in encounters:
                            if not encounter.get('strategies'):
                                continue
                            
                            strategy = encounter['strategies'][0]
                            script = strategy.get('script', '')
                            pet_slots = strategy.get('pet_slots', [])
                            
                            # Score for XP farming (fast battles, carry slots, repeatability)
                            xp_score = 0
                            carry_slot = None
                            
                            # Check for carry mechanics
                            if 'standby' in script:
                                xp_score += 15
                                carry_slot = 3
                            elif 'change(next)' in script and script.count('use(') < 8:
                                xp_score += 10
                                carry_slot = 3
                            
                            # Prefer short scripts (fast battles)
                            if len(script) < 150:
                                xp_score += 10
                            elif len(script) < 250:
                                xp_score += 5
                            
                            # Repeatability
                            if 'World Quest' in cat_name or 'Tamer' in cat_name:
                                xp_score += 8
                            
                            # Only include high XP encounters
                            if xp_score >= 15:
                                carry_name = 'Slot 3'
                                if carry_slot == 3 and len(pet_slots) >= 3 and pet_slots[2] and pet_slots[2][0]:
                                    carry_name = pet_slots[2][0].get('name', 'Slot 3')
                                
                                xp_encounters.append({
                                    'encounter': encounter.get('encounter_name', 'Unknown'),
                                    'expansion': exp_name,
                                    'category': cat_name,
                                    'carry_slot': carry_name,
                                    'xp_score': xp_score,
                                    'speed': 'Fast' if len(script) < 150 else 'Medium'
                                })
                
                # Sort by XP score
                xp_encounters.sort(key=lambda x: x['xp_score'], reverse=True)
        
        return jsonify(xp_encounters[:25])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/calendar')

def calendar():
    """Calendar page showing Squirt and Pet Battle Weeks"""
    return render_template('calendar.html')

@app.route('/api/calendar')
def get_calendar():
    """Return upcoming dates starting from today with Squirt and Pet Battle Week flags"""
    try:
        import datetime, calendar, flask
        # Get number of days param or default to 14 days ahead
        days_ahead = int(flask.request.args.get('days', 14))
        
        # Start from today
        start_date = datetime.date.today()
        
        # Base squirt date for schedule
        base_squirt = datetime.date(2025, 12, 3)
        # Pet Battle Week start
        pbw_start = datetime.date(2025, 12, 16)
        result = []
        for day in range(days_ahead):
            d = start_date + datetime.timedelta(days=day)
            days_since_base = (d - base_squirt).days
            is_squirt = (days_since_base % 15) == 0
            
            # Pet Battle Week repeats every 6 weeks (42 days)
            # This is an estimate; the actual rotation can vary slightly with patch cycles
            days_since_pbw = (d - pbw_start).days
            is_pbw = (days_since_pbw % 42) < 7 and days_since_pbw >= 0
            result.append({
                'date': d.isoformat(),
                'weekday': d.strftime('%A'),
                'is_squirt': is_squirt,
                'is_pet_battle_week': is_pbw
            })
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/squirt-status')
def get_squirt_status():
    """Check if it's Squirt day (based on updated schedule)"""
    try:
        import datetime
        
        # Updated base date so that 2025-12-03 is a Squirt day and repeats every 15 days
        base_squirt_date = datetime.datetime(2025, 12, 3)
        now = datetime.datetime.now()
        days_since_base = (now - base_squirt_date).days
        
        # Squirt appears every 15 days
        is_squirt_day = (days_since_base % 15) == 0
        
        days_until_squirt = 15 - (days_since_base % 15) if not is_squirt_day else 0
        
        return jsonify({
            'is_squirt_day': is_squirt_day,
            'days_until_squirt': days_until_squirt,
            'location': 'WoD Garrison',
            'message': '🎉 SQUIRT DAY! Check your Garrison!' if is_squirt_day else f'Squirt in {days_until_squirt} days',
            'note': 'Check if Pet Battle Week is active for SUPER SQUIRT bonus!'
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/strategy/fetch')
def fetch_strategy():
    """Fetch a strategy for a given NPC"""
    npc_name = request.args.get('npc_name')
    if not npc_name:
        return jsonify({"error": "Missing npc_name parameter"}), 400
        
    strategy = strategy_manager.get_strategy(npc_name)
    
    if strategy:
        return jsonify({
            "found": True,
            "strategy": strategy
        })
    else:
        return jsonify({
            "found": False,
            "message": "Strategy not found in local database."
        })

if __name__ == '__main__':
    update_stats()
    print("🌐 Starting PetWeaver Desktop App on http://127.0.0.1:5003")
    app.run(debug=False, port=5003)
