import requests
from bs4 import BeautifulSoup
import os
import re

# Configuration - ALL CLASSES WITH ALL MODES
TARGETS = [
    # DEATH KNIGHT
    {"class": "DEATHKNIGHT", "spec": "Blood", "spec_id": "250", "modes": {
        "Raid": {"rotation": "https://www.icy-veins.com/wow/blood-death-knight-tank-pve-rotation-cooldowns-abilities", "talents": "https://www.icy-veins.com/wow/blood-death-knight-tank-pve-spec-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/death-knight/blood/raid-tank"},
        "MythicPlus": {"rotation": "https://www.icy-veins.com/wow/blood-death-knight-tank-pve-mythic-plus-tips", "talents": "https://www.icy-veins.com/wow/blood-death-knight-tank-pve-mythic-plus-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/death-knight/blood/mythic-plus-tank"},
        "Delves": {"rotation": "https://www.icy-veins.com/wow/blood-death-knight-tank-pve-rotation-cooldowns-abilities", "talents": "https://www.icy-veins.com/wow/blood-death-knight-tank-pve-spec-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/death-knight/blood/raid-tank"},
        "PvP": {"rotation": "https://www.icy-veins.com/wow/blood-death-knight-pvp-tank-rotation", "talents": "https://www.icy-veins.com/wow/blood-death-knight-pvp-tank-spec-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/death-knight/blood/pvp-arena"}
    }},
    {"class": "DEATHKNIGHT", "spec": "Frost", "spec_id": "251", "modes": {
        "Raid": {"rotation": "https://www.icy-veins.com/wow/frost-death-knight-pve-dps-rotation-cooldowns-abilities", "talents": "https://www.icy-veins.com/wow/frost-death-knight-pve-dps-spec-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/death-knight/frost/raid-pve-dps"},
        "MythicPlus": {"rotation": "https://www.icy-veins.com/wow/frost-death-knight-pve-dps-mythic-plus-tips", "talents": "https://www.icy-veins.com/wow/frost-death-knight-pve-dps-mythic-plus-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/death-knight/frost/mythic-plus-pve-dps"},
        "Delves": {"rotation": "https://www.icy-veins.com/wow/frost-death-knight-pve-dps-rotation-cooldowns-abilities", "talents": "https://www.icy-veins.com/wow/frost-death-knight-pve-dps-spec-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/death-knight/frost/raid-pve-dps"},
        "PvP": {"rotation": "https://www.icy-veins.com/wow/frost-death-knight-pvp-dps-rotation", "talents": "https://www.icy-veins.com/wow/frost-death-knight-pvp-dps-spec-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/death-knight/frost/pvp-arena"}
    }},
    {"class": "DEATHKNIGHT", "spec": "Unholy", "spec_id": "252", "modes": {
        "Raid": {"rotation": "https://www.icy-veins.com/wow/unholy-death-knight-pve-dps-rotation-cooldowns-abilities", "talents": "https://www.icy-veins.com/wow/unholy-death-knight-pve-dps-spec-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/death-knight/unholy/raid-pve-dps"},
        "MythicPlus": {"rotation": "https://www.icy-veins.com/wow/unholy-death-knight-pve-dps-mythic-plus-tips", "talents": "https://www.icy-veins.com/wow/unholy-death-knight-pve-dps-mythic-plus-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/death-knight/unholy/mythic-plus-pve-dps"},
        "Delves": {"rotation": "https://www.icy-veins.com/wow/unholy-death-knight-pve-dps-rotation-cooldowns-abilities", "talents": "https://www.icy-veins.com/wow/unholy-death-knight-pve-dps-spec-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/death-knight/unholy/raid-pve-dps"},
        "PvP": {"rotation": "https://www.icy-veins.com/wow/unholy-death-knight-pvp-dps-rotation", "talents": "https://www.icy-veins.com/wow/unholy-death-knight-pvp-dps-spec-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/death-knight/unholy/pvp-arena"}
    }},
    
    # DEMON HUNTER
    {"class": "DEMONHUNTER", "spec": "Havoc", "spec_id": "577", "modes": {
        "Raid": {"rotation": "https://www.icy-veins.com/wow/havoc-demon-hunter-pve-dps-rotation-cooldowns-abilities", "talents": "https://www.icy-veins.com/wow/havoc-demon-hunter-pve-dps-spec-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/demon-hunter/havoc/raid-pve-dps"},
        "MythicPlus": {"rotation": "https://www.icy-veins.com/wow/havoc-demon-hunter-pve-dps-mythic-plus-tips", "talents": "https://www.icy-veins.com/wow/havoc-demon-hunter-pve-dps-mythic-plus-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/demon-hunter/havoc/mythic-plus-pve-dps"},
        "Delves": {"rotation": "https://www.icy-veins.com/wow/havoc-demon-hunter-pve-dps-rotation-cooldowns-abilities", "talents": "https://www.icy-veins.com/wow/havoc-demon-hunter-pve-dps-spec-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/demon-hunter/havoc/raid-pve-dps"},
        "PvP": {"rotation": "https://www.icy-veins.com/wow/havoc-demon-hunter-pvp-dps-rotation", "talents": "https://www.icy-veins.com/wow/havoc-demon-hunter-pvp-dps-spec-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/demon-hunter/havoc/pvp-arena"}
    }},
    {"class": "DEMONHUNTER", "spec": "Vengeance", "spec_id": "581", "modes": {
        "Raid": {"rotation": "https://www.icy-veins.com/wow/vengeance-demon-hunter-tank-pve-rotation-cooldowns-abilities", "talents": "https://www.icy-veins.com/wow/vengeance-demon-hunter-tank-pve-spec-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/demon-hunter/vengeance/raid-tank"},
        "MythicPlus": {"rotation": "https://www.icy-veins.com/wow/vengeance-demon-hunter-tank-pve-mythic-plus-tips", "talents": "https://www.icy-veins.com/wow/vengeance-demon-hunter-tank-pve-mythic-plus-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/demon-hunter/vengeance/mythic-plus-tank"},
        "Delves": {"rotation": "https://www.icy-veins.com/wow/vengeance-demon-hunter-tank-pve-rotation-cooldowns-abilities", "talents": "https://www.icy-veins.com/wow/vengeance-demon-hunter-tank-pve-spec-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/demon-hunter/vengeance/raid-tank"},
        "PvP": {"rotation": "https://www.icy-veins.com/wow/vengeance-demon-hunter-pvp-tank-rotation", "talents": "https://www.icy-veins.com/wow/vengeance-demon-hunter-pvp-tank-spec-builds-talents", "wowhead": "https://www.wowhead.com/guide/classes/demon-hunter/vengeance/pvp-arena"}
    }},
