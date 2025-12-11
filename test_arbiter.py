import time
import os
import threading
from arbiter_engine import ArbiterEngine
from skillweaver_engine import SkillWeaverEngine

# Mock Config
LOG_PATH = "mock_combat_log.txt"

def write_log_line(line):
    with open(LOG_PATH, "a") as f:
        f.write(line + "\n")

def test_arbiter():
    print("🧪 Testing The Arbiter...")
    
    # Setup
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)
    
    # Create empty log
    with open(LOG_PATH, "w") as f:
        f.write("Log Start\n")
        
    # Initialize Engines
    # Need to patch LOG_PATH in engines or use dependency injection
    # For this test, we'll just monkey patch the module level variable if possible
    # or rely on the engine using the same file if we set it up right.
    
    # Actually, ArbiterEngine uses self.log_path. SkillWeaver uses global LOG_PATH.
    # We need to ensure they point to our mock file.
    
    skillweaver = SkillWeaverEngine()
    # Patch SkillWeaver
    import skillweaver_engine
    skillweaver_engine.LOG_PATH = LOG_PATH
    skillweaver.start()
    
    arbiter = ArbiterEngine(skillweaver)
    arbiter.log_path = LOG_PATH # Patch Arbiter
    arbiter.start()
    
    time.sleep(1) # Let threads start
    
    # 1. Simulate "Correct" Cast
    # SkillWeaver expects BLOODTHIRST (SpellID 23881) by default
    print("📝 Simulating Correct Cast (Bloodthirst)...")
    timestamp = time.strftime("%m/%d %H:%M:%S.000")
    line = f"{timestamp},SPELL_CAST_SUCCESS,PlayerGUID,\"MyPlayerName\",TargetGUID,\"Target\",23881,\"Bloodthirst\",0x1,100,0,0,0,0,0,0,0,0"
    write_log_line(line)
    time.sleep(0.5)
    
    status = arbiter.get_status()
    print(f"Mistakes: {status['mistakes']}")
    assert status['mistakes'] == 0
    
    # 2. Simulate "Wrong" Cast
    # Cast Heroic Strike (SpellID 12345) instead
    print("📝 Simulating Wrong Cast (Heroic Strike)...")
    line = f"{timestamp},SPELL_CAST_SUCCESS,PlayerGUID,\"MyPlayerName\",TargetGUID,\"Target\",12345,\"Heroic Strike\",0x1,100,0,0,0,0,0,0,0,0"
    write_log_line(line)
    time.sleep(0.5)
    
    status = arbiter.get_status()
    print(f"Mistakes: {status['mistakes']}")
    assert status['mistakes'] == 1
    
    # 3. Verify SkillWeaver Feedback
    print(f"SkillWeaver Mistakes Logged: {len(skillweaver.mistakes)}")
    assert len(skillweaver.mistakes) == 1
    assert skillweaver.mistakes[0]['actual'] == 12345
    
    # Cleanup
    skillweaver.stop()
    arbiter.stop()
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)
        
    print("✅ Test Passed!")

if __name__ == "__main__":
    test_arbiter()
