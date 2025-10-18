"""Pomodoro timer functionality."""

import time
import threading
from pathlib import Path

from .utils import send_notification, format_duration


class PomodoroTimer:
    """Pomodoro timer manager."""
    
    def __init__(self, config):
        self.config = config
        self.state_file = Path.home() / '.saini' / 'pomodoro_state'
        self.pid_file = Path.home() / '.saini' / 'pomodoro_pid'
    
    def start(self):
        """Start Pomodoro timer."""
        if not self.config.pomodoro_enabled:
            return
        
        # Start work session
        state = {
            'type': 'work',
            'start': int(time.time()),
            'duration': self.config.pomodoro_work_time,
            'count': 0
        }
        
        with open(self.state_file, 'w') as f:
            f.write(f"{state['type']}|{state['start']}|{state['duration']}|{state['count']}\n")
        
        # Start background timer
        thread = threading.Thread(target=self._timer_loop, daemon=True)
        thread.start()
    
    def _timer_loop(self):
        """Background timer loop."""
        while self.state_file.exists():
            with open(self.state_file, 'r') as f:
                line = f.read().strip()
            
            parts = line.split('|')
            session_type = parts[0]
            start = int(parts[1])
            duration = int(parts[2])
            count = int(parts[3])
            
            elapsed = int(time.time()) - start
            remaining = duration - elapsed
            
            if remaining <= 0:
                if session_type == 'work':
                    send_notification("Pomodoro Complete! 🍅", "Time for a break! (5 min)")
                    count += 1
                    
                    # Long break every 4 pomodoros
                    break_time = self.config.pomodoro_long_break if count % 4 == 0 else self.config.pomodoro_break_time
                    
                    with open(self.state_file, 'w') as f:
                        f.write(f"break|{int(time.time())}|{break_time}|{count}\n")
                else:
                    send_notification("Break Over! ⏰", "Ready to focus? Starting new pomodoro...")
                    
                    with open(self.state_file, 'w') as f:
                        f.write(f"work|{int(time.time())}|{self.config.pomodoro_work_time}|{count}\n")
            
            time.sleep(60)  # Check every minute
    
    def stop(self):
        """Stop Pomodoro timer."""
        if self.state_file.exists():
            self.state_file.unlink()
    
    def get_status(self):
        """Get current Pomodoro status."""
        if not self.state_file.exists():
            return None
        
        with open(self.state_file, 'r') as f:
            line = f.read().strip()
        
        parts = line.split('|')
        session_type = parts[0]
        start = int(parts[1])
        duration = int(parts[2])
        count = int(parts[3])
        
        elapsed = int(time.time()) - start
        remaining = duration - elapsed
        
        if session_type == 'work':
            return f"  [magenta]🍅 Pomodoro: Work Session #{count + 1}[/magenta]\n  Time Left: [yellow]{format_duration(remaining)}[/yellow]"
        else:
            return f"  [cyan]☕ Break Time[/cyan]\n  Time Left: [yellow]{format_duration(remaining)}[/yellow]"