########################
CherryPy CGI Server Tool
########################

Mit dem CherryPy_ Tool *cherrypy-cgiserver* kann man aus CherryPy einen
vollwertigen CGI-Server (Common Gateway Interface) machen.
Damit lassen sich sogar PHP-Dateien ausführen und ausliefern.
Es muss nur der PHP-Interpreter auf dem Computer installiert sein.
Ein zusätzlicher Apache-Server ist nicht nötig.

.. _CherryPy: http://www.cherrypy.org/

So einfach lässt sich aus CherryPy ein vollwertiger PHP-Server machen:

.. code:: python

    #!/usr/bin/env python
    # coding: utf-8

    import os
    import cherrypy
    import cpcgiserver

    THISDIR = os.path.dirname(os.path.abspath(__file__))

    def main():
        config = {
            "global": {
                "server.socket_host": "0.0.0.0",
                "server.socket_port": 8080,
            },
            "/": {
                "tools.cgiserver.on": True,
                "tools.cgiserver.dir": THISDIR,
                "tools.cgiserver.base_url": "/",
                "tools.cgiserver.handlers": {".php": "/usr/bin/php-cgi"},
            }
        }
        app = cherrypy.Application(None, config = config)
        cherrypy.quickstart(app, config = config)

    if __name__ == "__main__":
        main()


=====
Links
=====

- Quellcode: https://github.com/gerold-penz/cherrypy-cgiserver


========
Lizenzen
========

Jeder (ohne Ausnahme) darf diesen Code verwenden. Dafür habe ich den Code unter
zwei Lizenzen gestellt -- frei wählbar.

**LGPL:**

- http://www.gnu.org/licenses/lgpl.html (english)
- http://www.gnu.de/documents/lgpl.de.html (deutsch)

**MIT:**

- http://opensource.org/licenses/MIT (english)
- http://de.wikipedia.org/wiki/MIT-Lizenz (deutsch)


======
Inhalt
======

.. toctree::
   :maxdepth: 1

   installation/index.rst






.. ==================
   Indices and tables
   ==================

   * :ref:`genindex`
   * :ref:`modindex`
   * :ref:`search`
