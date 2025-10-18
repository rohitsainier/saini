from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="saini",
    version="1.0.0",
    description="Developer productivity tools: time tracking, project tree, and more",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rohitsainier/saini",
    author="Rohit Saini",
    author_email="rohitsainier@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Tools",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="developer tools, time tracking, pomodoro, productivity, project tree, git",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "click>=8.0.0",
        "rich>=10.0.0",
        "gitpython>=3.1.0",
        "pandas>=1.3.0",
        "tabulate>=0.8.9",
    ],
    entry_points={
        "console_scripts": [
            "saini=saini.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/rohitsainier/saini/issues",
        "Source": "https://github.com/rohitsainier/saini",
    },
)