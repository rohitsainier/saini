#!/bin/bash

# Saini - Publishing Script
# Use this to publish your package to PyPI

set -e  # Exit on error

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${MAGENTA}╔════════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║      Saini - Publishing Script             ║${NC}"
echo -e "${MAGENTA}╚════════════════════════════════════════════╝${NC}"
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
TEST_PYPI=false
SKIP_TESTS=false
SKIP_BUILD=false
BUMP_VERSION=""
AUTO_YES=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--test)
            TEST_PYPI=true
            shift
            ;;
        --skip-tests)
            SKIP_TESTS=true
            shift
            ;;
        --skip-build)
            SKIP_BUILD=true
            shift
            ;;
        -v|--version)
            BUMP_VERSION="$2"
            shift 2
            ;;
        -y|--yes)
            AUTO_YES=true
            shift
            ;;
        -h|--help)
            echo "Usage: ./publish.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -t, --test         Publish to TestPyPI instead of PyPI"
            echo "  --skip-tests       Skip running tests before publishing"
            echo "  --skip-build       Skip building (use existing dist/)"
            echo "  -v, --version TYPE Bump version (major|minor|patch)"
            echo "  -y, --yes          Auto-confirm all prompts"
            echo "  -h, --help         Show this help message"
            echo ""
            echo "Examples:"
            echo "  ./publish.sh                    # Publish to PyPI"
            echo "  ./publish.sh -t                 # Test publish to TestPyPI"
            echo "  ./publish.sh -v patch           # Bump patch version and publish"
            echo "  ./publish.sh -t -y              # Auto-publish to TestPyPI"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use -h or --help for usage information"
            exit 1
            ;;
    esac
done

# Display configuration
echo -e "${YELLOW}Configuration:${NC}"
if [ "$TEST_PYPI" = true ]; then
    echo -e "  Target: ${CYAN}TestPyPI${NC} (test repository)"
else
    echo -e "  Target: ${MAGENTA}PyPI${NC} (production repository)"
fi
echo "  Skip tests: $SKIP_TESTS"
echo "  Skip build: $SKIP_BUILD"
[ -n "$BUMP_VERSION" ] && echo "  Version bump: $BUMP_VERSION"
echo ""

# Step 1: Check for uncommitted changes
print_status "Checking git status..."
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    print_warning "You have uncommitted changes"
    if [ "$AUTO_YES" = false ]; then
        read -p "$(echo -e ${YELLOW}Continue anyway? [y/N]:${NC} )" -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
else
    print_success "Working directory is clean"
fi
echo ""

# Step 2: Get current version
print_status "Reading current version..."
CURRENT_VERSION=$(python -c "import saini; print(saini.__version__)" 2>/dev/null || echo "0.0.0")
print_success "Current version: $CURRENT_VERSION"
echo ""

# Step 3: Bump version if requested
if [ -n "$BUMP_VERSION" ]; then
    print_status "Bumping version ($BUMP_VERSION)..."
    
    IFS='.' read -ra VERSION_PARTS <<< "$CURRENT_VERSION"
    MAJOR="${VERSION_PARTS[0]}"
    MINOR="${VERSION_PARTS[1]}"
    PATCH="${VERSION_PARTS[2]}"
    
    case "$BUMP_VERSION" in
        major)
            MAJOR=$((MAJOR + 1))
            MINOR=0
            PATCH=0
            ;;
        minor)
            MINOR=$((MINOR + 1))
            PATCH=0
            ;;
        patch)
            PATCH=$((PATCH + 1))
            ;;
        *)
            print_error "Invalid version type. Use: major, minor, or patch"
            exit 1
            ;;
    esac
    
    NEW_VERSION="$MAJOR.$MINOR.$PATCH"
    
    # Update version in files
    sed -i.bak "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" saini/__init__.py
    sed -i.bak "s/version=\".*\"/version=\"$NEW_VERSION\"/" setup.py
    rm -f saini/__init__.py.bak setup.py.bak
    
    print_success "Version bumped: $CURRENT_VERSION → $NEW_VERSION"
    
    # Commit version bump
    if [ "$AUTO_YES" = false ]; then
        read -p "$(echo -e ${YELLOW}Commit version bump? [Y/n]:${NC} )" -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            git add saini/__init__.py setup.py
            git commit -m "Bump version to $NEW_VERSION"
            git tag "v$NEW_VERSION"
            print_success "Version committed and tagged"
        fi
    else
        git add saini/__init__.py setup.py
        git commit -m "Bump version to $NEW_VERSION"
        git tag "v$NEW_VERSION"
        print_success "Version committed and tagged"
    fi
    
    CURRENT_VERSION=$NEW_VERSION
    echo ""
