# setup.py
from setuptools import setup, find_packages

setup(
    name="donor-cli",
    version="0.1",
    packages=find_packages(),  # find 'donor' package
    install_requires=[
        "click",
        "SQLAlchemy",
    ],
    entry_points={
        "console_scripts": [
            "donor=donor.cli:cli",  # points to donor/cli.py -> cli function
        ],
    },
)
