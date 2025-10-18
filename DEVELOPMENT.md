# Saini Development Guide

## Quick Commands

### Installation
```bash
./install.sh          # Install for development
./install.sh -r       # Reinstall
./install.sh -c       # Clean install
./install.sh -p       # Production install


./publish.sh -t       # Test publish (TestPyPI)
./publish.sh          # Production publish (PyPI)
./publish.sh -v patch # Bump patch & publish
./publish.sh -v minor # Bump minor & publish
./publish.sh -v major # Bump major & publish

python version.py current      # Show version
python version.py bump patch   # Bump patch
python version.py bump minor   # Bump minor
python version.py bump major   # Bump major
python version.py set 1.2.3    # Set specific version

make install          # Install
make reinstall        # Reinstall
make test-publish     # Test publish
make publish          # Publish
make version-patch    # Bump patch