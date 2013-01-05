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


class Root(object):

    def index(self, *args, **kwargs):

        return u"OK"

    index.exposed = True


    # CGI Umgebungsvariablen:
    # http://de.selfhtml.org/servercgi/cgi/umgebungsvariablen.htm
    # CGI-RFCs:
    # http://tools.ietf.org/html/rfc3875
    # http://tools.ietf.org/html/draft-robinson-www-interface-00


    def default(self, *args, **kwargs):

        #return repr(args) + " - " + repr(kwargs)

        if args[0] == PHPDIRNAME:

            cmd_args = ["php5-cgi", os.path.join(PHPDIR, "phpinfo.php")]

            proc = subprocess.Popen(
                cmd_args,
                executable = "php5-cgi",
                stdout = subprocess.PIPE,
                stderr = subprocess.STDOUT,
            )

            return proc.stdout.read()

        else:
            raise cherrypy.NotFound()

    default.exposed = True


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

