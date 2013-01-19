#!/usr/bin/env python
#coding: utf-8
"""
Simple Python-CGI-Server Example

Links to the Python-CGI pages:

- http://localhost:8080/simple_page.py
"""

import os
import sys
import cherrypy

THISDIR = os.path.dirname(os.path.abspath(__file__))
# Add app dir to path for testing cpcgiserver
APPDDIR = os.path.abspath(os.path.join(THISDIR, os.path.pardir, os.path.pardir))
sys.path.insert(0, APPDDIR)

import cpcgiserver


def main():

    config = {
        "global": {
            # Server settings
            "server.socket_host": "0.0.0.0",
            "server.socket_port": 8080,
        },
        "/": {
            # Enable CgiServer
            "tools.cgiserver.on": True,
            # Directory with Python-CGI files
            "tools.cgiserver.dir": os.path.join(THISDIR, "pycgi"),
            # URL for directory with Python-CGI files
            "tools.cgiserver.base_url": "/",
            # Connect Python extension with Python interpreter program
            "tools.cgiserver.handlers": {".py": "/usr/bin/python"},
        }
    }

    # Create and start application
    app = cherrypy.Application(None, config = config)
    cherrypy.quickstart(app, config = config)


if __name__ == "__main__":
    main()

