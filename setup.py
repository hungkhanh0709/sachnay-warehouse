"""
Setup configuration for the Sachnay Warehouse package.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_path.exists():
    requirements = requirements_path.read_text(encoding="utf-8").strip().split("\n")

setup(
    name="sachnay-warehouse",
    version="1.0.0",
    author="hungkhanh0709",
    description="Vietnamese Book Data Scraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hungkhanh0709/sachnay-warehouse",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "sachnay-warehouse=sachnay_warehouse.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)