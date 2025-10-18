"""Idle detection based on git activity."""

import time
import threading
from pathlib import Path
import git

from .utils import send_notification


class IdleDetector:
    """Idle detection manager."""
    
    def __init__(self, config):
        self.config = config
        self.idle_file = Path.home() / '.saini' / 'idle_check'
        self.running = False
    
    def start(self):
        """Start idle detection."""
        if not self.config.idle_detection_enabled:
            return
        
        self._record_activity()
        
        # Start background checker
        self.running = True
        thread = threading.Thread(target=self._check_loop, daemon=True)
        thread.start()
    
    def _record_activity(self):
        """Record current git activity."""
        try:
            repo = git.Repo(Path.cwd(), search_parent_directories=True)
            last_commit = int(repo.head.commit.committed_date)
            status_count = len(repo.index.diff(None)) + len(repo.untracked_files)
        except (git.InvalidGitRepositoryError, git.GitCommandError):
            last_commit = 0
            status_count = 0
        
        with open(self.idle_file, 'w') as f:
            f.write(f"{last_commit}|{status_count}|{int(time.time())}\n")
    
    def _check_loop(self):
        """Background idle checking loop."""
        while self.running and self.idle_file.exists():
            time.sleep(60)  # Check every minute
            
            if not self.idle_file.exists():
                break
            
            with open(self.idle_file, 'r') as f:
                line = f.read().strip()
            
            parts = line.split('|')
            prev_commit = int(parts[0])
            prev_status = int(parts[1])
            last_check = int(parts[2])
            
            try:
                repo = git.Repo(Path.cwd(), search_parent_directories=True)
                curr_commit = int(repo.head.commit.committed_date)
                curr_status = len(repo.index.diff(None)) + len(repo.untracked_files)
                
                if curr_commit != prev_commit or curr_status != prev_status:
                    # Activity detected
                    self._record_activity()
                else:
                    # Check idle threshold
                    idle_time = int(time.time()) - last_check
                    if idle_time >= self.config.idle_threshold:
                        send_notification("Auto-Paused ⏸", f"No git activity for {idle_time // 60} min")
                        self._auto_pause()
                        break
            except (git.InvalidGitRepositoryError, git.GitCommandError):
                pass
    
    def _auto_pause(self):
        """Auto-pause the session."""
        # This would trigger pause in the tracker
        # For now, just send notification
        pass
    
    def stop(self):
        """Stop idle detection."""
        self.running = False
        if self.idle_file.exists():
            self.idle_file.unlink()