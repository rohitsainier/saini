"""Core time tracking functionality."""

import os
import time
from datetime import datetime
from pathlib import Path
import git
from rich.console import Console
from rich.panel import Panel

from .config import Config
from .pomodoro import PomodoroTimer
from .idle_detection import IdleDetector
from .utils import format_duration, get_project_name, get_branch_name

console = Console()


class TimeTracker:
    """Main time tracker class."""
    
    def __init__(self):
        self.config = Config()
        self.data_dir = Path.home() / '.saini'
        self.data_dir.mkdir(exist_ok=True)
        
        self.sessions_file = self.data_dir / 'sessions.csv'
        self.current_session_file = self.data_dir / 'current_session'
        self.paused_session_file = self.data_dir / 'paused_session'
        
        self._init_sessions_file()
        
    def _init_sessions_file(self):
        """Initialize sessions CSV file if it doesn't exist."""
        if not self.sessions_file.exists():
            with open(self.sessions_file, 'w') as f:
                f.write('project,branch,start_time,end_time,duration_seconds,description,paused_duration\n')
    
    def start(self, description=None):
        """Start tracking time."""
        if self.current_session_file.exists():
            console.print("⚠ Session already active. Stop it first or use 'switch'.", style="yellow")
            self.status()
            return
        
        project = get_project_name()
        branch = get_branch_name()
        start_time = int(time.time())
        
        session_data = {
            'project': project,
            'branch': branch,
            'start_time': start_time,
            'description': description or '',
            'paused_duration': 0
        }
        
        # Save session
        with open(self.current_session_file, 'w') as f:
            f.write(f"{project}|{branch}|{start_time}|{description}|0\n")
        
        # Start features
        if self.config.pomodoro_enabled:
            PomodoroTimer(self.config).start()
        
        if self.config.idle_detection_enabled:
            IdleDetector(self.config).start()
        
        # Display
        console.print("✓ Started tracking", style="green bold")
        console.print(f"  Project: [cyan]{project}[/cyan]")
        console.print(f"  Branch:  [cyan]{branch}[/cyan]")
        if description:
            console.print(f"  Task:    [cyan]{description}[/cyan]")
        console.print(f"  Time:    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.config.pomodoro_enabled:
            console.print("  🍅 Pomodoro mode enabled", style="magenta")
        
        if self.config.idle_detection_enabled:
            console.print(f"  👁 Idle detection enabled ({self.config.idle_threshold // 60} min)", style="blue")
    
    def stop(self):
        """Stop tracking time."""
        if not self.current_session_file.exists():
            console.print("✗ No active session", style="red")
            return
        
        # Read session
        with open(self.current_session_file, 'r') as f:
            line = f.read().strip()
        
        parts = line.split('|')
        project = parts[0]
        branch = parts[1]
        start_time = int(parts[2])
        description = parts[3] if len(parts) > 3 else ''
        paused_duration = int(parts[4]) if len(parts) > 4 else 0
        
        end_time = int(time.time())
        total_duration = end_time - start_time - paused_duration
        
        # Save to CSV
        with open(self.sessions_file, 'a') as f:
            start_dt = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
            end_dt = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'{project},{branch},{start_dt},{end_dt},{total_duration},"{description}",{paused_duration}\n')
        
        # Clean up
        self.current_session_file.unlink()
        if self.paused_session_file.exists():
            self.paused_session_file.unlink()
        
        # Stop features
        PomodoroTimer(self.config).stop()
        IdleDetector(self.config).stop()
        
        # Display
        console.print("✓ Stopped tracking", style="green bold")
        console.print(f"  Project:  [cyan]{project}[/cyan]")
        console.print(f"  Branch:   [cyan]{branch}[/cyan]")
        console.print(f"  Duration: [cyan]{format_duration(total_duration)}[/cyan]")
        if paused_duration > 0:
            console.print(f"  Paused:   [yellow]{format_duration(paused_duration)}[/yellow]")
    
    def switch(self, description=None):
        """Switch to a new session."""
        if self.current_session_file.exists():
            console.print("Stopping current session...", style="yellow")
            self.stop()
            console.print()
        
        self.start(description)
    
    def pause(self):
        """Pause current session."""
        if not self.current_session_file.exists():
            console.print("✗ No active session", style="red")
            return
        
        if self.paused_session_file.exists():
            console.print("⚠ Session already paused", style="yellow")
            return
        
        # Read current session
        with open(self.current_session_file, 'r') as f:
            session_data = f.read().strip()
        
        pause_time = int(time.time())
        
        # Save paused state
        with open(self.paused_session_file, 'w') as f:
            f.write(f"{session_data}|{pause_time}\n")
        
        console.print("⏸ Session paused", style="yellow bold")
        console.print("  Use 'saini resume' to continue")
    
    def resume(self):
        """Resume paused session."""
        if not self.paused_session_file.exists():
            console.print("✗ No paused session", style="red")
            return
        
        # Read paused session
        with open(self.paused_session_file, 'r') as f:
            line = f.read().strip()
        
        parts = line.split('|')
        project = parts[0]
        branch = parts[1]
        start_time = int(parts[2])
        description = parts[3]
        prev_paused = int(parts[4])
        pause_start = int(parts[5])
        
        resume_time = int(time.time())
        this_pause = resume_time - pause_start
        total_paused = prev_paused + this_pause
        
        # Update current session
        with open(self.current_session_file, 'w') as f:
            f.write(f"{project}|{branch}|{start_time}|{description}|{total_paused}\n")
        
        # Remove paused state
        self.paused_session_file.unlink()
        
        # Restart idle detection
        if self.config.idle_detection_enabled:
            IdleDetector(self.config).start()
        
        console.print("▶ Session resumed", style="green bold")
        console.print(f"  Was paused for: [yellow]{format_duration(this_pause)}[/yellow]")
    
    def status(self):
        """Show current session status."""
        # Check if paused
        if self.paused_session_file.exists():
            with open(self.paused_session_file, 'r') as f:
                line = f.read().strip()
            
            parts = line.split('|')
            project = parts[0]
            branch = parts[1]
            description = parts[3]
            pause_start = int(parts[5])
            pause_duration = int(time.time()) - pause_start
            
            console.print(Panel.fit(
                f"[yellow]⏸ Session Paused[/yellow]\n\n"
                f"  Project: [cyan]{project}[/cyan]\n"
                f"  Branch:  [cyan]{branch}[/cyan]\n"
                f"  Task:    [cyan]{description}[/cyan]\n"
                f"  Paused:  [yellow]{format_duration(pause_duration)}[/yellow]\n\n"
                f"  Use [green]saini resume[/green] to continue",
                title="Time Tracker",
                border_style="yellow"
            ))
            return
        
        # Check if active
        if not self.current_session_file.exists():
            console.print(Panel.fit(
                "[yellow]⊘ No active session[/yellow]\n\n"
                "  Use [green]saini start \"task description\"[/green] to begin tracking",
                title="Time Tracker",
                border_style="yellow"
            ))
            return
        
        # Read active session
        with open(self.current_session_file, 'r') as f:
            line = f.read().strip()
        
        parts = line.split('|')
        project = parts[0]
        branch = parts[1]
        start_time = int(parts[2])
        description = parts[3] if len(parts) > 3 else ''
        paused_duration = int(parts[4]) if len(parts) > 4 else 0
        
        current_time = int(time.time())
        active_duration = current_time - start_time - paused_duration
        
        status_text = (
            f"[green]⚡ Active Session[/green]\n\n"
            f"  Project:  [cyan]{project}[/cyan]\n"
            f"  Branch:   [cyan]{branch}[/cyan]\n"
        )
        
        if description:
            status_text += f"  Task:     [cyan]{description}[/cyan]\n"
        
        start_dt = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
        status_text += (
            f"  Started:  {start_dt}\n"
            f"  Duration: [cyan]{format_duration(active_duration)}[/cyan]"
        )
        
        if paused_duration > 0:
            status_text += f"\n  Paused:   [yellow]{format_duration(paused_duration)}[/yellow]"
        
        # Add pomodoro status
        if self.config.pomodoro_enabled:
            pomodoro_status = PomodoroTimer(self.config).get_status()
            if pomodoro_status:
                status_text += f"\n\n{pomodoro_status}"
        
        console.print(Panel.fit(
            status_text,
            title="Time Tracker",
            border_style="green"
        ))