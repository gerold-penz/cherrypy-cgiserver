#!/usr/bin/env python
#coding: utf-8

"""
First tests with cherrypy tools framework

Created
    2013-01-05 by Gerold - http://halvar.at/
"""

import os
import cherrypy
import subprocess

THISDIR = os.path.dirname(os.path.abspath(__file__))
PHPDIRNAME = "php_files"
PHPDIR = os.path.join(THISDIR, PHPDIRNAME)


class CgiServer(cherrypy._cptools.Tool):
    """
    Erster Test mit einer Tool-Klasse
    """

    def __init__(self):
        """
        Initialisiert die Tool-Klasse

        Beim Initialisieren werden Hook-Punkt, Name, Priorität, usw. festgelegt.
        """

        self._point = "on_start_resource"
        self._name = "cgiserver"
        self._priority = 50
        self.__doc__ = self.callable.__doc__
        self._setargs()


    def callable(self):
        """
        """

        print
        print "CgiServer callable ..."
        print

        cmd_args = ["php5-cgi", os.path.join(PHPDIR, "phpinfo.php")]

        proc = subprocess.Popen(
            cmd_args,
            executable = "php5-cgi",
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
        )

        print
        print "PHP called"
        print

        header_processed = False
        header_list = []
        for line in proc.stdout:
            if not line.rstrip():
                header_processed = True
            if header_processed:
                print "Line:", line
                cherrypy.serving.response.body.append(line)
            else:
                header_list.append(line.rstrip())

        print
        print "PHP return values --> body"
        print

        # return header_list
        cherrypy.serving.response.header_list = header_list

        # no more request handler needed
        cherrypy.serving.request.handler = None





cherrypy.tools.cgiserver = CgiServer()


class Root(object):

    def index(self, *args, **kwargs):

        return u"OK"

    index.exposed = True


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

        # CgiServer
        "tools.cgiserver.on": True
    })

#    config = {
#        "/": {
#            "tools.staticdir.root": THISDIR,
#            "tools.staticdir.on": True,
#            "tools.staticdir.dir": "",
#        }
#    }


    app = cherrypy.Application(Root())

    cherrypy.quickstart(app)


if __name__ == "__main__":
    main()

