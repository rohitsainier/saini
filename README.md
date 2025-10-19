# Saini 🚀

[![PyPI version](https://badge.fury.io/py/saini.svg)](https://badge.fury.io/py/saini)
[![Python Support](https://img.shields.io/pypi/pyversions/saini.svg)](https://pypi.org/project/saini/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/saini)](https://pepy.tech/project/saini)

**Developer productivity toolkit by Rohit Saini**

Saini is a comprehensive command-line toolkit designed to boost developer productivity with intelligent time tracking, beautiful project visualization, and automation tools.

## ✨ Features

### ⏱️ Smart Time Tracking
- **Automatic Detection**: Auto-detect project and branch from git
- **Multi-Project Support**: Track time across multiple projects seamlessly
- **Pause/Resume**: Take breaks without losing context
- **Rich Reports**: Daily, weekly, and project-based analytics
- **Data Export**: Export to CSV or JSON for further analysis

### 🍅 Pomodoro Timer
- **Focus Sessions**: 25-minute work intervals with 5-minute breaks
- **Long Breaks**: Automatic 15-minute breaks after 4 pomodoros
- **Desktop Notifications**: Get notified when it's time for a break
- **Session Tracking**: Integrated with time tracking

### 👁️ Idle Detection
- **Smart Pause**: Auto-pause when no git activity detected
- **Configurable Threshold**: Set your own idle timeout (default: 10 minutes)
- **Activity Monitoring**: Tracks git commits and file changes
- **Seamless Resume**: Pick up right where you left off

### 🌳 Project Tree Visualization
- **Beautiful Output**: Rich, colorful tree structure with icons
- **Smart Filtering**: Auto-ignore node_modules, .git, build artifacts
- **File Information**: Optional file sizes and statistics
- **Multiple Formats**: Export to text or JSON
- **Customizable Depth**: Control how deep to traverse
- **Hidden Files**: Optionally show/hide hidden files

## 📦 Installation

### From PyPI (Recommended)

```bash
pip install saini
```

### From Source

```bash
git clone https://github.com/rohitsainier/saini.git
cd saini
./install.sh
```

### Upgrade

```bash
pip install --upgrade saini
```

## 🚀 Quick Start

### Time Tracking

```bash
# Start tracking your work
saini start "Implementing user authentication"

# Check current status
saini status

# Take a break
saini pause

# Resume work
saini resume

# Stop tracking
saini stop

# View today's report
saini report today
```

### Project Tree

```bash
# Show project structure
saini tree

# Limit depth to 3 levels
saini tree -d 3

# Show file sizes
saini tree -s

# Save to file
saini tree -o project-structure.txt

# Export as JSON
saini tree -o structure.json -f json
```

### Configuration

```bash
# Enable Pomodoro mode (25min work, 5min break)
saini config pomodoro on

# Enable idle detection
saini config idle on

# Set idle threshold to 15 minutes
saini config idle-time 15

# View all settings
saini config show
```

## 📚 Complete Command Reference

### Time Tracking Commands

| Command | Description | Example |
|---------|-------------|---------|
| `saini start [description]` | Start tracking time | `saini start "Bug fix #123"` |
| `saini stop` | Stop current session | `saini stop` |
| `saini switch [description]` | Switch to new task | `saini switch "Code review"` |
| `saini pause` | Pause current session | `saini pause` |
| `saini resume` | Resume paused session | `saini resume` |
| `saini status` | Show current status | `saini status` |

### Report Commands

| Command | Description | Example |
|---------|-------------|---------|
| `saini report today` | Today's activity | `saini report today` |
| `saini report yesterday` | Yesterday's activity | `saini report yesterday` |
| `saini report week` | This week's summary | `saini report week` |
| `saini report project [name]` | Project-specific report | `saini report project my-app` |
| `saini export csv [file]` | Export to CSV | `saini export csv report.csv` |
| `saini export json [file]` | Export to JSON | `saini export json report.json` |

### Configuration Commands

| Command | Description | Example |
|---------|-------------|---------|
| `saini config show` | Show all settings | `saini config show` |
| `saini config pomodoro [on\|off]` | Toggle Pomodoro timer | `saini config pomodoro on` |
| `saini config idle [on\|off]` | Toggle idle detection | `saini config idle on` |
| `saini config idle-time [min]` | Set idle threshold | `saini config idle-time 15` |

### Project Tree Commands

| Command | Description | Example |
|---------|-------------|---------|
| `saini tree` | Show project tree | `saini tree` |
| `saini tree -p [path]` | Specify custom path | `saini tree -p /path/to/project` |
| `saini tree -d [depth]` | Limit depth | `saini tree -d 3` |
| `saini tree -a` | Show hidden files | `saini tree -a` |
| `saini tree -s` | Show file sizes | `saini tree -s` |
| `saini tree -o [file]` | Save to file | `saini tree -o tree.txt` |
| `saini tree -f [format]` | Output format (text\|json) | `saini tree -f json` |
| `saini tree -i [pattern]` | Ignore pattern | `saini tree -i "*.log"` |
| `saini tree --no-icons` | Disable icons | `saini tree --no-icons` |

## 💡 Usage Examples

### Example 1: Daily Development Workflow

```bash
# Morning - Start your day
saini config pomodoro on
saini start "Sprint planning and standup"

# Check what you're tracking
saini status
# Output:
# ⚡ Active Session
#   Project:  my-awesome-app
#   Branch:   feature/user-auth
#   Task:     Sprint planning and standup
#   Duration: 15m 30s
#   🍅 Pomodoro: Work Session #1
#   Time Left: 9m 30s

# Switch to coding
saini switch "Implementing JWT authentication"

# Lunch break
saini pause

# Back from lunch
saini resume

# End of day - see what you accomplished
saini stop
saini report today
```

### Example 2: Project Analysis

```bash
# Understand project structure
saini tree -s -d 3

# Output:
# 📁 my-awesome-app
# ├── 📁 src
# │   ├── 📁 components
# │   │   ├── ⚛️ Header.jsx [2.3KB]
# │   │   └── ⚛️ Footer.jsx [1.8KB]
# │   ├── 🐍 main.py [5.2KB]
# │   └── 📋 config.json [892B]
# ├── 📁 tests
# │   └── 🐍 test_main.py [3.1KB]
# ├── 📝 README.md [4.5KB]
# └── 📋 package.json [1.2KB]
#
# 📊 3 directories, 8 files, Total size: 19.0KB

# Save for documentation
saini tree -o STRUCTURE.md

# Export as JSON for analysis
saini tree -o structure.json -f json

# Analyze only source code (ignore build files)
saini tree -i "dist" -i "node_modules" -i "*.min.js"
```

### Example 3: Weekly Review

```bash
# See weekly summary
saini report week

# Output:
# ═══════════════════════════════════════════════════
#          Time Tracking Report
# ═══════════════════════════════════════════════════
# 
# 📅 This Week (starting 2024-01-15)
# 
# By Project:
#   my-awesome-app      12h 30m
#   client-website      8h 45m
#   saini-package       5h 20m
# 
# Total: 26h 35m

# Export for timesheet
saini export csv 
```

### Example 4: Multi-Project Development

```bash
# Working on project A
cd ~/projects/project-a
saini start "Feature development"

# Switch to project B (auto-detects new project)
cd ~/projects/project-b
saini switch "Bug fix"

# Check time per project
saini report project project-a
saini report project project-b
```

### Example 5: Pomodoro Power User

```bash
# Enable Pomodoro with idle detection
saini config pomodoro on
saini config idle on
saini config idle-time 10

# Start focused work
saini start "Deep work - algorithm optimization"

# You'll get notifications:
# After 25 min: "Pomodoro Complete! 🍅 Time for a break! (5 min)"
# After 5 min break: "Break Over! ⏰ Ready to focus?"
# If idle for 10 min: "Auto-Paused ⏸ No git activity for 10m"

# Check status anytime
saini status
# Output:
# ⚡ Active Session
#   Project:  algorithm-lab
#   Branch:   optimization
#   Task:     Deep work - algorithm optimization
#   Duration: 1h 45m 30s
#   🍅 Pomodoro: Work Session #5
#   Time Left: 18m 12s
```

## 🎨 Screenshots

### Time Tracking Status
```
⚡ Active Session
  Project:  saini
  Branch:   main
  Task:     Adding tree visualization feature
  Started:  2024-01-15 10:00:00
  Duration: 45m 30s
  🍅 Pomodoro: Work Session #2
  Time Left: 12m 15s
```

### Project Tree
```
📁 saini
├── 📁 saini
│   ├── 🐍 __init__.py
│   ├── 🐍 cli.py
│   ├── 🐍 tracker.py
│   ├── 🐍 pomodoro.py
│   ├── 🐍 idle_detection.py
│   ├── 🐍 reports.py
│   ├── 🐍 config.py
│   ├── 🐍 tree.py
│   └── 🐍 utils.py
├── 📝 README.md
├── 📋 setup.py
├── 📋 requirements.txt
├── 🔧 install.sh
└── 🔧 publish.sh

📊 2 directories, 13 files
```

### Configuration
```
╔════════════════════════════════════════════╗
║     Time Tracker Configuration             ║
╚════════════════════════════════════════════╝

Setting               Value
─────────────────────────────────────────────
Pomodoro Mode         ✓ Enabled
Pomodoro Work Time    25 minutes
Pomodoro Break Time   5 minutes
Pomodoro Long Break   15 minutes
Idle Detection        ✓ Enabled
Idle Threshold        10 minutes
```


## ⚙️ Configuration

Configuration is stored in `~/.saini/config.json`:

```json
{
  "pomodoro_enabled": true,
  "pomodoro_work_time": 1500,
  "pomodoro_break_time": 300,
  "pomodoro_long_break": 900,
  "idle_detection_enabled": true,
  "idle_threshold": 600
}
```

### Data Storage

All data is stored in `~/.saini/`:
- `sessions.csv` - Time tracking sessions
- `config.json` - User configuration
- `current_session` - Active session data
- `paused_session` - Paused session data
- `pomodoro_state` - Pomodoro timer state
- `idle_check` - Idle detection state

## 🔧 Development

### Local Installation

```bash
# Clone the repository
git clone https://github.com/rohitsainier/saini.git
cd saini

# Install in development mode
./install.sh

# Or use Make
make install
```

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# With coverage
pytest --cov=saini tests/
```

### Building the Package

```bash
# Build
./install.sh -c
python -m build

# Or use Make
make build
```

### Publishing

```bash
# Test publish (TestPyPI)
./publish.sh -t

# Production publish (PyPI)
./publish.sh

# With version bump
./publish.sh -v patch  # 1.0.0 -> 1.0.1
./publish.sh -v minor  # 1.0.0 -> 1.1.0
./publish.sh -v major  # 1.0.0 -> 2.0.0

# Or use Make
make test-publish
make publish
```

## 🛠️ Makefile Commands

```bash
make install        # Install package locally
make reinstall      # Reinstall package
make clean          # Clean build artifacts
make test           # Run tests
make build          # Build package
make test-publish   # Publish to TestPyPI
make publish        # Publish to PyPI
make version-patch  # Bump patch version
make version-minor  # Bump minor version
make version-major  # Bump major version
```

## 📋 Requirements

- Python >= 3.7
- Git (for project/branch detection and idle detection)
- Dependencies:
  - click >= 8.0.0
  - rich >= 10.0.0
  - gitpython >= 3.1.0
  - pandas >= 1.3.0
  - tabulate >= 0.8.9

## 🐛 Troubleshooting

### Issue: Command not found after installation

```bash
# Make sure pip bin directory is in PATH
export PATH="$HOME/.local/bin:$PATH"

# Add to ~/.bashrc or ~/.zshrc for persistence
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

### Issue: Notifications not working

**macOS**: Notifications should work out of the box.

**Linux**: Install `notify-send`:
```bash
sudo apt-get install libnotify-bin  # Ubuntu/Debian
sudo yum install libnotify            # Fedora/CentOS
```

**Windows**: Notifications are shown in terminal.

### Issue: Git detection not working

```bash
# Make sure you're in a git repository
git init

# Or specify path explicitly
saini tree -p /path/to/git/repo
```

### Issue: Permission denied on install

```bash
# Use pip with --user flag
pip install --user saini

# Or use sudo (not recommended)
sudo pip install saini
```

## 🗺️ Roadmap

### Version 1.x
- [x] Time tracking with pause/resume
- [x] Pomodoro timer with notifications
- [x] Idle detection
- [x] Project tree visualization
- [x] Multiple report formats
- [x] CSV/JSON export

### Version 2.x (Planned)
- [ ] `.gitignore` aware tree generation
- [ ] Code complexity analysis
- [ ] Duplicate code detection
- [ ] Dead code finder
- [ ] Unused dependency detection
- [ ] Integration with Jira/GitHub Issues
- [ ] Team collaboration features
- [ ] Cloud sync for time tracking
- [ ] Web dashboard
- [ ] Custom tree themes
- [ ] Tree diff between git commits
- [ ] AI-powered time estimation
- [ ] Automatic time categorization

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Install and test**: `./install.sh -r`
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation
- Run tests before submitting PR

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Rohit Saini**

- GitHub: [@rohitsainier](https://github.com/rohitsainier)
- Email: rohitsainier@example.com
- Twitter: [@rohitsainier](https://twitter.com/rohitsainier)

## 🙏 Acknowledgments

- Inspired by the need for better developer productivity tools
- Built with [Click](https://click.palletsprojects.com/) and [Rich](https://rich.readthedocs.io/)
- Thanks to all contributors and users!

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/rohitsainier/saini?style=social)
![GitHub forks](https://img.shields.io/github/forks/rohitsainier/saini?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/rohitsainier/saini?style=social)

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/rohitsainier/saini/issues)
- **Discussions**: [GitHub Discussions](https://github.com/rohitsainier/saini/discussions)
- **Email**: rohitsainier@example.com

## 🌟 Star History

If you find Saini useful, please consider giving it a star! ⭐

## 📈 Changelog

### Version 1.0.0 (2024-01-15)
- Initial release
- Time tracking with pause/resume
- Pomodoro timer integration
- Idle detection
- Project tree visualization
- Report generation (today, yesterday, week)
- CSV/JSON export
- Configuration management
- Beautiful CLI with Rich
- Installation and publishing scripts

---

**Made with ❤️ by Rohit Saini**

*Boost your productivity, one commit at a time!*
```

## Additional Documentation Files

### `CONTRIBUTING.md`

```markdown
# Contributing to Saini

Thank you for your interest in contributing to Saini! 🎉

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/saini.git`
3. Create a branch: `git checkout -b feature/your-feature`
4. Make your changes
5. Test your changes: `./install.sh -r && pytest`
6. Commit: `git commit -m 'Add some feature'`
7. Push: `git push origin feature/your-feature`
8. Open a Pull Request

## Development Setup

```bash
# Install in development mode
./install.sh

# Install dev dependencies
pip install pytest pytest-cov black flake8 mypy

# Run tests
pytest tests/

# Format code
black saini/

# Lint
flake8 saini/
```

## Code Style

- Follow PEP 8
- Use Black for formatting
- Add docstrings to all functions
- Write tests for new features

## Pull Request Guidelines

- Update README.md if needed
- Add tests for new features
- Ensure all tests pass
- Update CHANGELOG.md

## Questions?

Open an issue or discussion!
```

### `CHANGELOG.md`

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2024-01-15

### Added
- Initial release
- Time tracking functionality
- Pomodoro timer with desktop notifications
- Idle detection based on git activity
- Project tree visualization with icons
- Multiple report formats (today, yesterday, week, project)
- CSV and JSON export
- Configuration management
- Beautiful CLI with Rich library
- Installation script (install.sh)
- Publishing script (publish.sh)
- Makefile for common tasks

### Features
- Auto-detect project and branch from git
- Pause/resume time tracking
- 25-minute Pomodoro sessions with 5-minute breaks
- Customizable idle detection threshold
- File size information in tree view
- Export tree to text or JSON
- Comprehensive documentation

## [Unreleased]

### Planned
- .gitignore aware tree
- Code complexity analysis
- Duplicate code detection
- Integration with GitHub/Jira
- Team collaboration features
```

Now you have a complete, professional README! 🚀

Want me to create any other documentation files like:
- API documentation
- Architecture diagram
- Tutorial/Guide
- FAQ section?