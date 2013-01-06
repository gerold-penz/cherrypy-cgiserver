#!/usr/bin/env python
#coding: utf-8

import os
import sys
import cherrypy

THISDIR = os.path.dirname(os.path.abspath(__file__))
# Add app dir to path for testing cpcgiserver
APPDDIR = os.path.abspath(os.path.join(THISDIR, os.path.pardir, os.path.pardir))
sys.path.insert(0, APPDDIR)

import cpcgiserver


class Root(object): pass


def main():

    cherrypy.config.update({
        # Host
        "server.socket_host": "0.0.0.0",
        "server.socket_port": 8080,
        # Encoding der auszuliefernden HTML-Seiten
        "tools.encode.on": True,
        "tools.encode.encoding": "utf-8",
        "tools.decode.on": True,
        # URL Anpassung
        "tools.trailing_slash.on": True,
        # Gzip
        "tools.gzip.on": True,
    })

    config = {
        "/": {
            # Staticdir
            "tools.staticdir.on": True,
            "tools.staticdir.root": THISDIR,
            "tools.staticdir.dir": "php_files",
            "tools.staticdir.match": r"(?i)(gif|jpg|png|jpeg|js|7z|pdf|zip|svg|emf|avi|ods|css|ico|html|htm|p3p|swf|htc)$",
            # CgiServer
            "tools.cgiserver.on": True,
            "tools.cgiserver.root": THISDIR,
            "tools.cgiserver.dir": "php_files",
            "tools.cgiserver.base_url": "/",
            "tools.cgiserver.handlers": {".php": "/usr/bin/php-cgi"},
        }
    }
    app = cherrypy.Application(Root(), config = config)

    cherrypy.quickstart(app)


if __name__ == "__main__":
    main()

