#!/usr/bin/env python
# coding: utf-8
"""
CherryPy CGI-Server Tool - Setup
 
Created
    2013-01-20 by Gerold - http://halvar.at/
"""

import os
import setuptools

THISDIR = os.path.dirname(os.path.abspath(__file__))
HOMEPAGE = "https://code.google.com/p/cherrypy-cgiserver/"
DOWNLOAD_BASEURL = "https://cherrypy-cgiserver.googlecode.com/files/"
VERSION = open(os.path.join(THISDIR, "version.txt")).readline().strip()
DOWNLOAD_URL = DOWNLOAD_BASEURL + "cherrypy-cgiserver-%s.tar.gz" % VERSION


setuptools.setup(
    name = "cherrypy-cgiserver",
    version = VERSION,
    description = (
        "Python CGI Server - Perfect To Deliver PHP Files Within A Python "
        "CherryPy Application"
    ),
    long_description = open(os.path.join(THISDIR, "README.txt")).read(),
    keywords = "CherryPy Web CGI Tool",
    author = "Gerold Penz",
    author_email = "gerold@halvar.at",
    url = HOMEPAGE,
    download_url = DOWNLOAD_URL,
    packages = [
        "cpcgiserver",
        "cpcgiserver.lib",
    ],
    classifiers = [
        "Development Status :: 4 - Beta",
        #"Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: CherryPy",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
    ],
#    install_requires = [
#        "cherrypy",
#    ],

)

