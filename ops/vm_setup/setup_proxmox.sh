#!/bin/bash
echo 'Configuring Proxmox VM for Goblin...'
apt update && apt install -y python3 python3-venv git
echo 'Proxmox VM setup complete.'
