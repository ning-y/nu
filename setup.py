import os
from setuptools import setup, find_packages

# Meta information
version = "0.0.0-snapshot3"

setup(
    # Basic info
    name="nu",
    version=version,
    author="ning",
    author_email="ningyuan.sg@gmail.com",
    url="https://github.com/ning-y/nu",
    description="Assorted utilities for ning's personal use.",
    long_description="Assorted utilities for ning's personal use.",
    classifiers=[
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Programming Language :: Python",
    ],

    # Packages and depencies
    py_modules=["nu"],
    install_requires=[
        "xdg",
    ],

    # Scripts
    entry_points={
        "console_scripts": [
            "nu = nu.__main__:main"],
    },
)
