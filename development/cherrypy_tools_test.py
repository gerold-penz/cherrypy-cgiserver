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
import urlparse
from cStringIO import StringIO
from cherrypy.wsgiserver import wsgiserver2
from cherrypy._cpcompat import unquote

THISDIR = os.path.dirname(os.path.abspath(__file__))
PHPDIRNAME = "php_files"
PHPDIR = os.path.join(THISDIR, PHPDIRNAME)


def safe_unicode(value):
    """
    Versucht den übergebenen Wert als Unicode-String zurück zu geben, auch wenn
    dabei Informationen verloren gehen.
    """

    try:
        return unicode(value)
    except UnicodeDecodeError:
        try:
            return unicode(value, "utf-8")
        except UnicodeDecodeError:
            return unicode(value, "iso-8859-15", "ignore")
        except StandardError, err:
            return unicode(repr(value))
    except StandardError, err:
        return unicode(repr(value))


def show_request():
    """
    Zeigt die Attribute des Requests als Text an.
    """
    from pprint import pformat

    retstr = u"<pre>"
    for key, value in cherrypy.request.__dict__.items():
        value = safe_unicode(value)
        retstr += u"%s: %s\n\n" % (
            key,
            pformat(value).replace("\\n", "\n")
        )
    retstr += u"</pre>"

    return unicode(retstr)


class CgiServer(cherrypy._cptools.Tool):
    """
    Erster Test mit einer Tool-Klasse
    """

    def __init__(self):
        """
        Initialisiert die Tool-Klasse

        Beim Initialisieren werden Hook-Punkt, Name, Priorität, usw. festgelegt.
        """

        cherrypy._cptools.Tool.__init__(
            self,
            point = "on_start_resource",
            callable = self.callable,
            name = "cgiserver",
            priority = 50
        )


    def callable(self, base_url, dir, root="", handlers = None):
        """
        Verwandelt CherryPy in einen CGI-Server

        :param base_url: Absolute HTTP-URL of the CGI base directory.
            z.B.: "/cgi"

        :param dir: Absoluter oder relativer Pfad zum Ordner mit den CGI-Dateien.
            Wird der Pfad relativ angegeben, dann wird er an *root* angehängt.
            Gleiches Verhalten wie beim Staticdir-Tool.

        :param root: An diesen Pfad wird *dir* angehängt, falls *dir* nicht
            absolut übergeben wurde.

        :param handlers: Dictionary mit den Dateiendungen und den
            zugehörigen Interpretern. z.B.::

                {".php": "/usr/bin/php-cgi", ".py": "/usr/bin/python"}

            Es werden nur Dateien ausgeführt, denen ein Handler zugewiesen
            wurde. Wird die Dateiendung nicht im Dictionary gefunden, wird
            das Tool beendet, so dass die Abarbeitung des Requests z.B. von
            Staticdir ausgeliefert werden kann.
        """

        # short names for request and headers
        request = cherrypy.request
        headers = request.headers

        # Allow the use of '~' to refer to a user's home directory.
        # (copied from *cherrypy.lib.static*)
        dir = os.path.expanduser(dir)

        # If dir is relative, make absolute using "root".
        # (copied from *cherrypy.lib.static*)
        if not os.path.isabs(dir):
            if not root:
                msg = "Static dir requires an absolute dir (or root)."
                cherrypy.log(msg, 'TOOLS.CGISERVER')
                raise ValueError(msg)
            dir = os.path.join(root, dir)

        # Determine where we are in the object tree relative to 'base_url'
        # (copied from *cherrypy.lib.static*)
        if base_url == "":
            base_url = "/"
        base_url = base_url.rstrip(r"\/")
        branch = request.path_info[len(base_url) + 1:]
        branch = unquote(branch.lstrip(r"\/"))

        # Dateiname des Skriptes ermitteln (Es muss auf angehängte Pfade geachtet werden.)
        # Dabei wird auch der an die URL des Skriptes angehängte Pfad ermittelt
        branch_items = branch.split("/")
        script_filename = None
        path_info_start = None
        path_info = ""
        for i in range(len(branch_items), 0, -1):
            _file_path = os.path.join(dir, *branch_items[:i])
            if os.path.isfile(_file_path):
                script_filename = _file_path
                path_info_start = i
                break
        if not path_info_start is None and branch_items[path_info_start:]:
            path_info = "/" + "/".join(branch_items[path_info_start:])
        if not script_filename:
            return

        # URL des Skriptes ermitteln
        script_name = script_filename[len(dir):]

        # There's a chance that the branch pulled from the URL might
        # have ".." or similar uplevel attacks in it. Check that the final
        # filename is a child of dir.
        # (copied from *cherrypy.lib.static*)
        if not os.path.normpath(script_filename).startswith(os.path.normpath(dir)):
            raise cherrypy.HTTPError(403) # Forbidden

        # Wenn Dateiendung unbekannt, dann Funktion beenden, damit ein
        # evt. eingestelltes Staticdir-Tool die Datei ausliefern kann
        ext = os.path.splitext(script_filename)
        if ext[1] not in handlers:
            return




