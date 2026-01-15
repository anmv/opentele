import pathlib
from setuptools import setup
import re

README = (pathlib.Path(__file__).parent / "README.md").read_text()

PACKAGE_NAME = "opentele"
VERSION = "1.15.1"
SOURCE_DIRECTORY = "src"

with open("requirements.txt") as data:
    requirements = [
        line for line in data.read().split("\n") if line and not line.startswith("#")
    ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    license="MIT",
    description="A Python library for generating official Telegram API client data (device models, system versions, API credentials).",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/thedemons/opentele",
    author="thedemons",
    author_email="thedemons@gmail.com",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 5 - Production/Stable",
    ],
    keywords=[
        "telegram",
        "api",
        "opentele",
        "device",
    ],
    include_package_data=True,
    packages=[PACKAGE_NAME],
    package_dir={PACKAGE_NAME: SOURCE_DIRECTORY},
    install_requires=requirements,
)
