.PHONY: help install reinstall clean test build publish test-publish

help:
	@echo "Saini - Development Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install        Install package locally (development mode)"
	@echo "  make reinstall      Reinstall package"
	@echo "  make clean          Clean build artifacts"
	@echo "  make test           Run tests"
	@echo "  make build          Build package"
	@echo "  make test-publish   Publish to TestPyPI"
	@echo "  make publish        Publish to PyPI"
	@echo "  make version-patch  Bump patch version"
	@echo "  make version-minor  Bump minor version"
	@echo "  make version-major  Bump major version"

install:
	@./install.sh

reinstall:
	@./install.sh -r

clean:
	@./install.sh -c
	@rm -rf build/ dist/ *.egg-info
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "✓ Cleaned"

test:
	@pytest tests/ -v

build:
	@./install.sh -c
	@python -m build
	@echo "✓ Package built"

test-publish:
	@./publish.sh -t

publish:
	@./publish.sh

version-patch:
	@python version.py bump patch

version-minor:
	@python version.py bump minor

version-major:
	@python version.py bump major