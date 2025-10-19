"""Project structure analyzer with best practices suggestions."""

from pathlib import Path
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    """Suggestion severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUGGESTION = "suggestion"


@dataclass
class Suggestion:
    """A structure improvement suggestion."""
    severity: Severity
    category: str
    message: str
    details: str
    file_path: str = ""


class ProjectAnalyzer:
    """Analyze project structure and provide suggestions."""
    
    # Best practice patterns for different project types
    PYTHON_BEST_PRACTICES = {
        'required_files': {
            'README.md': 'Documentation file explaining the project',
            'requirements.txt': 'Python dependencies list',
            '.gitignore': 'Git ignore patterns',
            'setup.py': 'Package setup file (for distributable packages)',
        },
        'recommended_structure': {
            'tests/': 'Unit tests directory',
            'docs/': 'Documentation directory',
            'src/': 'Source code directory (alternative to package root)',
        },
        'anti_patterns': {
            'too_many_root_files': 'More than 10 Python files in root',
            'mixed_case_folders': 'Folders with mixed case (use lowercase)',
            'no_init_py': 'Package directory missing __init__.py',
            'deep_nesting': 'Directory nesting deeper than 5 levels',
        }
    }
    
    JAVASCRIPT_BEST_PRACTICES = {
        'required_files': {
            'package.json': 'NPM package configuration',
            'README.md': 'Project documentation',
            '.gitignore': 'Git ignore patterns',
        },
        'recommended_structure': {
            'src/': 'Source code directory',
            'tests/' or 'test/': 'Test files',
            'public/': 'Public assets',
            'dist/': 'Build output (should be in .gitignore)',
        },
    }
    
    JAVA_BEST_PRACTICES = {
        'required_files': {
            'pom.xml' or 'build.gradle': 'Build configuration',
            'README.md': 'Project documentation',
        },
        'recommended_structure': {
            'src/main/java/': 'Main Java source code',
            'src/test/java/': 'Test source code',
            'src/main/resources/': 'Application resources',
        },
    }
    
    def __init__(self, root_path: Path):
        """Initialize analyzer."""
        self.root_path = Path(root_path)
        self.suggestions: List[Suggestion] = []
        self.project_type = self._detect_project_type()
        self.structure = self._analyze_structure()
    
    def _detect_project_type(self) -> str:
        """Detect project type based on files."""
        files = set(f.name for f in self.root_path.iterdir() if f.is_file())
        
        # Python
        if 'setup.py' in files or 'pyproject.toml' in files or 'requirements.txt' in files:
            return 'python'
        
        # JavaScript/Node
        if 'package.json' in files:
            return 'javascript'
        
        # Java
        if 'pom.xml' in files or 'build.gradle' in files:
            return 'java'
        
        # Go
        if 'go.mod' in files:
            return 'go'
        
        # Rust
        if 'Cargo.toml' in files:
            return 'rust'
        
        # Ruby
        if 'Gemfile' in files:
            return 'ruby'
        
        # Generic
        return 'generic'
    
    def _analyze_structure(self) -> Dict:
        """Analyze the project structure."""
        structure = {
            'total_files': 0,
            'total_dirs': 0,
            'max_depth': 0,
            'files_by_type': {},
            'root_files': [],
            'root_dirs': [],
            'missing_files': [],
            'unnecessary_files': [],
        }
        
        # Count files and directories
        for path in self.root_path.rglob('*'):
            try:
                if path.is_file():
                    structure['total_files'] += 1
                    ext = path.suffix
                    structure['files_by_type'][ext] = structure['files_by_type'].get(ext, 0) + 1
                    
                    # Root level files
                    if path.parent == self.root_path:
                        structure['root_files'].append(path.name)
                elif path.is_dir():
                    structure['total_dirs'] += 1
                    
                    # Root level directories
                    if path.parent == self.root_path:
                        structure['root_dirs'].append(path.name)
                
                # Calculate depth
                depth = len(path.relative_to(self.root_path).parts)
                structure['max_depth'] = max(structure['max_depth'], depth)
            
            except (PermissionError, OSError):
                pass
        
        return structure
    
    def analyze(self) -> List[Suggestion]:
        """Run all analysis checks."""
        self.suggestions = []
        
        # Run project-specific checks
        if self.project_type == 'python':
            self._check_python_structure()
        elif self.project_type == 'javascript':
            self._check_javascript_structure()
        elif self.project_type == 'java':
            self._check_java_structure()
        
        # Run general checks
        self._check_general_best_practices()
        self._check_solid_principles()
        self._check_naming_conventions()
        self._check_organization()
        
        return self.suggestions
    
    def _check_python_structure(self):
        """Check Python project structure."""
        # Check for required files
        for file, description in self.PYTHON_BEST_PRACTICES['required_files'].items():
            if not (self.root_path / file).exists():
                self.suggestions.append(Suggestion(
                    severity=Severity.WARNING,
                    category="Missing File",
                    message=f"Missing {file}",
                    details=f"Consider adding {file}: {description}"
                ))
        
        # Check for __init__.py in packages
        for path in self.root_path.rglob('*.py'):
            parent = path.parent
            if parent != self.root_path and parent.is_dir():
                if not (parent / '__init__.py').exists():
                    # Check if it's a package (has multiple .py files)
                    py_files = list(parent.glob('*.py'))
                    if len(py_files) > 1:
                        self.suggestions.append(Suggestion(
                            severity=Severity.WARNING,
                            category="Package Structure",
                            message=f"Missing __init__.py in {parent.name}/",
                            details="Python packages should have __init__.py to be importable",
                            file_path=str(parent.relative_to(self.root_path))
                        ))
        
        # Check for tests directory
        if not (self.root_path / 'tests').exists() and not (self.root_path / 'test').exists():
            self.suggestions.append(Suggestion(
                severity=Severity.SUGGESTION,
                category="Project Organization",
                message="No tests directory found",
                details="Create a 'tests/' directory for unit tests following best practices"
            ))
        
        # Check for too many root-level Python files
        root_py_files = list(self.root_path.glob('*.py'))
        if len(root_py_files) > 5:
            self.suggestions.append(Suggestion(
                severity=Severity.WARNING,
                category="Organization",
                message=f"{len(root_py_files)} Python files in root directory",
                details="Consider organizing code into packages/modules for better structure"
            ))
    
    def _check_javascript_structure(self):
        """Check JavaScript/Node.js project structure."""
        # Check for package.json
        if not (self.root_path / 'package.json').exists():
            self.suggestions.append(Suggestion(
                severity=Severity.ERROR,
                category="Missing File",
                message="Missing package.json",
                details="Run 'npm init' to create package.json"
            ))
        
        # Check for src directory
        if not (self.root_path / 'src').exists():
            self.suggestions.append(Suggestion(
                severity=Severity.SUGGESTION,
                category="Project Organization",
                message="No src/ directory found",
                details="Consider organizing source code in a 'src/' directory"
            ))
    
    def _check_java_structure(self):
        """Check Java project structure."""
        # Check Maven/Gradle structure
        has_maven = (self.root_path / 'src/main/java').exists()
        has_gradle = (self.root_path / 'build.gradle').exists()
        
        if not has_maven and not has_gradle:
            self.suggestions.append(Suggestion(
                severity=Severity.WARNING,
                category="Project Structure",
                message="Non-standard Java project structure",
                details="Consider using Maven (src/main/java) or Gradle structure"
            ))
    
    def _check_general_best_practices(self):
        """Check general best practices."""
        # README
        readme_files = ['README.md', 'README.rst', 'README.txt', 'README']
        has_readme = any((self.root_path / f).exists() for f in readme_files)
        
        if not has_readme:
            self.suggestions.append(Suggestion(
                severity=Severity.ERROR,
                category="Documentation",
                message="Missing README file",
                details="Add README.md to document your project purpose, installation, and usage"
            ))
        
        # LICENSE
        if not (self.root_path / 'LICENSE').exists() and not (self.root_path / 'LICENSE.txt').exists():
            self.suggestions.append(Suggestion(
                severity=Severity.INFO,
                category="Legal",
                message="No LICENSE file found",
                details="Consider adding a LICENSE file to clarify usage rights"
            ))
        
        # .gitignore
        if not (self.root_path / '.gitignore').exists():
            self.suggestions.append(Suggestion(
                severity=Severity.WARNING,
                category="Version Control",
                message="Missing .gitignore",
                details="Add .gitignore to exclude build artifacts and sensitive files"
            ))
    
    def _check_solid_principles(self):
        """Check adherence to SOLID principles in structure."""
        # Single Responsibility: Check for god objects
        for path in self.root_path.rglob('*'):
            if path.is_file() and path.suffix in ['.py', '.js', '.java']:
                try:
                    size = path.stat().st_size
                    # Files larger than 500 lines (~10KB for average code)
                    if size > 10000:
                        self.suggestions.append(Suggestion(
                            severity=Severity.WARNING,
                            category="SOLID: Single Responsibility",
                            message=f"Large file: {path.name}",
                            details=f"File is {size} bytes. Consider breaking into smaller, focused modules",
                            file_path=str(path.relative_to(self.root_path))
                        ))
                except (OSError, PermissionError):
                    pass
        
        # Dependency Inversion: Check for config separation
        has_config = any((self.root_path / f).exists() for f in ['config/', 'settings/', 'config.py', 'settings.py'])
        if not has_config and self.structure['total_files'] > 10:
            self.suggestions.append(Suggestion(
                severity=Severity.SUGGESTION,
                category="SOLID: Dependency Inversion",
                message="No separate configuration found",
                details="Consider separating configuration from code (config.py, settings/, .env)"
            ))
    
    def _check_naming_conventions(self):
        """Check naming conventions."""
        for path in self.root_path.iterdir():
            if path.is_dir():
                name = path.name
                
                # Check for spaces in folder names
                if ' ' in name:
                    self.suggestions.append(Suggestion(
                        severity=Severity.ERROR,
                        category="Naming Convention",
                        message=f"Folder name contains spaces: '{name}'",
                        details="Use underscores or hyphens instead of spaces",
                        file_path=name
                    ))
                
                # Check for mixed case (not lowercase or not PascalCase)
                if self.project_type == 'python' and name.lower() != name and not name[0].isupper():
                    self.suggestions.append(Suggestion(
                        severity=Severity.WARNING,
                        category="Naming Convention",
                        message=f"Python package should be lowercase: '{name}'",
                        details="Python packages typically use lowercase with underscores",
                        file_path=name
                    ))
    
    def _check_organization(self):
        """Check overall organization."""
        # Check depth
        if self.structure['max_depth'] > 6:
            self.suggestions.append(Suggestion(
                severity=Severity.WARNING,
                category="Organization",
                message=f"Deep directory nesting ({self.structure['max_depth']} levels)",
                details="Consider flattening structure for better maintainability"
            ))
        
        # Check for separation of concerns
        has_tests_separate = (self.root_path / 'tests').exists() or (self.root_path / 'test').exists()
        has_docs_separate = (self.root_path / 'docs').exists() or (self.root_path / 'documentation').exists()
        
        if not has_tests_separate and self.structure['total_files'] > 5:
            self.suggestions.append(Suggestion(
                severity=Severity.SUGGESTION,
                category="Separation of Concerns",
                message="Tests not in separate directory",
                details="Create a 'tests/' directory to separate test code from source code"
            ))
        
        if not has_docs_separate and self.structure['total_files'] > 20:
            self.suggestions.append(Suggestion(
                severity=Severity.INFO,
                category="Documentation",
                message="No docs directory",
                details="Consider creating a 'docs/' directory for detailed documentation"
            ))
    
    def get_health_score(self) -> Tuple[int, str]:
        """Calculate project structure health score."""
        total_points = 100
        
        # Deduct points for errors and warnings
        for suggestion in self.suggestions:
            if suggestion.severity == Severity.ERROR:
                total_points -= 15
            elif suggestion.severity == Severity.WARNING:
                total_points -= 5
            elif suggestion.severity == Severity.SUGGESTION:
                total_points -= 2
        
        score = max(0, total_points)
        
        # Determine grade
        if score >= 90:
            grade = "Excellent ⭐⭐⭐"
        elif score >= 75:
            grade = "Good ⭐⭐"
        elif score >= 60:
            grade = "Fair ⭐"
        else:
            grade = "Needs Improvement"
        
        return score, grade
    
    def get_project_type_recommendations(self) -> List[str]:
        """Get project-type specific recommendations."""
        recommendations = []
        
        if self.project_type == 'python':
            recommendations.extend([
                "📦 Use a 'src/' directory for your package code",
                "🧪 Keep tests in a separate 'tests/' directory",
                "📝 Document modules with docstrings",
                "🔧 Use setup.py or pyproject.toml for packaging",
                "🎯 Follow PEP 8 naming conventions",
            ])
        elif self.project_type == 'javascript':
            recommendations.extend([
                "📦 Organize code in 'src/' directory",
                "🧪 Place tests in '__tests__' or 'test/' directory",
                "⚙️ Use 'config/' for configuration files",
                "🎨 Separate components, utils, and services",
                "📝 Document with JSDoc comments",
            ])
        elif self.project_type == 'java':
            recommendations.extend([
                "📦 Follow Maven structure: src/main/java",
                "🧪 Tests in src/test/java",
                "📄 Resources in src/main/resources",
                "🎯 Package by feature, not by layer",
                "🏗️ Use design patterns appropriately",
            ])
        
        # General recommendations
        recommendations.extend([
            "📖 Maintain clear README with setup instructions",
            "🔐 Use .gitignore to exclude sensitive files",
            "📋 Keep configuration separate from code",
            "🎯 One responsibility per module/class",
            "♻️ Apply DRY principle (Don't Repeat Yourself)",
        ])
        
        return recommendations


class BestPracticeTemplates:
    """Templates for recommended project structures."""
    
    PYTHON_TEMPLATE = """
Recommended Python Project Structure:
    
project_name/
├── README.md
├── LICENSE
├── setup.py or pyproject.toml
├── requirements.txt
├── .gitignore
├── .env.example
│
├── src/
│   └── project_name/
│       ├── __init__.py
│       ├── main.py
│       ├── core/
│       │   ├── __init__.py
│       │   └── ...
│       └── utils/
│           ├── __init__.py
│           └── ...
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_*.py
│
├── docs/
│   ├── conf.py
│   └── index.rst
│
└── scripts/
    └── ...
"""
    
    JAVASCRIPT_TEMPLATE = """
Recommended JavaScript/Node.js Project Structure:

project_name/
├── README.md
├── package.json
├── .gitignore
├── .env.example
│
├── src/
│   ├── index.js
│   ├── components/
│   ├── utils/
│   ├── services/
│   └── config/
│
├── tests/
│   └── ...
│
├── public/
│   └── ...
│
└── docs/
    └── ...
"""