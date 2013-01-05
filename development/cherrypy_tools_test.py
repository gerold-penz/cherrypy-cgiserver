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
from cherrypy.wsgiserver import wsgiserver2

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

        cherrypy.log(" ")
        cherrypy.log(repr(dir(cherrypy.request)))
        cherrypy.log(" ")

# cherrypy.request
#        [
#            '__attrname__',
#            '__bool__',
#            '__class__',
#            '__contains__'
#            '__delattr__'
#            '__delitem__'
#            '__dict__'
#            '__doc__'
#            '__format__'
#            '__getattr__'
#            '__getattribute__'
#            '__getitem__'
#            '__hash__'
#            '__init__'
#            '__len__'
#            '__module__'
#            '__new__'
#            '__nonzero__'
#            '__reduce__'
#            '__reduce_ex__'
#            '__repr__'
#            '__setattr__'
#            '__setitem__'
#            '__sizeof__'
#            '__slots__'
#            '__str__'
#            '__subclasshook__'
#            '__weakref__'
#            '_get_body_params'
#            '_get_dict'
#            'app'
#            'base'
#            'body'
#            'body_params'
#            'close'
#            'closed'
#            'config'
#            'cookie'
#            'dispatch'
#            'error_page'
#            'error_response'
#            'get_resource'
#            'handle_error'
#            'handler'
#            'header_list'
#            'headers'
#            'hooks'
#            'is_index'
#            'local'
#            'login'
#            'method'
#            'methods_with_bodies'
#            'multiprocess'
#            'multithread'
#            'namespaces'
#            'params'
#            'path_info'
#            'prev'
#            'process_headers'
#            'process_query_string'
#            'process_request_body'
#            'protocol'
#            'query_string'
#            'query_string_encoding'
#            'remote'
#            'request_line'
#            'respond'
#            'rfile'
#            'run'
#            'scheme'
#            'script_name'
#            'server_protocol'
#            'show_mismatched_params'
#            'show_tracebacks'
#            'stage'
#            'throw_errors'
#            'throws'
#            'toolmaps'
#            'wsgi_environ'
#        ]

# cherrypy.request.headers
#        {
#            'Remote-Addr': '127.0.0.1',
#            'Accept-Language': 'de-de,de;q=0.8,en-us;q=0.5,en;q=0.3',
#            'Accept-Encoding': 'gzip, deflate',
#            'Connection': 'keep-alive',
#            'Accept': 'image/png,image/*;q=0.8,*/*;q=0.5',
#            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0',
#            'Host': 'localhost:8080',
#            'Referer': 'http://localhost:8080/'
#        }


        # ToDo: Prepare environment for CGI callable


        # Call PHP interpreter
        cmd_args = ["php5-cgi", os.path.join(PHPDIR, "phpinfo.php")]
        proc = subprocess.Popen(
            cmd_args,
            executable = "php5-cgi",
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            env = {}
        )

        # Get headers
        cherrypy.serving.response.headers = wsgiserver2.read_headers(
            proc.stdout, cherrypy.serving.response.headers
        )

        # Get body
        cherrypy.serving.response.body = proc.stdout

        # Finished: no more request handler needed
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