fi

# Step 4: Run tests (optional)
if [ "$SKIP_TESTS" = false ]; then
    print_status "Running tests..."
    
    # Check if tests exist
    if [ -d "tests" ] || [ -f "test_*.py" ]; then
        if command -v pytest &> /dev/null; then
            pytest || {
                print_error "Tests failed"
                exit 1
            }
            print_success "All tests passed"
        else
            print_warning "pytest not found, skipping tests"
        fi
    else
        print_warning "No tests found, skipping"
    fi
    echo ""
fi

# Step 5: Clean previous builds
print_status "Cleaning previous builds..."
rm -rf build/
rm -rf dist/
rm -rf *.egg-info
rm -rf saini.egg-info
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
print_success "Cleaned"
echo ""

# Step 6: Install/upgrade build tools
print_status "Installing build tools..."
pip install --upgrade build twine >/dev/null 2>&1
print_success "Build tools ready"
echo ""

# Step 7: Build package
if [ "$SKIP_BUILD" = false ]; then
    print_status "Building package..."
    python -m build
    print_success "Package built"
    echo ""
    
    # Show build artifacts
    print_status "Build artifacts:"
    ls -lh dist/
    echo ""
fi

# Step 8: Check package
print_status "Checking package..."
twine check dist/*
print_success "Package check passed"
echo ""

# Step 9: Check for PyPI credentials
if [ ! -f "$HOME/.pypirc" ]; then
    print_warning "No ~/.pypirc found"
    echo ""
    echo "To avoid entering credentials each time, create ~/.pypirc:"
    echo ""
    if [ "$TEST_PYPI" = true ]; then
        echo "  [testpypi]"
        echo "  repository = https://test.pypi.org/legacy/"
        echo "  username = __token__"
        echo "  password = pypi-YOUR_TEST_PYPI_TOKEN_HERE"
        echo ""
        echo "Get your token from: https://test.pypi.org/manage/account/token/"
    else
        echo "  [pypi]"
        echo "  repository = https://upload.pypi.org/legacy/"
        echo "  username = __token__"
        echo "  password = pypi-YOUR_PYPI_TOKEN_HERE"
        echo ""
        echo "Get your token from: https://pypi.org/manage/account/token/"
    fi
    echo ""
    echo "Then run: chmod 600 ~/.pypirc"
    echo ""
    
    if [ "$AUTO_YES" = false ]; then
        read -p "$(echo -e ${YELLOW}Continue with manual token entry? [Y/n]:${NC} )" -n 1 -r
        echo
        if [[ $REPLY =~ ^[Nn]$ ]]; then
            exit 0
        fi
    fi
    echo ""
fi

# Step 10: Confirm before upload
if [ "$AUTO_YES" = false ]; then
    echo -e "${YELLOW}╔════════════════════════════════════════════╗${NC}"
    echo -e "${YELLOW}║           Ready to Publish!                ║${NC}"
    echo -e "${YELLOW}╚════════════════════════════════════════════╝${NC}"
    echo ""
    echo "  Package: saini"
    echo "  Version: $CURRENT_VERSION"
    if [ "$TEST_PYPI" = true ]; then
        echo -e "  Target:  ${CYAN}TestPyPI${NC}"
        echo ""
        echo -e "${CYAN}After publishing to TestPyPI, you can test install with:${NC}"
        echo "  pip install --index-url https://test.pypi.org/simple/ saini"
    else
        echo -e "  Target:  ${MAGENTA}PyPI (PRODUCTION)${NC}"
        echo ""
        echo -e "${RED}⚠ WARNING: This will publish to the PRODUCTION PyPI!${NC}"
    fi
    echo ""
    
    read -p "$(echo -e ${YELLOW}Continue with upload? [y/N]:${NC} )" -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Upload cancelled"
        exit 0
    fi
    echo ""
fi

# Step 11: Upload to PyPI
print_status "Uploading to $([ "$TEST_PYPI" = true ] && echo "TestPyPI" || echo "PyPI")..."

if [ "$TEST_PYPI" = true ]; then
    # Upload to TestPyPI
    python -m twine upload --repository testpypi dist/*
    
    echo ""
    print_success "Successfully published to TestPyPI!"
    echo ""
    echo -e "${CYAN}Test installation:${NC}"
    echo "  pip install --index-url https://test.pypi.org/simple/ saini"
    echo ""
    echo -e "${CYAN}View on TestPyPI:${NC}"
    echo "  https://test.pypi.org/project/saini/"
else
    # Upload to PyPI
    python -m twine upload dist/*
    
    echo ""
    print_success "Successfully published to PyPI!"
    echo ""
    echo -e "${CYAN}Installation:${NC}"
    echo "  pip install saini"
    echo ""
    echo -e "${CYAN}View on PyPI:${NC}"
    echo "  https://pypi.org/project/saini/"
    echo ""
    echo -e "${CYAN}Documentation:${NC}"
    echo "  https://github.com/yourusername/saini"
fi

echo ""

# Step 12: Push to git (if version was bumped)
if [ -n "$BUMP_VERSION" ]; then
    if [ "$AUTO_YES" = false ]; then
        read -p "$(echo -e ${YELLOW}Push to git repository? [Y/n]:${NC} )" -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            print_status "Pushing to git..."
            git push
            git push --tags
            print_success "Pushed to git with tags"
        fi
    else
        print_status "Pushing to git..."
        git push
        git push --tags
        print_success "Pushed to git with tags"
    fi
    echo ""
fi

# Step 13: Final message
echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║    Publishing completed successfully! 🎉   ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
echo ""

if [ "$TEST_PYPI" = true ]; then
    echo -e "${YELLOW}Next steps:${NC}"
    echo "  1. Test the package from TestPyPI:"
    echo "     pip install --index-url https://test.pypi.org/simple/ saini"
    echo ""
    echo "  2. If everything works, publish to production:"
    echo "     ./publish.sh"
else
    echo -e "${YELLOW}What's next:${NC}"
    echo "  1. Share your package:"
    echo "     pip install saini"
    echo ""
    echo "  2. Create a GitHub release:"
    echo "     https://github.com/rohitsainier/saini/releases/new"
    echo ""
    echo "  3. Update your documentation"
    echo ""
    echo "  4. Announce on social media! 🚀"
fi
echo ""

# Step 14: Show package stats (if on PyPI)
if [ "$TEST_PYPI" = false ]; then
    echo -e "${CYAN}Package links:${NC}"
    echo "  PyPI: https://pypi.org/project/saini/"
    echo "  Install: pip install saini"
    echo "  Docs: https://github.com/rohitsainier/saini"
    echo ""
fi

# Optional: Open browser
if [ "$AUTO_YES" = false ]; then
    read -p "$(echo -e ${YELLOW}Open package page in browser? [Y/n]:${NC} )" -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        if [ "$TEST_PYPI" = true ]; then
            open "https://test.pypi.org/project/saini/" 2>/dev/null || xdg-open "https://test.pypi.org/project/saini/" 2>/dev/null || echo "Visit: https://test.pypi.org/project/saini/"
        else
            open "https://pypi.org/project/saini/" 2>/dev/null || xdg-open "https://pypi.org/project/saini/" 2>/dev/null || echo "Visit: https://pypi.org/project/saini/"
        fi
    fi
fi

echo ""
print_success "All done! 🎊"
echo ""