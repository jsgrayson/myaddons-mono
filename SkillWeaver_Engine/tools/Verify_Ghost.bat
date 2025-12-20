@echo off
echo --- SkillWeaver Second System Diagnostic ---
set /p com_port="Enter the COM Port for the Logitech Device (e.g., COM3): "
mode %com_port% BAUD=250000 PARITY=n DATA=8 STOP=1
echo.
echo Sending Heartbeat to %com_port%...
echo . > %com_port%
echo.
echo If the RX LED on the Arduino flickered, the bridge is OPEN.
pause
