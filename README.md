# Saini 🚀

[![PyPI version](https://badge.fury.io/py/saini.svg)](https://badge.fury.io/py/saini)
[![Python Support](https://img.shields.io/pypi/pyversions/saini.svg)](https://pypi.org/project/saini/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/saini)](https://pepy.tech/project/saini)

**Developer productivity toolkit by Rohit Saini**

Saini is a comprehensive command-line toolkit designed to boost developer productivity with intelligent time tracking, beautiful project visualization, ML model conversion, and automation tools.

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

### 🌳 Project Tree Visualization & Analysis
- **Beautiful Output**: Rich, colorful tree structure with icons
- **Smart Filtering**: Auto-ignore node_modules, .git, build artifacts
- **File Information**: Optional file sizes and statistics
- **Multiple Formats**: Export to text or JSON
- **Customizable Depth**: Control how deep to traverse
- **Structure Analysis**: AI-powered best practices suggestions
- **Health Score**: Get a project structure health rating
- **SOLID Principles**: Check adherence to design principles

### 🤖 ML Model Conversion
- **PyTorch → ONNX**: Convert PyTorch models with optimization
- **TensorFlow → ONNX**: Support for Keras and SavedModel formats
- **ONNX → CoreML**: Deploy models to iOS/macOS
- **Auto-Conversion**: Direct conversion between any supported formats
- **Batch Processing**: Convert multiple models at once
- **Model Verification**: Automatic validation and info display
- **Optimization**: Built-in ONNX model optimization

## 📦 Installation

### Basic Installation (Time Tracking + Tree)

```bash
pip install saini
```

### Full Installation (Including ML Conversion)

```bash
# Install with ML support
pip install "saini[ml]"

# Or install ML dependencies separately
pip install saini
pip install torch onnx tensorflow tf2onnx coremltools
```

### From Source

```bash
git clone https://github.com/rohitsainier/saini.git
cd saini
./install.sh

# For ML support
pip install torch onnx tensorflow tf2onnx coremltools
```

### Upgrade

```bash
pip install --upgrade saini
# or
pip install --upgrade "saini[ml]"
```

## 🚀 Quick Start

### Time Tracking

```bash
# Start tracking your work
saini start "Implementing user authentication"

# Check current status with live timer
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

### Project Tree & Analysis

```bash
# Show project structure
saini tree

# Analyze structure with best practices suggestions
saini tree --analyze

# Limit depth to 3 levels with analysis
saini tree -d 3 --analyze

# Show file sizes
saini tree -s

# Save to file
saini tree -o project-structure.txt
```

### Model Conversion

```bash
# PyTorch to ONNX
saini convert pytorch-onnx model.pth model.onnx -s 1,3,224,224

# TensorFlow to ONNX
saini convert tf-onnx model.h5 model.onnx

# ONNX to CoreML
saini convert onnx-coreml model.onnx model.mlmodel --target iOS15

# Direct PyTorch to CoreML (via ONNX)
saini convert auto model.pt model.mlmodel \
    --from pytorch --to coreml -s 1,3,224,224

# Batch convert multiple models
saini convert batch models/ output/ --from pytorch --to onnx -s 1,3,224,224
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
| `saini status` | Show live status | `saini status` |
| `saini status --static` | Show static snapshot | `saini status --static` |
| `saini dashboard` | Show live dashboard | `saini dashboard` |

### Report Commands

| Command | Description | Example |
|---------|-------------|---------|
| `saini report today` | Today's activity | `saini report today` |
| `saini report yesterday` | Yesterday's activity | `saini report yesterday` |
| `saini report week` | This week's summary | `saini report week` |
| `saini report project [name]` | Project-specific report | `saini report project my-app` |
| `saini export csv [file]` | Export to CSV | `saini export csv report.csv` |
| `saini export json [file]` | Export to JSON | `saini export json report.json` |

### Project Tree Commands

| Command | Description | Example |
|---------|-------------|---------|
| `saini tree` | Show project tree | `saini tree` |
| `saini tree --analyze` | Show tree with analysis | `saini tree --analyze` |
| `saini tree -p [path]` | Specify custom path | `saini tree -p /path/to/project` |
| `saini tree -d [depth]` | Limit depth | `saini tree -d 3` |
| `saini tree -a` | Show hidden files | `saini tree -a` |
| `saini tree -s` | Show file sizes | `saini tree -s` |
| `saini tree -o [file]` | Save to file | `saini tree -o tree.txt` |
| `saini tree -f [format]` | Output format (text\|json) | `saini tree -f json` |
| `saini tree -i [pattern]` | Ignore pattern | `saini tree -i "*.log"` |
| `saini tree --no-icons` | Disable icons | `saini tree --no-icons` |

### Model Conversion Commands

| Command | Description | Example |
|---------|-------------|---------|
| `saini convert pytorch-onnx` | PyTorch to ONNX | `saini convert pytorch-onnx model.pth out.onnx -s 1,3,224,224` |
| `saini convert tf-onnx` | TensorFlow to ONNX | `saini convert tf-onnx model.h5 out.onnx` |
| `saini convert onnx-coreml` | ONNX to CoreML | `saini convert onnx-coreml model.onnx out.mlmodel` |
| `saini convert auto` | Auto-convert any format | `saini convert auto model.pt out.mlmodel --from pytorch --to coreml -s 1,3,224,224` |
| `saini convert batch` | Batch convert models | `saini convert batch models/ out/ --from pytorch --to onnx -s 1,3,224,224` |

### Configuration Commands

| Command | Description | Example |
|---------|-------------|---------|
| `saini config show` | Show all settings | `saini config show` |
| `saini config pomodoro [on\|off]` | Toggle Pomodoro timer | `saini config pomodoro on` |
| `saini config idle [on\|off]` | Toggle idle detection | `saini config idle on` |
| `saini config idle-time [min]` | Set idle threshold | `saini config idle-time 15` |

## 💡 Usage Examples

### Example 1: Daily Development Workflow

```bash
# Morning - Start your day
saini config pomodoro on
saini start "Sprint planning and standup"

# Check what you're tracking (live updating)
saini status
# Output:
# 🔴 Active Session - LIVE
#   Project:  my-awesome-app
#   Branch:   feature/user-auth
#   Task:     Sprint planning and standup
#   ⏱️  00:15:30
#   🍅 Pomodoro Session #1
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

### Example 2: Project Structure Analysis

```bash
# Analyze project structure with best practices
saini tree --analyze

# Output:
# 📁 my-awesome-app
# ├── 📁 src
# │   ├── 🐍 __init__.py
# │   ├── 🐍 main.py
# │   └── 📁 utils
# ├── 📁 tests
# ├── 📝 README.md
# └── 📋 setup.py
#
# ═══════════════════════════════════════════════════
# 
# 📋 Analysis
# Project Type: PYTHON
#
# 🏆 Structure Health Score
# 85/100 - Good ⭐⭐
#
# ⚠️  Warnings (Should Fix):
#   • Missing requirements.txt
#     Consider adding requirements.txt: Python dependencies list
#
# 💡 Suggestions (Consider):
#   • No docs directory
#     Consider creating a 'docs/' directory for detailed documentation
#
# 📚 Best Practices
#   📦 Use a 'src/' directory for your package code
#   🧪 Keep tests in a separate 'tests/' directory
#   📝 Document modules with docstrings
#   ...
```

### Example 3: ML Model Conversion Pipeline

```bash
# Convert PyTorch model to ONNX
saini convert pytorch-onnx resnet50.pth resnet50.onnx -s 1,3,224,224

# Output:
# 🔄 Converting PyTorch → ONNX
#   Model: resnet50.pth
#   Output: resnet50.onnx
# Loading PyTorch model... ████████████████████ 100%
# ✓ Successfully converted to ONNX
#
# ┌─── ONNX Model Info ───┐
# │ IR Version    │ 8     │
# │ Opset Version │ 11    │
# │ Inputs        │ input: [1, 3, 224, 224] │
# │ Outputs       │ output: [1, 1000] │
# │ File Size     │ 97.8 MB │
# └───────────────────────┘

# Convert ONNX to CoreML for iOS deployment
saini convert onnx-coreml resnet50.onnx resnet50.mlmodel \
    --target iOS15 --precision FLOAT16 --name ResNet50

# Direct conversion PyTorch → CoreML
saini convert auto mobilenet.pt mobilenet.mlmodel \
    --from pytorch --to coreml \
    -s 1,3,224,224 \
    --target iOS16 \
    --precision FLOAT16

# Batch convert all PyTorch models in a directory
saini convert batch pytorch_models/ onnx_models/ \
    --from pytorch --to onnx -s 1,3,224,224
```

### Example 4: TensorFlow/Keras to CoreML

```bash
# Convert Keras model to ONNX
saini convert tf-onnx my_model.h5 my_model.onnx

# Then to CoreML
saini convert onnx-coreml my_model.onnx my_model.mlmodel \
    --target iOS15 --name MyAwesomeModel

# Or do it in one step
saini convert auto my_model.h5 my_model.mlmodel \
    --from tensorflow --to coreml \
    --target iOS15 --precision FLOAT16
```

### Example 5: Weekly Review

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
#   ml-pipeline         8h 45m
#   saini-package       5h 20m
# 
# Total: 26h 35m

# Export for timesheet
saini export csv weekly_report.csv
```

### Example 6: Pomodoro Power User

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
```

## 🎨 Screenshots

### Time Tracking Status
```
🔴 Time Tracker - LIVE
  Project:  saini
  Branch:   main
  Task:     Adding ML model conversion
  Started:  2024-01-15 10:00:00
  
  ⏱️  01:45:30
  
  🍅 Pomodoro Session #5
  [████████████░░░░░░░░] 60%
  Time Left: 10m 00s
  
Press Ctrl+C to exit live view
```

### Project Tree with Analysis
```
📁 saini
├── 📁 saini
│   ├── 🐍 __init__.py
│   ├── 🐍 cli.py
│   ├── 🐍 tracker.py
│   ├── 🐍 converter.py
│   ├── 🐍 analyzer.py
│   └── 🐍 tree.py
├── 📝 README.md
├── 📋 setup.py
└── 📋 requirements.txt

📊 2 directories, 13 files

🏆 Structure Health Score: 92/100 - Excellent ⭐⭐⭐
```

### Model Conversion Progress
```
🔄 Converting PyTorch → ONNX
  Model: resnet50.pth
  Output: resnet50.onnx

Converting to ONNX... ████████████████████ 100%

✓ Successfully converted to ONNX

┌────────── ONNX Model Info ──────────┐
│ Property       │ Value               │
├────────────────┼─────────────────────┤
│ IR Version     │ 8                   │
│ Opset Version  │ 11                  │
│ Inputs         │ input: [1,3,224,224]│
│ Outputs        │ output: [1, 1000]   │
│ File Size      │ 97.8 MB             │
└────────────────┴─────────────────────┘
```

## 🤖 Model Conversion Details

### Supported Conversions

| From | To | Via | Status |
|------|-----|-----|--------|
| PyTorch | ONNX | Direct | ✅ |
| TensorFlow | ONNX | Direct | ✅ |
| Keras | ONNX | Direct | ✅ |
| ONNX | CoreML | Direct | ✅ |
| PyTorch | CoreML | ONNX | ✅ |
| TensorFlow | CoreML | ONNX | ✅ |

### PyTorch Conversion Options

```bash
saini convert pytorch-onnx MODEL OUTPUT -s SHAPE [OPTIONS]

Options:
  -s, --input-shape TEXT      Input tensor shape (required) e.g., 1,3,224,224
  --input-names TEXT          Comma-separated input names
  --output-names TEXT         Comma-separated output names
  --opset INTEGER            ONNX opset version (default: 11)
  --no-optimize              Skip ONNX optimization
```

### TensorFlow Conversion Options

```bash
saini convert tf-onnx MODEL OUTPUT [OPTIONS]

Options:
  --opset INTEGER            ONNX opset version (default: 11)
  --no-optimize              Skip ONNX optimization
```

### CoreML Conversion Options

```bash
saini convert onnx-coreml MODEL OUTPUT [OPTIONS]

Options:
  --name TEXT                Model name (default: ConvertedModel)
  --target TEXT              Deployment target: iOS13, iOS14, iOS15, iOS16,
                            macOS10_15, macOS11, macOS12 (default: iOS13)
  --precision TEXT           Compute precision: FLOAT32, FLOAT16 (default: FLOAT32)
```

### Auto Conversion

```bash
saini convert auto MODEL OUTPUT --from FRAMEWORK --to FORMAT [OPTIONS]

Frameworks: pytorch, tensorflow, keras, onnx
Formats: onnx, coreml

All options from specific converters are supported
```

### Batch Conversion

```bash
saini convert batch MODELS_DIR OUTPUT_DIR --from FRAMEWORK --to FORMAT [OPTIONS]

Example:
  saini convert batch models/ output/ --from pytorch --to onnx -s 1,3,224,224
  saini convert batch onnx_models/ coreml/ --from onnx --to coreml --target iOS15
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

# Install with ML support
pip install torch onnx tensorflow tf2onnx coremltools

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
./publish.sh -v patch  # 1.0.5 -> 1.0.6
./publish.sh -v minor  # 1.0.5 -> 1.1.0
./publish.sh -v major  # 1.0.5 -> 2.0.0

# Or use Make
make test-publish
make publish
```

## 🛠️ Makefile Commands

```bash
make help           # Show all available commands
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

### Core Requirements
- Python >= 3.7
- Git (for project/branch detection and idle detection)

### Core Dependencies
- click >= 8.0.0
- rich >= 10.0.0
- gitpython >= 3.1.0
- pandas >= 1.3.0
- tabulate >= 0.8.9

### Optional ML Dependencies (for model conversion)
- torch >= 1.9.0
- onnx >= 1.10.0
- onnxoptimizer >= 0.2.6
- tensorflow >= 2.6.0
- tf2onnx >= 1.9.0
- coremltools >= 5.0.0

Install with: `pip install "saini[ml]"`

## 🐛 Troubleshooting

### Issue: Command not found after installation

```bash
# Make sure pip bin directory is in PATH
export PATH="$HOME/.local/bin:$PATH"

# Add to ~/.bashrc or ~/.zshrc for persistence
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

### Issue: ML conversion dependencies

```bash
# Install ML dependencies separately if needed
pip install torch onnx tensorflow tf2onnx coremltools

# Or install specific framework
pip install torch onnx  # For PyTorch conversion
pip install tensorflow tf2onnx  # For TensorFlow conversion
pip install coremltools  # For CoreML conversion
```

### Issue: ONNX conversion fails

```bash
# Try different opset version
saini convert pytorch-onnx model.pth output.onnx -s 1,3,224,224 --opset 13

# Check PyTorch model format
# Model should be the actual model, not just state_dict
```

### Issue: CoreML conversion fails

```bash
# Make sure ONNX model is valid first
# Try with FLOAT32 instead of FLOAT16
saini convert onnx-coreml model.onnx output.mlmodel --precision FLOAT32
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

## 🗺️ Roadmap

### Version 1.0 ✅
- [x] Time tracking with pause/resume
- [x] Pomodoro timer with notifications
- [x] Idle detection
- [x] Project tree visualization
- [x] Project structure analysis
- [x] Multiple report formats
- [x] CSV/JSON export
- [x] ML model conversion (PyTorch, TensorFlow, ONNX, CoreML)

### Version 1.1 (In Progress)
- [ ] `.gitignore` aware tree generation
- [ ] Model quantization support
- [ ] Model performance benchmarking
- [ ] ONNX Runtime integration

### Version 2.0 (Planned)
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
- [ ] TensorRT conversion support
- [ ] OpenVINO support
- [ ] Model compression tools

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
- Use type hints where appropriate
- Add docstrings to all functions

### Areas for Contribution

- 🐛 Bug fixes
- ✨ New features
- 📝 Documentation improvements
- 🧪 Test coverage
- 🎨 UI/UX improvements
- 🌍 Internationalization
- ⚡ Performance optimizations

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Rohit Saini**

- GitHub: [@rohitsainier](https://github.com/rohitsainier)
- Email: rohitsainier@gmail.com
- Twitter: [@rohitsainier](https://twitter.com/rohitsainier)

## 🙏 Acknowledgments

- Inspired by the need for better developer productivity tools
- Built with [Click](https://click.palletsprojects.com/) and [Rich](https://rich.readthedocs.io/)
- ML conversion powered by [ONNX](https://onnx.ai/), [PyTorch](https://pytorch.org/), [TensorFlow](https://www.tensorflow.org/), and [CoreML Tools](https://coremltools.readme.io/)
- Thanks to all contributors and users!

## 📊 Stats

![GitHub stars](https://img.shields.io/github/stars/rohitsainier/saini?style=social)
![GitHub forks](https://img.shields.io/github/forks/rohitsainier/saini?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/rohitsainier/saini?style=social)
![GitHub issues](https://img.shields.io/github/issues/rohitsainier/saini)
![GitHub pull requests](https://img.shields.io/github/issues-pr/rohitsainier/saini)

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/rohitsainier/saini/issues)
- **Discussions**: [GitHub Discussions](https://github.com/rohitsainier/saini/discussions)
- **Documentation**: [Wiki](https://github.com/rohitsainier/saini/wiki)
- **Email**: rohitsainier@gmail.com

## 🌟 Star History

If you find Saini useful, please consider giving it a star! ⭐

[![Star History Chart](https://api.star-history.com/svg?repos=rohitsainier/saini&type=Date)](https://star-history.com/#rohitsainier/saini&Date)

## 📈 Changelog

### Version 1.0.5 (Current)
- ✨ Added ML model conversion support
  - PyTorch to ONNX conversion
  - TensorFlow/Keras to ONNX conversion
  - ONNX to CoreML conversion
  - Auto-conversion between formats
  - Batch conversion support
- 🎨 Added project structure analysis
- 🏆 Health score for project structure
- 💡 Best practices suggestions
- 🐛 Various bug fixes and improvements

### Version 1.0.0 (2024-01-15)
- 🎉 Initial release
- ⏱️ Time tracking functionality
- 🍅 Pomodoro timer with desktop notifications
- 👁️ Idle detection based on git activity
- 🌳 Project tree visualization with icons
- 📊 Multiple report formats
- 💾 CSV and JSON export
- ⚙️ Configuration management
- 🎨 Beautiful CLI with Rich library

---

**Made with ❤️ by Rohit Saini**

*Boost your productivity, one commit at a time!*

---

## Quick Links

- [Installation Guide](#-installation)
- [Quick Start](#-quick-start)
- [Command Reference](#-complete-command-reference)
- [Model Conversion Guide](#-model-conversion-details)
- [Configuration](#%EF%B8%8F-configuration)
- [Contributing](#-contributing)
- [License](#-license)