#!/bin/bash
echo "Launching Holocron Suite..."

# Main Server (Port 5005)
osascript -e 'tell app "Terminal" to do script "cd /Users/jgrayson/Documents/holocron && python3 server.py"'

# SkillWeaver (Port 5003)
osascript -e 'tell app "Terminal" to do script "cd /Users/jgrayson/Documents/holocron && python3 templates/skillweaver_server.py"'

# GoblinStack (Port 5004)
osascript -e 'tell app "Terminal" to do script "cd /Users/jgrayson/Documents/holocron && python3 templates/goblinstack_server.py"'

echo "Check your Terminal windows! Servers should be running."
