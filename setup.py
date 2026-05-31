from setuptools import setup

setup(
    name="nlrename",
    version="0.1.0",
    py_modules=["nlrename"],
    install_requires=[
        "click>=8.0.0",
        "python-dateutil>=2.8.0",
    ],
    entry_points={
        "console_scripts": [
            "nlrename=nlrename:cli",
        ],
    },
)