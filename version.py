#!/usr/bin/env python3
"""Version management helper script."""

import re
import sys
from pathlib import Path


def get_current_version():
    """Get current version from __init__.py."""
    init_file = Path(__file__).parent / 'saini' / '__init__.py'
    content = init_file.read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if match:
        return match.group(1)
    return "0.0.0"


def bump_version(version, bump_type='patch'):
    """Bump version number."""
    major, minor, patch = map(int, version.split('.'))
    
    if bump_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif bump_type == 'minor':
        minor += 1
        patch = 0
    elif bump_type == 'patch':
        patch += 1
    else:
        raise ValueError(f"Invalid bump type: {bump_type}")
    
    return f"{major}.{minor}.{patch}"


def update_version(new_version):
    """Update version in all files."""
    files_to_update = [
        Path(__file__).parent / 'saini' / '__init__.py',
        Path(__file__).parent / 'setup.py',
    ]
    
    for file_path in files_to_update:
        if not file_path.exists():
            continue
        
        content = file_path.read_text()
        
        # Update version string
        content = re.sub(
            r'(__version__|version)\s*=\s*["\'][^"\']+["\']',
            f'\\1="{new_version}"',
            content
        )
        
        file_path.write_text(content)
        print(f"✓ Updated {file_path.name}")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python version.py [current|bump <type>|set <version>]")
        print("\nExamples:")
        print("  python version.py current          # Show current version")
        print("  python version.py bump patch       # Bump patch version")
        print("  python version.py bump minor       # Bump minor version")
        print("  python version.py bump major       # Bump major version")
        print("  python version.py set 1.2.3        # Set specific version")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'current':
        version = get_current_version()
        print(f"Current version: {version}")
    
    elif command == 'bump':
        if len(sys.argv) < 3:
            print("Error: Specify bump type (major|minor|patch)")
            sys.exit(1)
        
        bump_type = sys.argv[2]
        current = get_current_version()
        new_version = bump_version(current, bump_type)
        
        print(f"Bumping version: {current} → {new_version}")
        update_version(new_version)
        print(f"\n✓ Version bumped to {new_version}")
    
    elif command == 'set':
        if len(sys.argv) < 3:
            print("Error: Specify version number")
            sys.exit(1)
        
        new_version = sys.argv[2]
        current = get_current_version()
        
        print(f"Setting version: {current} → {new_version}")
        update_version(new_version)
        print(f"\n✓ Version set to {new_version}")
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()