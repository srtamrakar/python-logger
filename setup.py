import os
import re

from setuptools import find_packages, setup

ROOT = os.path.dirname(__file__)
MODULE_NAME = "NeatLogger"


def get_author() -> str:
    author_re = re.compile(r"""__author__ = ['"]([A-Za-z .]+)['"]""")
    init = open(os.path.join(ROOT, MODULE_NAME, "__init__.py")).read()
    return author_re.search(init).group(1)


def get_version() -> str:
    version_re = re.compile(r"""__version__ = ['"]([0-9.]+)['"]""")
    init = open(os.path.join(ROOT, MODULE_NAME, "__init__.py")).read()
    return version_re.search(init).group(1)


def get_description() -> str:
    with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as f:
        description = f.read()
    return description


dependencies_list = [
    "colorama==0.4.3",
    "multiprocessing-logging==0.3.1",
    "pyfiglet==0.7",
    "python-json-logger==2.0.0",
]

setup(
    name=MODULE_NAME,
    packages=find_packages(),
    version=get_version(),
    license="MIT",
    description="Convenient wrapper for logging python applications with options to add color, select logging style, rotate files by size and time, etc.",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    author=get_author(),
    url="https://github.com/srtamrakar/python-logger",
    download_url=f"https://github.com/srtamrakar/python-logger/archive/v_{get_version()}.tar.gz",
    keywords=["log", "logger", "logging", "apache", "json", "color"],
    install_requires=dependencies_list,
    setup_requires=dependencies_list,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
    ],
)
