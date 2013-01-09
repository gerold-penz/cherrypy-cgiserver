#!/usr/bin/env python
#coding: utf-8
"""
Simple PHP-Server Example

Links to the PHP pages:

- http://localhost:8080/testsubdir/simple_page.php
- http://localhost:8080/testsubdir/phpinfo.php

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
        "/testsubdir": {
            # Enable CgiServer
            "tools.cgiserver.on": True,
            # Directory with PHP files
            "tools.cgiserver.dir": os.path.join(THISDIR, "testsubdir"),
            # URL for directory with PHP files
            "tools.cgiserver.base_url": "/testsubdir",
            # Connect PHP extension with PHP interpreter program
            "tools.cgiserver.handlers": {".php": "/usr/bin/php-cgi"},
        }
    }

    # Create and start application
    app = cherrypy.Application(None, config = config)
    cherrypy.quickstart(app, config = config)


if __name__ == "__main__":
    main()

