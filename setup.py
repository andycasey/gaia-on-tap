# coding: utf-8

""" Gaia on TAP """ 

import os
import re
import sys

try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup

major, minor1, minor2, release, serial =  sys.version_info
open_kwargs = {"encoding": "utf-8"} if major >= 3 else {}

def rf(filename):
    with open(filename, **open_kwargs) as fp:
        contents = fp.read()
    return contents

version_regex = re.compile("__version__ = \"(.*?)\"")
contents = rf(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "code", "__init__.py"))

version = version_regex.findall(contents)[0]

setup(name="gaia-on-tap",
    version=version,
    author="Andrew R. Casey",
    author_email="arc@ast.cam.ac.uk",
    packages=["gaia"],
    package_dir=dict(gaia="code"),
    url="http://www.github.com/andycasey/gaia-on-tap/",
    license="MIT",
    description="Utilities and tutorials for accessing Gaia data using TAP",
    long_description=rf(os.path.join(os.path.dirname(__file__), "README.md")),
    install_requires=rf(
        os.path.join(os.path.dirname(__file__), "REQUIREMENTS.md")).split("\n"),
    entry_points={}
)
