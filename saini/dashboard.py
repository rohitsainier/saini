"""Live dashboard view."""

import time
from datetime import datetime
from rich.console import Console
from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

console = Console()


def create_dashboard(tracker):
    """Create live dashboard layout."""
    layout = Layout()
    
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3),
    )
    
    layout["main"].split_row(
        Layout(name="status"),
        Layout(name="stats"),
    )
    
    # Header
    layout["header"].update(Panel("🚀 Saini Dashboard - LIVE", style="bold magenta"))
    
    # Footer
    layout["footer"].update(Panel("[dim]Press Ctrl+C to exit[/dim]", style="dim"))
    
    return layout


def show_dashboard():
    """Show live updating dashboard."""
    from .tracker import TimeTracker
    from .reports import Reports
    
    tracker = TimeTracker()
    reports = Reports()
    
    layout = create_dashboard(tracker)
    
    try:
        with Live(layout, refresh_per_second=1, console=console):
            while True:
                # Update status panel
                layout["status"].update(tracker._generate_status_display())
                
                # Update stats panel
                stats_table = Table(title="Today's Stats", show_header=False)
                stats_table.add_row("Sessions", "3")
                stats_table.add_row("Total Time", "2h 45m")
                stats_table.add_row("Pomodoros", "5")
                
                layout["stats"].update(Panel(stats_table, border_style="blue"))
                
                time.sleep(1)
    except KeyboardInterrupt:
        console.print("\n✓ Dashboard closed", style="dim")