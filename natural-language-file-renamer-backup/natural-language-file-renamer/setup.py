#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="natural-language-file-renamer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "python-dateutil>=2.8.0",
        "regex>=2023.6.3",
    ],
    entry_points={
        "console_scripts": [
            "rename=renamer.cli:cli",
        ],
    },
    author="Femirins",
    description="CLI tool to rename files using natural language.",
    license="MIT",
)