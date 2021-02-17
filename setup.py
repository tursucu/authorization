#!/usr/bin/env python

import sys

from setuptools import setup, find_packages


install_requires = [
    "pyjwt"
]

# Require python 3.8
if sys.version_info.major != 3 and sys.version_info.minor != 8:
    sys.exit("Authorization requires Python 3.8.")

setup(
    name="authorization",
    version="1.0.0",  # Keep the Kog version at parity with the Riot API major version, use the minor version for breaking changes, and the patch version for everything else
    author="Mehmet TURŞUCU",
    author_email="team@report.gg",
    url="https://github.com/tursucu/kogmaw",
    description="Report.GG GraphQL Auth Wrapper (1rd Party)",
    keywords=["Auth", "API", "REST"],
    classifiers=[
        "Development Status :: 1 - Beta",
        "Programming Language :: Python :: 3",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Games/Entertainment",
        "Topic :: Games/Entertainment :: Real Time Strategy",
        "Topic :: Games/Entertainment :: Role-Playing",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT",
    packages=find_packages(),
    zip_safe=True,
    install_requires=install_requires,
    include_package_data=True
)