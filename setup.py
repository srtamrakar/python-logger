import os
from setuptools import setup, find_packages

module_version = "0.4.8"

with open(
    os.path.join(os.path.dirname(__file__), "README.md"), "r", encoding="utf-8"
) as f:
    long_description = f.read()

dependencies_list = [
    "colorama==0.4.3",
    "multiprocessing-logging==0.3.1",
    "pyfiglet==0.7",
    "python-json-logger==2.0.0",
]

setup(
    name="NeatLogger",
    packages=find_packages(),
    version=module_version,
    license="MIT",
    description="Convenient wrapper for logging python applications with options to add color, select logging style, rotate files by size and time, etc.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Samyak Ratna Tamrakar",
    author_email="samyak.r.tamrakar@gmail.com",
    url="https://github.com/srtamrakar/python-logger",
    download_url=f"https://github.com/srtamrakar/python-logger/archive/v_{module_version}.tar.gz",
    keywords=["log", "logger", "logging", "apache", "json", "color"],
    install_requires=dependencies_list,
    setup_requires=dependencies_list,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
