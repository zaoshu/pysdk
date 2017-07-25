#!/usr/bin/env python3
# coding=utf-8
from __future__ import print_function
from setuptools import setup, find_packages
import sys

setup(
    name="zaoshu",
    version="0.1.1",
    author="Kevin Cheng",
    author_email="cheng1483x@gmail.com",
    description="zaoshu包实现里对造数openapi功能的封装，使开发人员专注于功能的实现，提高开发效率。 ",
    long_description=open("README.rst").read(),
    license="MIT",
    url="https://github.com/zaoshu/pysdk",
    packages=['zaoshu'],
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Development Status :: 4 - Beta"
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: Free For Home Use",
        "Natural Language :: Chinese (Simplified)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3 :: Only",

    ],
)
