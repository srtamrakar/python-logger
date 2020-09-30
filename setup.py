from setuptools import setup, find_packages

module_version = "0.4.5"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

with open("requirements.txt", "r", encoding="utf-8") as f:
    dependencies_list = f.read().splitlines()

setup(
    name="NeatLogger",
    packages=find_packages(),
    version=module_version,
    license="MIT",
    description="Convenient wrapper for logging python applications, in the desired format, into the files with desired separation intervals.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Samyak Ratna Tamrakar",
    author_email="samyak.r.tamrakar@gmail.com",
    url="https://github.com/srtamrakar/python-logger",
    download_url=f"https://github.com/srtamrakar/python-logger/archive/v_{module_version}.tar.gz",
    keywords=["log", "logger", "logging", "apache", "json"],
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
