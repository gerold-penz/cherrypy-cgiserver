#!/usr/bin/env python
# coding: utf-8
"""
CherryPy CGI-Server Tool - Setup
 
Created
    2013-01-20 by Gerold - http://halvar.at/
"""

import os
from setuptools import setup, find_packages

THISDIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(THISDIR)

VERSION = open("version.txt").readline().strip()
HOMEPAGE = "http://gerold-penz.github.com/cherrypy-cgiserver/"
DOWNLOAD_BASEURL = "https://github.com/gerold-penz/cherrypy-cgiserver/raw/master/dist/"
DOWNLOAD_URL = DOWNLOAD_BASEURL + "cherrypy-cgiserver-%s.tar.gz" % VERSION


setup(
    name = "cherrypy-cgiserver",
    version = VERSION,
    description = (
        "Python CGI Server - Perfect To Deliver PHP Files Within A Python "
        "CherryPy Application"
    ),
    long_description = open("README.rst").read(),
    keywords = "CherryPy Web CGI Tool",
    author = "Gerold Penz",
    author_email = "gerold@halvar.at",
    url = HOMEPAGE,
    download_url = DOWNLOAD_URL,
    packages = find_packages(),
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: CherryPy",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
    ],
    install_requires = [
        # "distribute",
        # "cherrypy",
    ],
)

