from setuptools import setup, find_packages

setup(
    
    name="sbom-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click>=8.0",
        "pymongo>=4.0",
    ],
    entry_points={
        "console_scripts": [
            "sbom-cli=sbom_cli.cli:cli",
        ],
    },
    python_requires=">=3.9",
    author="Ryan Schulman",
    description="CLI tool to ingest CycloneDX 1.6 SBOMs into MongoDB",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
