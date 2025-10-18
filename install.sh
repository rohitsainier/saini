#!/bin/bash

# Saini - Local Installation Script
# Use this to test your package locally before publishing

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Saini - Local Installation Script       ║${NC}"
echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
echo ""

# Function to print status messages
print_status() {
    echo -e "${CYAN}▶${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    print_error "setup.py not found. Please run this script from the package root directory."
    exit 1
fi

# Parse command line arguments
REINSTALL=false
CLEAN=false
DEV_MODE=true
SKIP_DEPS=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--reinstall)
            REINSTALL=true
            shift
            ;;
        -c|--clean)
            CLEAN=true
            shift
            ;;
        -p|--production)
            DEV_MODE=false
            shift
            ;;
        --skip-deps)
            SKIP_DEPS=true
            shift
            ;;
        -h|--help)
            echo "Usage: ./install.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -r, --reinstall    Uninstall existing version first"
            echo "  -c, --clean        Clean build artifacts before installing"
            echo "  -p, --production   Install in production mode (not editable)"
            echo "  --skip-deps        Skip installing dependencies"
            echo "  -h, --help         Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./install.sh                    # Install in development mode"
            echo "  ./install.sh -r                 # Reinstall"
            echo "  ./install.sh -c                 # Clean install"
            echo "  ./install.sh -p                 # Production install"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

echo -e "${YELLOW}Configuration:${NC}"
echo "  Development mode: $DEV_MODE"
echo "  Clean build: $CLEAN"
echo "  Reinstall: $REINSTALL"
echo ""

# Step 1: Uninstall if requested
if [ "$REINSTALL" = true ]; then
    print_status "Uninstalling existing version..."
    pip uninstall -y saini 2>/dev/null || true
    print_success "Uninstalled"
    echo ""
fi

# Step 2: Clean build artifacts if requested
if [ "$CLEAN" = true ]; then
    print_status "Cleaning build artifacts..."
    
    rm -rf build/
    rm -rf dist/
    rm -rf *.egg-info
    rm -rf saini.egg-info
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    
    print_success "Cleaned"
    echo ""
fi

# Step 3: Check Python version
print_status "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.7"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    print_error "Python $REQUIRED_VERSION or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

print_success "Python $PYTHON_VERSION"
echo ""

# Step 4: Create/activate virtual environment (optional)
read -p "$(echo -e ${YELLOW}Create/use virtual environment? [y/N]:${NC} )" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
    
    print_status "Activating virtual environment..."
    source venv/bin/activate
    print_success "Activated (venv)"
    echo ""
fi

# Step 5: Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip >/dev/null 2>&1
print_success "pip upgraded"
echo ""

# Step 6: Install build tools
print_status "Installing build tools..."
pip install --upgrade setuptools wheel build >/dev/null 2>&1
print_success "Build tools installed"
echo ""

# Step 7: Install dependencies
if [ "$SKIP_DEPS" = false ]; then
    print_status "Installing dependencies..."
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt >/dev/null 2>&1
        print_success "Dependencies installed"
    else
        print_warning "requirements.txt not found, skipping"
    fi
    echo ""
fi

# Step 8: Install package
if [ "$DEV_MODE" = true ]; then
    print_status "Installing package in development mode..."
    pip install -e .
    print_success "Package installed (editable mode)"
else
    print_status "Building package..."
    python -m build
    
    print_status "Installing package..."
    pip install dist/saini-*.whl --force-reinstall
    print_success "Package installed (production mode)"
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Installation completed successfully!   ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
echo ""

# Step 9: Verify installation
print_status "Verifying installation..."
if command -v saini &> /dev/null; then
    VERSION=$(saini --version 2>&1 | grep -oP '\d+\.\d+\.\d+' || echo "unknown")
    print_success "Saini installed successfully (version: $VERSION)"
else
    print_error "Installation verification failed"
    exit 1
fi

echo ""
echo -e "${CYAN}Quick Test Commands:${NC}"
echo "  saini --help              # Show all commands"
echo "  saini tree                # Show project tree"
echo "  saini start 'Test task'   # Start time tracking"
echo "  saini status              # Check status"
echo "  saini config show         # Show configuration"
echo ""

# Step 10: Run tests (optional)
read -p "$(echo -e ${YELLOW}Run quick tests? [y/N]:${NC} )" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    print_status "Running tests..."
    echo ""
    
    echo -e "${CYAN}Test 1: Show version${NC}"
    saini --version
    echo ""
    
    echo -e "${CYAN}Test 2: Show help${NC}"
    saini --help | head -20
    echo ""
    
    echo -e "${CYAN}Test 3: Show tree (limited depth)${NC}"
    saini tree -d 2
    echo ""
    
    echo -e "${CYAN}Test 4: Check config${NC}"
    saini config show
    echo ""
    
    print_success "All tests passed!"
fi

echo ""
echo -e "${GREEN}✓ Ready to use Saini!${NC}"
echo ""

# Helpful tips
echo -e "${BLUE}Development Tips:${NC}"
if [ "$DEV_MODE" = true ]; then
    echo "  • You're in development mode - changes to code will take effect immediately"
    echo "  • Run './install.sh -r' to reinstall after major changes"
else
    echo "  • You're in production mode - rebuild after making changes"
    echo "  • Run './install.sh -r -p' to reinstall"
fi
echo "  • Run './publish.sh' to publish to PyPI"
echo ""