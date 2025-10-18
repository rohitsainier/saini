"""Configuration management."""

import json
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()


class Config:
    """Configuration manager."""
    
    def __init__(self):
        self.config_dir = Path.home() / '.saini'
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / 'config.json'
        
        self.defaults = {
            'pomodoro_enabled': False,
            'pomodoro_work_time': 1500,  # 25 minutes
            'pomodoro_break_time': 300,   # 5 minutes
            'pomodoro_long_break': 900,   # 15 minutes
            'idle_detection_enabled': False,
            'idle_threshold': 600,  # 10 minutes
        }
        
        self.load()
    
    def load(self):
        """Load configuration from file."""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                data = json.load(f)
            for key, value in data.items():
                setattr(self, key, value)
        else:
            for key, value in self.defaults.items():
                setattr(self, key, value)
            self.save()
    
    def save(self):
        """Save configuration to file."""
        data = {
            key: getattr(self, key)
            for key in self.defaults.keys()
        }
        with open(self.config_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def set_pomodoro(self, enabled):
        """Enable/disable Pomodoro mode."""
        self.pomodoro_enabled = enabled
        self.save()
        
        if enabled:
            console.print("✓ Pomodoro mode enabled", style="green")
        else:
            console.print("✓ Pomodoro mode disabled", style="yellow")
    
    def set_idle_detection(self, enabled):
        """Enable/disable idle detection."""
        self.idle_detection_enabled = enabled
        self.save()
        
        if enabled:
            console.print("✓ Idle detection enabled", style="green")
        else:
            console.print("✓ Idle detection disabled", style="yellow")
    
    def set_idle_threshold(self, minutes):
        """Set idle threshold in minutes."""
        self.idle_threshold = minutes * 60
        self.save()
        console.print(f"✓ Idle threshold set to {minutes} minutes", style="green")
    
    def show(self):
        """Display current configuration."""
        table = Table(title="Time Tracker Configuration", show_header=True, header_style="bold cyan")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="yellow")
        
        table.add_row("Pomodoro Mode", "✓ Enabled" if self.pomodoro_enabled else "✗ Disabled")
        table.add_row("Pomodoro Work Time", f"{self.pomodoro_work_time // 60} minutes")
        table.add_row("Pomodoro Break Time", f"{self.pomodoro_break_time // 60} minutes")
        table.add_row("Pomodoro Long Break", f"{self.pomodoro_long_break // 60} minutes")
        table.add_row("Idle Detection", "✓ Enabled" if self.idle_detection_enabled else "✗ Disabled")
        table.add_row("Idle Threshold", f"{self.idle_threshold // 60} minutes")
        
        console.print(table)