#        # TEST ---------
#        cherrypy.serving.response.body = [show_request()]
#        cherrypy.serving.request.handler = None
#        return
#        # TEST ----------








        # prepare body
        if request.method in request.methods_with_bodies:
            body_file = request.rfile
            content_length = headers.get("content-length", 0)
        else:
            body_file = StringIO()
            content_length = None

        # prepare environment for CGI callable
        # There I got infos about the environment variables:
        # http://de.selfhtml.org/servercgi/cgi/umgebungsvariablen.htm
        # http://tools.ietf.org/html/rfc3875#page-12

        env = {
            # REMOTE_ADDR
            # Enthält die IP-Adresse des Server-Rechners, über den das CGI-Script
            # aufgerufen wurde. Es muss sich hierbei nicht unbedingt um die
            # IP-Adresse des aufrufenden Client-Rechners handeln - der Wert kann
            # beispielsweise auch von einem Proxy-Server stammen.
            "REMOTE_ADDR": headers.get("remote-addr", "127.0.0.1")
        }

        # CONTENT_LENGTH
        # Enthält die Anzahl der Zeichen, die beim Aufruf des CGI-Scripts
        # über die POST-Methode übergeben wurden. Wenn das CGI-Script
        # beispielsweise beim Absenden eines HTML-Formulars aufgerufen
        # wurde und dort als Übertragungsmethode POST angegeben ist,
        # steht in dieser Umgebungsvariablen, wie viele Zeichen das Script
        # von der Standardeingabe lesen muss, um die übermittelten
        # Formulardaten vollständig einzulesen.
        if not content_length is None:
            env["CONTENT_LENGTH"] = str(content_length)

        # CONTENT_TYPE
        # Enthält beim Aufruf über die POST-Methode den Seite MIME-Typ
        # der übergebenen Daten. Wenn das CGI-Script beispielsweise beim
        # Absenden eines HTML-Formulars aufgerufen wurde und dort als
        # Übertragungsmethode POST angegeben ist, steht in dieser
        # Umgebungsvariablen der für HTML-Formulare typische MIME-Typ
        # application/x-www-form-urlencoded (zu diesem MIME-Typ siehe auch
        # Seite Datenstrom bei Übertragung von Formulardaten).
        if "content-type" in headers:
            env["CONTENT_TYPE"] = headers["CONTENT_TYPE"]

        # DOCUMENT_ROOT
        # Enthält den physischen Pfad des Wurzelverzeichnisses für die Ablage
        # von Dateien, die im Webserver aufrufbar sind. Ein CGI-Script kann aus
        # dieser Angabe beispielsweise absolute Pfadnamen zum Öffnen von Dateien
        # errechnen.
        env["DOCUMENT_ROOT"] = dir

        # GATEWAY_INTERFACE
        # Enthält die Version der CGI-Schnittstelle, die von dem installierten
        # Server unterstützt wird, z.B. CGI/1.1, wenn die gegenwärtig übliche
        # Version 1.1 der Schnittstellendefinition unterstützt wird.
        env["GATEWAY_INTERFACE"] = "CGI/1.1"

        # HTTP_ACCEPT
        # Enthält die Liste der MIME-Typen, die der aufrufende Web-Browser
        # akzeptiert. Die Angabe */* bedeutet: der Web-Browser akzeptiert alles.
        if "accept" in headers:
            env["HTTP_ACCEPT"] = headers["accept"]
        elif hasattr(request, "wsgi_environ"):
            if "HTTP_ACCEPT" in request.wsgi_environ:
                env["HTTP_ACCEPT"] = request.wsgi_environ["HTTP_ACCEPT"]

        # HTTP_ACCEPT_CHARSET
        # Enthält die Liste der Zeichenkodierungen, die der aufrufende Web-Browser
        # akzeptiert, beispielsweise iso-8859-1, utf-8, utf-16, *;q=0.1.
        if "accept-charset" in headers:
            env["HTTP_ACCEPT_CHARSET"] = headers["accept-charset"]

        # HTTP_ACCEPT_ENCODING
        # Enthält eine Liste der Kodierungsmethoden, die der aufrufende Browser
        # akzeptiert. Manche Browser akzeptieren beispielsweise auch den
        # Kodierungstyp gzip, was bedeutet, dass der Browser auch Dateien
        # empfangen kann, die nach dem GNU-Zip-Algorithmus komprimiert an ihn
        # übertragen werden.
        if "accept-encoding" in headers:
            env["HTTP_ACCEPT_ENCODING"] = headers["accept-encoding"]
        elif hasattr(request, "wsgi_environ"):
            if "HTTP_ACCEPT_ENCODING" in request.wsgi_environ:
                env["HTTP_ACCEPT_ENCODING"] = request.wsgi_environ["HTTP_ACCEPT_ENCODING"]

        # HTTP_ACCEPT_LANGUAGE
        # Enthält, welche Landessprache der aufrufende Browser bei seiner
        # Benutzeroberfläche verwendet. Häufige Werte sind z.B. de (für
        # deutschsprachige Browser) oder en (für englischsprachige Browser).
        # Ein CGI-Script kann aufgrund dieser Angabe beispielsweise entscheiden,
        # ob es eine deutschsprachige oder eine englischsprachige Antwort an
        # den Browser sendet.
        if "accept-language" in headers:
            env["HTTP_ACCEPT_LANGUAGE"] = headers["accept-language"]

        # HTTP_CONNECTION
        # Enthält Informationen über den Status der HTTP-Verbindung zwischen
        # Server und aufrufendem Browser. Der Wert Keep-Alive bedeutet, der
        # Browser wartet auf Antwort.
        if "connection" in headers:
            env["HTTP_CONNECTION"] = headers["connection"]
        elif hasattr(request, "wsgi_environ"):
            if "HTTP_CONNECTION" in request.wsgi_environ:
                env["HTTP_CONNECTION"] = request.wsgi_environ["HTTP_CONNECTION"]

        # HTTP_COOKIE
        # Enthält Namen und Wert von Cookies, sofern solche vom aufrufenden
        # Browser gesendet werden.
        if request.cookie:
            env["HTTP_COOKIE"] = request.cookie

        # HTTP_HOST
        # Enthält den Domain-Namen oder die IP-Adresse aus der Adresszeile des
        # aufrufenden Browsers. Für ein CGI-Script kann diese Angabe wichtig sein,
        # falls es mehrere Server bedienen muss.
        if "host" in headers:
            env["HTTP_HOST"] = headers["host"]
        elif hasattr(request, "wsgi_environ"):
            if "HTTP_HOST" in request.wsgi_environ:
                env["HTTP_HOST"] = request.wsgi_environ["HTTP_HOST"]

        # HTTP_REFERER
        # Enthält den URI der Web-Seite, von der aus das CGI-Script aufgerufen
        # wurde. Der Wert wird jedoch nicht von allen Web-Browsern korrekt
        # übermittelt, ist also nicht in jedem Fall verfügbar.
        if "referer" in headers:
            env["HTTP_REFERER"] = headers["referer"]

        # HTTP_USER_AGENT
        # Enthält Produkt- und Versionsinformationen zum aufrufenden Web-Browser.
        # Ein CGI-Script kann auf diese Weise ermitteln, welchen Browser ein
        # Anwender verwendet.
        if "user-agent" in headers:
            env["HTTP_USER_AGENT"] = headers["user-agent"]

        # PATH_INFO
        # Wird einem CGI-Script eine Zeichenkette mit Daten übergeben,
        # dann enthält PATH_INFO den Teil der Zeichenkette nach dem Namen
        # des Scripts bis zum ersten ?. Wenn das Script beispielsweise die
        # Adresse http://meine.seite.net/cgi-bin/test.pl hat, aber mit
        # http://meine.seite.net/cgi-bin/test.pl/querys/musicbase.sql?cat=Mozart
        # aufgerufen wird, dann enthält diese Umgebungsvariable den Anteil
        # /querys/musicbase.sql. Sie ist dazu gedacht, Dateinamen mit Pfadangabe
        # als Übergabeparameter für Scripts zu ermöglichen.
        env["PATH_INFO"] = path_info

        # path_info: u'/cgi/dateiname.php/arbeitsdir/arbeitsdatei.sql'
        # es sollte "/arbeitsdir/arbeitsdatei.sql" zurück gegeben werden



        # PATH_TRANSLATED
        # Enthält wie PATH_INFO den Anteil des URI nach dem Scriptnamen bis
        # zum ersten ?, jedoch mit dem Unterschied, dass nicht der Anteil
        # selbst aus dem URI zurückgegeben wird, sondern der vom Webserver
        # übersetzte Datenpfad dieses Anteils. Angenommen, das Script hat die
        # Adresse http://meine.seite.net/cgi-bin/test.pl, wurde aber mit
        # http://meine.seite.net/cgi-bin/test.pl/querys/musicbase.sql aufgerufen.
        # Dann könnte der zusätzliche Adressanteil /querys/musicbase.sql aus
        # Sicht des Webservers beispielsweise in einen physischen Pfadnamen wie
        # /usr/web/seite/querys/musicbase.sql aufgelöst werden. Diesen Pfadnamen
        # würde PATH_TRANSLATED zurückgeben.

        # QUERY_STRING
        # Enthält eine Zeichenkette mit Daten, die dem Script im URI nach dem
        # ersten ? übergeben wurden. Angenommen, das Script hat die Adresse
        # http://meine.seite.net/cgi-bin/test.pl, wurde aber mit
        # http://meine.seite.net/cgi-bin/test.pl?User=Stefan aufgerufen.
        # Dann würde QUERY_STRING den Wert User=Stefan enthalten. Wenn ein
        # Anwender ein HTML-Formular ausgefüllt hat, bei dessen Absenden das
        # CGI-Script mit der GET-Methode aufgerufen wurde, dann stehen in
        # dieser Umgebungsvariablen die ausgefüllten Formulardaten. Die Daten
        # sind nach den Regeln des MIME-Typs application/x-www-form-urlencoded
        # kodiert.

        # REMOTE_HOST
        # Enthält den Hostnamen des Rechners, über den das CGI-Script aufgerufen
        # wurde. Dieser Wert wird jedoch nur gesetzt, wenn der Webserver
        # entsprechend konfiguriert und dazu in der Lage ist, der IP-Adresse
        # den entsprechenden Hostnamen zuzuordnen. Es muss sich hierbei nicht
        # unbedingt um die IP-Adresse des aufrufenden Client-Rechners handeln -
        # der Wert kann beispielsweise auch von einem Proxy-Server stammen.

        # REMOTE_IDENT
        # Enthält Protokollinformationen, wenn auf dem Server das Protokoll
        # ident für geschützte Zugriffe läuft.

        # REMOTE_PORT
        # Ermittelt, über welchen Port des Client-Rechners das CGI-Script
        # aufgerufen wurde. Diese Zahl liegt gewöhnlich im Bereich ab 1024
        # aufwärts und wird vom aufrufenden Web-Browser zufällig ausgewählt.

        # REMOTE_USER
        # Enthält den Benutzernamen, mit dem sich der aufrufende Benutzer
        # angemeldet hat, um das CGI-Script ausführen zu lassen. Wenn das
        # Script beispielsweise htaccess-geschützt ist, muss sich der
        # aufrufende Benutzer mit Benutzernamen und Passwort anmelden. Der
        # dabei eingegebene Benutzername kann mit dieser Variable ermittelt
        # werden.

        # REQUEST_METHOD
        # Enthält die HTTP-Anfragemethode, mit der das CGI-Programm aufgerufen
        # wurde. Beispielsweise GET oder POST. Ein CGI-Script kann diese
        # Variable auslesen und danach entscheiden, wie es Formulardaten
        # einlesen kann: entweder von der Standardeingabe (bei Methode POST)
        # oder aus der Umgebungsvariablen QUERY_STRING (bei Methode GET).
        if hasattr(request, "method"):
            env["REQUEST_METHOD"] = request.method

        # REQUEST_URI
        # Enthält den HTTP-Pfad des Scripts inklusive der im Aufruf übergebenen
        # Daten. Angenommen, das Script hat die Adresse
        # http://meine.seite.net/cgi-bin/test.pl und wurde mit
        # http://meine.seite.net/cgi-bin/test.pl?User=Stefan aufgerufen.
        # Dann liefert REQUEST_URI den Wert /cgi-bin/test.pl?User=Stefan.

        # SCRIPT_FILENAME
        # Enthält den physischen Pfad des Scripts auf dem Server-Rechner,
        # also z.B. /usr/web/data/cgi-bin/test.pl.
        env["SCRIPT_FILENAME"] = script_filename

        # SCRIPT_NAME
        # Enthält den HTTP-Pfad des Scripts. Angenommen, das Script hat die
        # Adresse http://meine.seite.net/cgi-bin/test.pl. Dann liefert
        # SCRIPT_NAME den Wert /cgi-bin/test.pl.
        env["SCRIPT_NAME"] = script_name

        # SERVER_ADDR
        # Enthält die IP-Adresse des Server-Rechners.

        # SERVER_ADMIN
        # Enthält Namen/E-Mail-Adresse des in der Webserver-Konfiguration
        # eingetragenen Server-Administrators.

        # SERVER_NAME
        # Enthält den Namen des Server-Rechners, auf dem das CGI-Script läuft.
        # Normalerweise ist dies der eingetragene Hostname des Rechners.

        # SERVER_PORT
        # Enthält die Portnummer, die für den Webserver eingerichtet wurde.
        # Normalerweise ist dies für Webserver die Nummer 80.

        # SERVER_PROTOCOL
        # Enthält die Version des HTTP-Protokolls, das der installierte
        # Webserver unterstützt, z.B. HTTP/1.1, wenn die gegenwärtig übliche
        # Version 1.1 des HTTP-Protokolls unterstützt wird.
        if hasattr(request, "server_protocol"):
            env["SERVER_PROTOCOL"] = request.server_protocol

        # SERVER_SIGNATURE
        # Enthält eine erweiterte Selbstauskunft des Servers,
        # z.B. Apache/1.3.31 Server at localhost Port 80.

        # SERVER_SOFTWARE  (Nicht mit PHP)
        # Enthält den Namen und die Versionsnummer der Webserver-Software auf
        # dem Server-Rechner.
        #
        if hasattr(request, "wsgi_environ"):
            if "SERVER_SOFTWARE" in request.wsgi_environ:
                env["SERVER_SOFTWARE"] = request.wsgi_environ["SERVER_SOFTWARE"]
                env["REDIRECT_STATUS"] = "200"



        # ToDo: Wenn Dateiendung bekannt, dann bekannten Interpreter mit Datei als Parameter aufrufen
        # cgi_handlers {"php": "php-cgi", "py": "python"}



        print
        print os.path.join(PHPDIR, "phpinfo.php")
        print

        # call PHP interpreter
        cmd_args = ["/usr/bin/php5-cgi", os.path.join(PHPDIR, "phpinfo.php"), "--"]
        proc = subprocess.Popen(
            cmd_args,
            executable = "/usr/bin/php5-cgi",
            stdin = subprocess.PIPE,
            stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT,
            cwd = PHPDIR,
            env = env
        )
        proc.stdin.write(body_file.read())

        # get headers
        cherrypy.serving.response.headers = wsgiserver2.read_headers(
            proc.stdout, cherrypy.serving.response.headers
        )

        # get body
        cherrypy.serving.response.body = proc.stdout

        # finished: no more request handler needed
        cherrypy.serving.request.handler = None

cherrypy.tools.cgiserver = CgiServer()


class Root(object):


    def index(self, *args, **kwargs):

        return """
        <html>
        <body>
            {request}
        </body>
        </html>
        """.format(request = show_request())

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
    })

    config = {
        "/": {
            "tools.staticdir.root": THISDIR,
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "",
            # CgiServer
            #"tools.cgiserver.root": THISDIR
        },
        "/cgi": {
            # CgiServer
            "tools.cgiserver.on": True,
            "tools.cgiserver.base_url": "/cgi",
            "tools.cgiserver.dir": os.path.join(THISDIR, "php_files"),
            "tools.cgiserver.handlers": {
                ".php": "/usr/bin/php-cgi",
                ".py": "/usr/bin/python",
            },
        }
    }
    app = cherrypy.Application(Root(), config = config)

    cherrypy.quickstart(app)


if __name__ == "__main__":
    main()

