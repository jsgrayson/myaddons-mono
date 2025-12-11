import os
import subprocess
from datetime import datetime

class GitManager:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self._init_repo()

    def _init_repo(self):
        if not os.path.exists(os.path.join(self.repo_path, ".git")):
            try:
                os.makedirs(self.repo_path, exist_ok=True)
                subprocess.run(["git", "init"], cwd=self.repo_path, check=True)
                print(f"[Timekeeper] Initialized Git repo at {self.repo_path}")
            except Exception as e:
                print(f"[Timekeeper] Git init failed: {e}")

    def commit_backup(self, message=None):
        """Commits all files in the repo path."""
        try:
            if not message:
                message = f"Auto-Backup: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            subprocess.run(["git", "add", "."], cwd=self.repo_path, check=True)
            subprocess.run(["git", "commit", "-m", message], cwd=self.repo_path, check=True)
            print(f"[Timekeeper] Backup committed: {message}")
            return True
        except Exception as e:
            print(f"[Timekeeper] Commit failed: {e}")
            return False
