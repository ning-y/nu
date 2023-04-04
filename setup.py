import os
from setuptools import setup, find_packages

# Meta information
version = "0.0.0-snapshot7"

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

    # Dependencies
    install_requires=[
        "xdg",
    ],

    # # Scripts
    # entry_points={
    #     "console_scripts": [
    #         "nu = nu.__main__:main"],
    # },
)
