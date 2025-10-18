"""Command-line interface for Saini."""

import click
from rich.console import Console
from pathlib import Path

from .tracker import TimeTracker
from .config import Config
from .reports import Reports
from .tree import ProjectTree

console = Console()

@click.group(invoke_without_command=True)
@click.pass_context
@click.version_option(version="1.0.0", prog_name="Saini")
def main(ctx):
    """Saini - Developer productivity tools."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(status)


# ============================================================================
# TIME TRACKING COMMANDS
# ============================================================================

@main.command()
@click.argument('description', required=False)
def start(description):
    """Start tracking time."""
    tracker = TimeTracker()
    tracker.start(description)


@main.command()
def stop():
    """Stop current session."""
    tracker = TimeTracker()
    tracker.stop()


@main.command()
@click.argument('description', required=False)
def switch(description):
    """Switch to a new session (stops current)."""
    tracker = TimeTracker()
    tracker.switch(description)


@main.command()
def pause():
    """Pause current session."""
    tracker = TimeTracker()
    tracker.pause()


@main.command()
def resume():
    """Resume paused session."""
    tracker = TimeTracker()
    tracker.resume()


@main.command()
def status():
    """Show current session status."""
    tracker = TimeTracker()
    tracker.status()


# ============================================================================
# CONFIGURATION COMMANDS
# ============================================================================

@main.group()
def config():
    """Configure Saini settings."""
    pass


@config.command(name='show')
def config_show():
    """Show current configuration."""
    cfg = Config()
    cfg.show()


@config.command(name='pomodoro')
@click.argument('value', type=click.Choice(['on', 'off']))
def config_pomodoro(value):
    """Enable/disable Pomodoro mode."""
    cfg = Config()
    cfg.set_pomodoro(value == 'on')


@config.command(name='idle')
@click.argument('value', type=click.Choice(['on', 'off']))
def config_idle(value):
    """Enable/disable idle detection."""
    cfg = Config()
    cfg.set_idle_detection(value == 'on')


@config.command(name='idle-time')
@click.argument('minutes', type=int)
def config_idle_time(minutes):
    """Set idle threshold in minutes."""
    cfg = Config()
    cfg.set_idle_threshold(minutes)


# ============================================================================
# REPORT COMMANDS
# ============================================================================

@main.group()
def report():
    """Generate time tracking reports."""
    pass


@report.command(name='today')
def report_today():
    """Show today's time tracking."""
    reports = Reports()
    reports.today()


@report.command(name='yesterday')
def report_yesterday():
    """Show yesterday's time tracking."""
    reports = Reports()
    reports.yesterday()


@report.command(name='week')
def report_week():
    """Show this week's time tracking."""
    reports = Reports()
    reports.week()


@report.command(name='project')
@click.argument('project_name', required=False)
def report_project(project_name):
    """Show report for specific project."""
    reports = Reports()
    reports.by_project(project_name)


@main.command()
@click.argument('format', type=click.Choice(['csv', 'json']))
@click.option('--output', '-o', help='Output file name')
def export(format, output):
    """Export tracking data."""
    reports = Reports()
    reports.export(format, output)


# ============================================================================
# PROJECT TREE COMMANDS
# ============================================================================

@main.command()
@click.option('--path', '-p', default='.', help='Root path to generate tree from')
@click.option('--depth', '-d', type=int, help='Maximum depth to traverse')
@click.option('--hidden', '-a', is_flag=True, help='Show hidden files')
@click.option('--no-icons', is_flag=True, help='Disable icons')
@click.option('--size', '-s', is_flag=True, help='Show file sizes')
@click.option('--output', '-o', help='Save tree to file')
@click.option('--format', '-f', type=click.Choice(['text', 'json']), default='text', help='Output format')
@click.option('--ignore', '-i', multiple=True, help='Additional patterns to ignore')
def tree(path, depth, hidden, no_icons, size, output, format, ignore):
    """Generate project structure tree.
    
    Examples:
        saini tree                          # Show tree of current directory
        saini tree -p /path/to/project      # Show tree of specific path
        saini tree -d 3                     # Limit depth to 3 levels
        saini tree -a                       # Show hidden files
        saini tree -s                       # Show file sizes
        saini tree -o tree.txt              # Save to file
        saini tree -i "*.pyc" -i "test_*"   # Ignore additional patterns
    """
    project_tree = ProjectTree(
        root_path=path,
        max_depth=depth,
        show_hidden=hidden,
        custom_ignore=set(ignore) if ignore else None,
        show_size=size,
        icons=not no_icons
    )
    
    if output:
        project_tree.save_to_file(output, format)
    else:
        project_tree.generate()


@main.command(name='tree-ignore')
@click.option('--path', '-p', default='.', help='Root path')
def tree_ignore(path):
    """Generate tree respecting .gitignore patterns."""
    console.print("🚧 Feature coming soon: Tree with .gitignore support", style="yellow")
    # TODO: Implement gitignore-aware tree


if __name__ == '__main__':
    main()