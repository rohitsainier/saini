"""Project structure tree generator with best practices analysis."""

import os
from pathlib import Path
from rich.console import Console
from rich.tree import Tree
from rich.text import Text
from rich import box
from rich.panel import Panel
from rich.table import Table

from .analyzer import ProjectAnalyzer, Severity

console = Console()


class ProjectTree:
    """Generate and display project structure tree with analysis."""
    
    # Default ignore patterns
    DEFAULT_IGNORE = {
        # Version Control
        '.git', '.gitignore', '.gitattributes', '.gitmodules',
        '.svn', '.hg', '.bzr',
        
        # Dependencies
        'node_modules', 'bower_components', 'vendor', 'packages',
        'venv', 'env', '.env', '.venv', 'virtualenv',
        '__pycache__', '.pytest_cache', '.mypy_cache', '.tox',
        
        # Build outputs
        'dist', 'build', 'out', 'target', 'bin', 'obj',
        '*.egg-info', '.eggs',
        
        # IDE
        '.idea', '.vscode', '.vs', '*.swp', '*.swo', '*~',
        '.DS_Store', 'Thumbs.db',
        
        # Logs and databases
        '*.log', '*.sqlite', '*.db',
        'logs', 'log',
        
        # Others
        '.cache', 'coverage', 'htmlcov', '.coverage',
        'tmp', 'temp', '.tmp', '.temp',
    }
    
    # File type icons
    FILE_ICONS = {
        # Programming Languages
        '.py': '🐍',
        '.js': '📜',
        '.ts': '📘',
        '.jsx': '⚛️',
        '.tsx': '⚛️',
        '.java': '☕',
        '.cpp': '⚙️',
        '.c': '⚙️',
        '.h': '📋',
        '.go': '🔷',
        '.rs': '🦀',
        '.php': '🐘',
        '.rb': '💎',
        '.swift': '🍎',
        '.kt': '🅺',
        '.scala': '🔴',
        
        # Web
        '.html': '🌐',
        '.css': '🎨',
        '.scss': '🎨',
        '.sass': '🎨',
        '.less': '🎨',
        '.vue': '💚',
        
        # Data/Config
        '.json': '📋',
        '.yaml': '📋',
        '.yml': '📋',
        '.xml': '📋',
        '.toml': '📋',
        '.ini': '📋',
        '.conf': '📋',
        '.config': '📋',
        
        # Documentation
        '.md': '📝',
        '.txt': '📄',
        '.pdf': '📕',
        '.doc': '📘',
        '.docx': '📘',
        
        # Database
        '.sql': '🗄️',
        '.db': '🗄️',
        '.sqlite': '🗄️',
        
        # Images
        '.png': '🖼️',
        '.jpg': '🖼️',
        '.jpeg': '🖼️',
        '.gif': '🖼️',
        '.svg': '🖼️',
        '.ico': '🖼️',
        
        # Archives
        '.zip': '📦',
        '.tar': '📦',
        '.gz': '📦',
        '.rar': '📦',
        
        # Others
        '.sh': '🔧',
        '.bash': '🔧',
        '.zsh': '🔧',
        '.env': '🔐',
        '.lock': '🔒',
        'Dockerfile': '🐳',
        'docker-compose': '🐳',
        'Makefile': '🔨',
        'README': '📖',
        'LICENSE': '⚖️',
    }
    
    def __init__(self, root_path='.', max_depth=None, show_hidden=False, 
                 custom_ignore=None, show_size=False, icons=True, analyze=False):
        """
        Initialize ProjectTree.
        
        Args:
            root_path: Root directory to start from
            max_depth: Maximum depth to traverse (None for unlimited)
            show_hidden: Show hidden files/folders
            custom_ignore: Additional patterns to ignore
            show_size: Show file sizes
            icons: Show file type icons
            analyze: Perform structure analysis
        """
        self.root_path = Path(root_path).resolve()
        self.max_depth = max_depth
        self.show_hidden = show_hidden
        self.show_size = show_size
        self.icons = icons
        self.analyze = analyze
        
        # Combine default and custom ignore patterns
        self.ignore_patterns = self.DEFAULT_IGNORE.copy()
        if custom_ignore:
            self.ignore_patterns.update(custom_ignore)
        
        self.stats = {
            'files': 0,
            'dirs': 0,
            'total_size': 0,
        }
        
        # Analyzer
        self.analyzer = ProjectAnalyzer(self.root_path) if analyze else None
    
    def _should_ignore(self, path):
        """Check if path should be ignored."""
        name = path.name
        
        # Hidden files
        if not self.show_hidden and name.startswith('.'):
            return True
        
        # Check ignore patterns
        for pattern in self.ignore_patterns:
            if pattern.startswith('*'):
                # Extension pattern
                if name.endswith(pattern[1:]):
                    return True
            elif name == pattern or name.startswith(pattern):
                return True
        
        return False
    
    def _get_icon(self, path):
        """Get icon for file/folder."""
        if not self.icons:
            return ''
        
        if path.is_dir():
            return '📁 '
        
        # Check specific filenames first
        for key, icon in self.FILE_ICONS.items():
            if not key.startswith('.') and path.name.lower().startswith(key.lower()):
                return f'{icon} '
        
        # Check extension
        ext = path.suffix.lower()
        return self.FILE_ICONS.get(ext, '📄 ')
    
    def _format_size(self, size):
        """Format file size."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f}{unit}"
            size /= 1024.0
        return f"{size:.1f}TB"
    
    def _get_file_info(self, path):
        """Get formatted file information."""
        icon = self._get_icon(path)
        name = path.name
        
        if path.is_file() and self.show_size:
            try:
                size = path.stat().st_size
                self.stats['total_size'] += size
                return f"{icon}{name} [{self._format_size(size)}]"
            except (OSError, PermissionError):
                return f"{icon}{name} [?]"
        
        return f"{icon}{name}"
    
    def _build_tree(self, tree, path, prefix="", depth=0):
        """Recursively build tree structure."""
        if self.max_depth is not None and depth >= self.max_depth:
            return
        
        try:
            # Get all items in directory
            items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
            
            for item in items:
                if self._should_ignore(item):
                    continue
                
                if item.is_dir():
                    self.stats['dirs'] += 1
                    branch = tree.add(self._get_file_info(item), style="bold cyan")
                    self._build_tree(branch, item, prefix + "  ", depth + 1)
                else:
                    self.stats['files'] += 1
                    # Color code by file type
                    if item.suffix in ['.py', '.js', '.java', '.cpp', '.go']:
                        style = "green"
                    elif item.suffix in ['.html', '.css', '.json', '.yaml']:
                        style = "blue"
                    elif item.suffix in ['.md', '.txt']:
                        style = "yellow"
                    else:
                        style = "white"
                    
                    tree.add(self._get_file_info(item), style=style)
        
        except PermissionError:
            tree.add("[Permission Denied]", style="red italic")
    
    def generate(self):
        """Generate and display the tree with optional analysis."""
        # Create root tree
        root_info = f"{self._get_icon(self.root_path)}{self.root_path.name}"
        tree = Tree(root_info, style="bold magenta", guide_style="dim")
        
        # Build the tree
        self._build_tree(tree, self.root_path)
        
        # Display tree
        console.print()
        console.print(tree)
        console.print()
        
        # Display statistics
        stats_text = (
            f"📊 [cyan]{self.stats['dirs']}[/cyan] directories, "
            f"[green]{self.stats['files']}[/green] files"
        )
        
        if self.show_size:
            stats_text += f", Total size: [yellow]{self._format_size(self.stats['total_size'])}[/yellow]"
        
        console.print(Panel(stats_text, title="Statistics", border_style="blue"))
        
        # Perform analysis if requested
        if self.analyze and self.analyzer:
            self._display_analysis()
    
    def _display_analysis(self):
        """Display structure analysis and suggestions."""
        console.print()
        console.print("=" * 60, style="dim")
        console.print()
        
        # Project type
        console.print(Panel(
            f"[cyan]Project Type:[/cyan] [bold]{self.analyzer.project_type.upper()}[/bold]",
            title="📋 Analysis",
            border_style="cyan"
        ))
        console.print()
        
        # Run analysis
        suggestions = self.analyzer.analyze()
        
        # Health score
        score, grade = self.analyzer.get_health_score()
        score_color = "green" if score >= 75 else "yellow" if score >= 60 else "red"
        
        console.print(Panel(
            f"[bold {score_color}]{score}/100 - {grade}[/bold {score_color}]",
            title="🏆 Structure Health Score",
            border_style=score_color
        ))
        console.print()
        
        # Suggestions grouped by severity
        if suggestions:
            self._display_suggestions(suggestions)
        else:
            console.print(Panel(
                "[bold green]✓ No issues found! Your project structure looks great! 🎉[/bold green]",
                border_style="green"
            ))
        
        # Recommendations
        console.print()
        self._display_recommendations()
    
    def _display_suggestions(self, suggestions):
        """Display categorized suggestions."""
        # Group by severity
        errors = [s for s in suggestions if s.severity == Severity.ERROR]
        warnings = [s for s in suggestions if s.severity == Severity.WARNING]
        suggestions_list = [s for s in suggestions if s.severity == Severity.SUGGESTION]
        info = [s for s in suggestions if s.severity == Severity.INFO]
        
        # Display errors
        if errors:
            console.print("[bold red]❌ Errors (Must Fix):[/bold red]")
            for suggestion in errors:
                console.print(f"  • [red]{suggestion.message}[/red]")
                console.print(f"    [dim]{suggestion.details}[/dim]")
            console.print()
        
        # Display warnings
        if warnings:
            console.print("[bold yellow]⚠️  Warnings (Should Fix):[/bold yellow]")
            for suggestion in warnings:
                console.print(f"  • [yellow]{suggestion.message}[/yellow]")
                console.print(f"    [dim]{suggestion.details}[/dim]")
            console.print()
        
        # Display suggestions
        if suggestions_list:
            console.print("[bold cyan]💡 Suggestions (Consider):[/bold cyan]")
            for suggestion in suggestions_list[:5]:  # Show top 5
                console.print(f"  • [cyan]{suggestion.message}[/cyan]")
                console.print(f"    [dim]{suggestion.details}[/dim]")
            
            if len(suggestions_list) > 5:
                console.print(f"  [dim]... and {len(suggestions_list) - 5} more suggestions[/dim]")
            console.print()
        
        # Display info
        if info:
            console.print("[bold blue]ℹ️  Information:[/bold blue]")
            for suggestion in info[:3]:  # Show top 3
                console.print(f"  • [blue]{suggestion.message}[/blue]")
                console.print(f"    [dim]{suggestion.details}[/dim]")
            console.print()
    
    def _display_recommendations(self):
        """Display project-type specific recommendations."""
        recommendations = self.analyzer.get_project_type_recommendations()
        
        console.print(Panel(
            "\n".join(f"  {rec}" for rec in recommendations[:8]),
            title="📚 Best Practices",
            border_style="blue"
        ))
        
        # Show ideal structure
        console.print()
        if self.analyzer.project_type == 'python':
            from .analyzer import BestPracticeTemplates
            console.print(Panel(
                BestPracticeTemplates.PYTHON_TEMPLATE,
                title="🏗️  Recommended Python Project Structure",
                border_style="green"
            ))
        elif self.analyzer.project_type == 'javascript':
            from .analyzer import BestPracticeTemplates
            console.print(Panel(
                BestPracticeTemplates.JAVASCRIPT_TEMPLATE,
                title="🏗️  Recommended JavaScript Project Structure",
                border_style="green"
            ))
    
    def save_to_file(self, output_file='tree.txt', format='text'):
        """Save tree to file."""
        if format == 'text':
            with open(output_file, 'w', encoding='utf-8') as f:
                console_file = Console(file=f, width=120)
                
                root_info = f"{self.root_path.name}"
                tree = Tree(root_info)
                self._build_tree(tree, self.root_path)
                
                console_file.print(tree)
                console_file.print()
                console_file.print(f"{self.stats['dirs']} directories, {self.stats['files']} files")
            
            console.print(f"✓ Tree saved to {output_file}", style="green")
        
        elif format == 'json':
            import json
            tree_data = self._build_json_tree(self.root_path)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(tree_data, f, indent=2)
            
            console.print(f"✓ Tree saved to {output_file}", style="green")
    
    def _build_json_tree(self, path, depth=0):
        """Build tree as JSON structure."""
        if self.max_depth is not None and depth >= self.max_depth:
            return None
        
        node = {
            'name': path.name,
            'type': 'directory' if path.is_dir() else 'file',
            'path': str(path.relative_to(self.root_path)),
        }
        
        if path.is_file():
            try:
                node['size'] = path.stat().st_size
            except (OSError, PermissionError):
                node['size'] = 0
        
        if path.is_dir():
            children = []
            try:
                items = sorted(path.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))
                for item in items:
                    if self._should_ignore(item):
                        continue
                    child = self._build_json_tree(item, depth + 1)
                    if child:
                        children.append(child)
                
                if children:
                    node['children'] = children
            except PermissionError:
                node['error'] = 'Permission Denied'
        
        return node


def generate_gitignore_tree():
    """Generate tree respecting .gitignore patterns."""
    # This would parse .gitignore and respect those patterns
    # Implementation can be added later
    pass