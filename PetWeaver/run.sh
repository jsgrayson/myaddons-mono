#!/bin/bash
# Run PetWeaver Backend on Port 8001

echo "Starting PetWeaver Backend..."
cd "$(dirname "$0")"
python3 app.py
