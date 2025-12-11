# Holocron Ecosystem Ports

This document defines the reserved ports for the Holocron ecosystem to prevent conflicts.

| Service | Port | Description |
| :--- | :--- | :--- |
| **Holocron Server** | `5001` | The main ERP dashboard and API server (`server.py`). |
| **PetWeaver** | `5002` | The Pet Battle simulation engine (`app.py`). |
| **SkillWeaver** | `5003` | Talent and rotation optimization service (`skillweaver_server.py`). |
| **GoblinStack** | `5004` | Gold making and auction house analytics (`goblinstack_server.py`). |

## Troubleshooting
If you encounter a "Port already in use" error:
1. Run `lsof -i :<PORT>` to see what is holding the port.
2. Run `kill -9 <PID>` to terminate the process.
3. Or use the helper script: `./stop_all.sh`.
