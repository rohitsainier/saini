"""Reporting functionality."""

import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
from rich.console import Console
from rich.table import Table
import json

from .utils import format_duration

console = Console()


class Reports:
    """Report generator."""
    
    def __init__(self):
        self.sessions_file = Path.home() / '.saini' / 'sessions.csv'
    
    def _load_data(self):
        """Load sessions data."""
        if not self.sessions_file.exists():
            return pd.DataFrame()
        
        df = pd.read_csv(self.sessions_file)
        df['start_time'] = pd.to_datetime(df['start_time'])
        df['end_time'] = pd.to_datetime(df['end_time'])
        return df
    
    def today(self):
        """Show today's report."""
        df = self._load_data()
        if df.empty:
            console.print("No tracking data found", style="yellow")
            return
        
        today = datetime.now().date()
        df_today = df[df['start_time'].dt.date == today]
        
        if df_today.empty:
            console.print("No sessions recorded today", style="yellow")
            return
        
        table = Table(title=f"📅 Today ({today})", show_header=True, header_style="bold cyan")
        table.add_column("Project", style="cyan")
        table.add_column("Branch", style="green")
        table.add_column("Duration", style="yellow")
        table.add_column("Description", style="white")
        
        for _, row in df_today.iterrows():
            table.add_row(
                row['project'],
                row['branch'],
                format_duration(row['duration_seconds']),
                row['description']
            )
        
        console.print(table)
        console.print(f"\nTotal: {format_duration(df_today['duration_seconds'].sum())}", style="bold green")
    
    def yesterday(self):
        """Show yesterday's report."""
        df = self._load_data()
        if df.empty:
            console.print("No tracking data found", style="yellow")
            return
        
        yesterday = (datetime.now() - timedelta(days=1)).date()
        df_yesterday = df[df['start_time'].dt.date == yesterday]
        
        if df_yesterday.empty:
            console.print("No sessions recorded yesterday", style="yellow")
            return
        
        console.print(f"📅 Yesterday ({yesterday})", style="cyan bold")
        
        by_project = df_yesterday.groupby('project')['duration_seconds'].sum()
        for project, duration in by_project.items():
            console.print(f"  {project}: {format_duration(duration)}")
        
        console.print(f"\nTotal: {format_duration(df_yesterday['duration_seconds'].sum())}", style="bold green")
    
    def week(self):
        """Show this week's report."""
        df = self._load_data()
        if df.empty:
            console.print("No tracking data found", style="yellow")
            return
        
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        df_week = df[df['start_time'].dt.date >= week_start]
        
        if df_week.empty:
            console.print("No sessions recorded this week", style="yellow")
            return
        
        console.print(f"📅 This Week (starting {week_start})", style="cyan bold")
        console.print()
        
        by_project = df_week.groupby('project')['duration_seconds'].sum()
        console.print("By Project:", style="bold")
        for project, duration in by_project.items():
            console.print(f"  {project}: {format_duration(duration)}")
        
        console.print(f"\nTotal: {format_duration(df_week['duration_seconds'].sum())}", style="bold green")
    
    def by_project(self, project_name=None):
        """Show report for specific project."""
        df = self._load_data()
        if df.empty:
            console.print("No tracking data found", style="yellow")
            return
        
        if project_name:
            df_project = df[df['project'] == project_name]
        else:
            # Use current project
            from .utils import get_project_name
            project_name = get_project_name()
            df_project = df[df['project'] == project_name]
        
        if df_project.empty:
            console.print(f"No sessions found for project: {project_name}", style="yellow")
            return
        
        console.print(f"📊 Project: {project_name}", style="cyan bold")
        console.print()
        
        by_branch = df_project.groupby('branch')['duration_seconds'].sum()
        console.print("By Branch:", style="bold")
        for branch, duration in by_branch.items():
            console.print(f"  {branch}: {format_duration(duration)}")
        
        console.print(f"\nTotal: {format_duration(df_project['duration_seconds'].sum())}", style="bold green")
    
    def export(self, format_type, output_file=None):
        """Export data to file."""
        df = self._load_data()
        if df.empty:
            console.print("No tracking data to export", style="yellow")
            return
        
        if format_type == 'csv':
            output_file = output_file or 'timetrack-export.csv'
            df.to_csv(output_file, index=False)
            console.print(f"✓ Exported to {output_file}", style="green")
        
        elif format_type == 'json':
            output_file = output_file or 'timetrack-export.json'
            df.to_json(output_file, orient='records', indent=2, date_format='iso')
            console.print(f"✓ Exported to {output_file}", style="green")