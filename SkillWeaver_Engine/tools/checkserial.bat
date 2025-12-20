@echo off
set /p port="Enter COM Port (e.g. COM3): "
mode %port% BAUD=250000 PARITY=n DATA=8 STOP=1
echo Testing Heartbeat on %port%...
echo . > %port%
echo Heartbeat sent. Check Arduino RX LED.
pause
