#!/usr/bin/env python
# coding: utf-8
"""
CherryPy CGI-Server Tool - Setup
 
Created
    2013-01-20 by Gerold - http://halvar.at/
"""

import os
import sys
import distutils.core
from setuptools import setup, find_packages

# Upload zu Google-Code
# http://code.google.com/p/support/source/browse/#svn%2Ftrunk%2Fscripts
try:
    from googlecode_upload.googlecode_distutils_upload import upload
except ImportError:
    class upload(distutils.core.Command):
        user_options = []
        def __init__(self, *args, **kwargs):
            sys.stderr.write(
                "error: Install this module in site-packages to upload: \n"
                "http://support.googlecode.com/svn/trunk/scripts/googlecode_distutils_upload.py"
            )
            sys.exit(3)

THISDIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(THISDIR)

VERSION = open("version.txt").readline().strip()
HOMEPAGE = "http://gerold-penz.github.com/cherrypy-cgiserver/"
DOWNLOAD_BASEURL = "https://cherrypy-cgiserver.googlecode.com/files/"
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
#    data_files = [
#        ["./yyy", ["_git_add.py"]],
#    ],
    classifiers = [
        # "Development Status :: 4 - Beta",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: CherryPy",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
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
#        "distribute",
        "cherrypy",
    ],
    cmdclass = {"upload": upload},
)

