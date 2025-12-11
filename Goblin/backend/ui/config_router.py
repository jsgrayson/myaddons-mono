from fastapi import APIRouter, HTTPException
import os
import shutil
import datetime

router = APIRouter()

CONFIG_DIR = "backend/config"

ALLOWED_EXT = [".yaml", ".yml", ".json", ".toml", ".env", ".ini"]


def list_config_files():
    files = []
    for f in os.listdir(CONFIG_DIR):
        full = os.path.join(CONFIG_DIR, f)
        if os.path.isfile(full):
            for ext in ALLOWED_EXT:
                if f.endswith(ext):
                    files.append(f)
    return sorted(files)


@router.get("/ui/config/list")
async def get_config_list():
    return {"files": list_config_files()}


@router.get("/ui/config/load/{filename}")
async def load_config(filename: str):
    path = os.path.join(CONFIG_DIR, filename)

    if not os.path.exists(path):
        raise HTTPException(404, "File not found")

    with open(path, "r") as f:
        content = f.read()

    return {"filename": filename, "content": content}


@router.post("/ui/config/save/{filename}")
async def save_config(filename: str, data: dict):
    content = data.get("content", "")
    path = os.path.join(CONFIG_DIR, filename)

    if not os.path.exists(path):
        raise HTTPException(404, "File not found")

    # Backup old file
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = f"{path}.bak-{timestamp}"
    shutil.copy(path, backup_path)

    # Save new file
    with open(path, "w") as f:
        f.write(content)

    return {"status": "ok", "backup": backup_path}
