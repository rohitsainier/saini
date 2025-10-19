from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Read README
try:
    long_description = (here / "README.md").read_text(encoding="utf-8")
except FileNotFoundError:
    long_description = "Developer productivity tools: time tracking, project tree, and more"

setup(
    name="saini",
    version="1.0.5",
    
    # Description
    description="Developer productivity toolkit: time tracking, Pomodoro timer, project tree visualization, and automation tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    
    # URLs
    url="https://github.com/rohitsainier/saini",
    
    # Author
    author="Rohit Saini",
    author_email="rohitsainier@gmail.com",
    
    # Classifiers - ALL VALID
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    
    # Keywords
    keywords="git time-tracking pomodoro productivity developer-tools project-tree cli automation",
    
    # Packages
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    
    # Python version
    python_requires=">=3.7, <4",
    
    # Dependencies
    install_requires=[
        "click>=8.0.0",
        "rich>=10.0.0",
        "gitpython>=3.1.0",
        "pandas>=1.3.0",
        "tabulate>=0.8.9",
    ],
    
    # Extra dependencies
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.950",
        ],
    },
    
    # Entry points
    entry_points={
        "console_scripts": [
            "saini=saini.cli:main",
        ],
    },
    
    # Project URLs
    project_urls={
        "Bug Reports": "https://github.com/rohitsainier/saini/issues",
        "Source": "https://github.com/rohitsainier/saini",
        "Documentation": "https://github.com/rohitsainier/saini#readme",
    },
    
    # Include additional files
    include_package_data=True,
    
    # Zip safe
    zip_safe=False,
)