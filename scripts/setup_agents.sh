#!/bin/bash
set -e

################################################################################
# Agents Setup Script (SAFE VERSION)
################################################################################

BASE_DIR="$HOME/Documents/goblin-clean/agents"

echo "[Agents] Creating agent directories ..."

mkdir -p "$BASE_DIR/warden/logs"
mkdir -p "$BASE_DIR/tsm_brain/logs" "$BASE_DIR/tsm_brain/data"
mkdir -p "$BASE_DIR/gmail_archiver/logs"
mkdir -p "$BASE_DIR/bank_runner/logs"
mkdir -p "$BASE_DIR/ah_runner/logs"

################################################################################
# Helper to write text safely
################################################################################
write_file() {
    FILE="$1"
    shift
    printf "%s\n" "$@" > "$FILE"
}

################################################################################
# WARDEN
################################################################################

write_file "$BASE_DIR/warden/warden.py" \
"import time" \
"from loguru import logger" \
"" \
"class Warden:" \
"    def __init__(self):" \
"        logger.info(\"Warden agent initialized\")" \
"" \
"    def heartbeat(self):" \
"        logger.info(\"Warden heartbeat OK\")" \
"" \
"if __name__ == \"__main__\":" \
"    w = Warden()" \
"    while True:" \
"        w.heartbeat()" \
"        time.sleep(5)"

write_file "$BASE_DIR/warden/config.py" \
"INTERVAL = 5"

write_file "$BASE_DIR/warden/__init__.py" ""
write_file "$BASE_DIR/warden/logs/.gitkeep" ""

################################################################################
# TSM BRAIN
################################################################################

write_file "$BASE_DIR/tsm_brain/tsm_brain.py" \
"from loguru import logger" \
"from .model import TSMModel" \
"" \
"class TSMBrain:" \
"    def __init__(self):" \
"        self.model = TSMModel()" \
"        logger.info(\"TSM Brain initialized\")" \
"" \
"    def predict(self, item_id: int):" \
"        return self.model.predict_price(item_id)" \
"" \
"if __name__ == \"__main__\":" \
"    brain = TSMBrain()" \
"    print(brain.predict(123))"

write_file "$BASE_DIR/tsm_brain/model.py" \
"class TSMModel:" \
"    def predict_price(self, item_id: int) -> float:" \
"        return 42.0"

write_file "$BASE_DIR/tsm_brain/config.py" \
"MODEL_PATH = \"./models/model.pkl\""

write_file "$BASE_DIR/tsm_brain/__init__.py" ""
write_file "$BASE_DIR/tsm_brain/logs/.gitkeep" ""
write_file "$BASE_DIR/tsm_brain/data/.gitkeep" ""

################################################################################
# GMAIL ARCHIVER
################################################################################

write_file "$BASE_DIR/gmail_archiver/archiver.py" \
"from loguru import logger" \
"" \
"class GmailArchiver:" \
"    def archive(self):" \
"        logger.info(\"Archiving Gmail...\")" \
"        return True" \
"" \
"if __name__ == \"__main__\":" \
"    g = GmailArchiver()" \
"    g.archive()"

write_file "$BASE_DIR/gmail_archiver/config.py" \
"ARCHIVE_DAYS = 14"

write_file "$BASE_DIR/gmail_archiver/__init__.py" ""
write_file "$BASE_DIR/gmail_archiver/logs/.gitkeep" ""

################################################################################
# BANK RUNNER
################################################################################

write_file "$BASE_DIR/bank_runner/bank_runner.py" \
"from loguru import logger" \
"" \
"class BankRunner:" \
"    def run(self):" \
"        logger.info(\"Running bank operations...\")" \
"        return True" \
"" \
"if __name__ == \"__main__\":" \
"    r = BankRunner()" \
"    r.run()"

write_file "$BASE_DIR/bank_runner/config.py" \
"BANK_INTERVAL = 60"

write_file "$BASE_DIR/bank_runner/__init__.py" ""
write_file "$BASE_DIR/bank_runner/logs/.gitkeep" ""

################################################################################
# AH RUNNER
################################################################################

write_file "$BASE_DIR/ah_runner/ah_runner.py" \
"from loguru import logger" \
"" \
"class AHRunner:" \
"    def scan(self):" \
"        logger.info(\"Scanning Auction House...\")" \
"        return True" \
"" \
"if __name__ == \"__main__\":" \
"    a = AHRunner()" \
"    a.scan()"

write_file "$BASE_DIR/ah_runner/config.py" \
"SCAN_INTERVAL = 120"

write_file "$BASE_DIR/ah_runner/__init__.py" ""
write_file "$BASE_DIR/ah_runner/logs/.gitkeep" ""

################################################################################
# DONE
################################################################################

echo "[Agents] Agents created successfully."

