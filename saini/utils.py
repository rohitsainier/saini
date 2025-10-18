"""Utility functions."""

import os
from pathlib import Path
import git


def format_duration(seconds):
    """Format duration in seconds to human-readable string."""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"


def get_project_name():
    """Get current project name from git or directory."""
    try:
        repo = git.Repo(Path.cwd(), search_parent_directories=True)
        return Path(repo.working_dir).name
    except (git.InvalidGitRepositoryError, git.GitCommandError):
        return Path.cwd().name


def get_branch_name():
    """Get current git branch name."""
    try:
        repo = git.Repo(Path.cwd(), search_parent_directories=True)
        return repo.active_branch.name
    except (git.InvalidGitRepositoryError, git.GitCommandError, TypeError):
        return "no-git"


def send_notification(title, message):
    """Send desktop notification."""
    try:
        # macOS
        if os.system("which osascript > /dev/null 2>&1") == 0:
            os.system(f'osascript -e \'display notification "{message}" with title "{title}" sound name "Glass"\'')
        # Linux
        elif os.system("which notify-send > /dev/null 2>&1") == 0:
            os.system(f'notify-send "{title}" "{message}"')
        else:
            print(f"🔔 {title}: {message}")
    except Exception:
        pass