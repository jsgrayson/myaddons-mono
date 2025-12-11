#!/bin/bash
echo 'Checking Goblin services...'
pgrep -f uvicorn && echo 'Backend: OK' || echo 'Backend: DOWN'
