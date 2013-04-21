#!/usr/bin/env python
# coding: utf-8
"""
CherryPy CGI-Server Tool
 
Created
    2013-01-05 by Gerold - http://halvar.at/
Requirements
    - CherryPy: http://cherrypy.org/
Licenses
    - http://gerold-penz.github.com/cherrypy-cgiserver/#lizenzen
"""

import os
import cherrypy
import subprocess
import threading
import tempfile
import httplib
import urlparse
import lib.format_
from cStringIO import StringIO
from cherrypy.wsgiserver import wsgiserver2
from cherrypy._cpcompat import unquote

THISDIR = os.path.dirname(os.path.abspath(__file__))


def _determine_script_filename_and_path_info(dir, base_url):
    """
    Hilfsfunktion: Ermittelt *script_filename* und *path_info*

    Info: Greift auf *cherrypy.request.path_info* zu.
    """

    branch = cherrypy.request.path_info[len(base_url) + 1:]
    branch = unquote(branch.lstrip(r"\/"))
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

    return script_filename, path_info


class CgiServer(cherrypy._cptools.Tool):
    """
    CgiServer Tool
    """

    def __init__(self):
        """
        Initialize tool
        """

        cherrypy._cptools.Tool.__init__(
            self,
            point = "on_start_resource",
            callable = self.callable,
            name = "cgiserver",
            priority = 50
        )


    def callable(
        self,
        base_url,
        dir,
        root = "",
        handlers = None,
        server_admin = None,
        response_file_max_size_in_memory = 16000000,
        directory_index = None,
        timeout_seconds = 25
    ):
        """
        Adds an embedded CGI server to CherryPy

        :param base_url: Absolute HTTP-URL of the CGI base directory.
            z.B.: "/cgi"

        :param dir: Absoluter oder relativer Pfad zum Ordner mit den CGI-Dateien.
            Wird der Pfad relativ angegeben, dann wird er an *root* angehängt.
            Gleiches Verhalten wie beim Staticdir-Tool.
            Achtung! Die Eingebaute Python-Funktion *dir* wird hiermit
            überschrieben.

        :param root: An diesen Pfad wird *dir* angehängt, falls *dir* nicht
            absolut übergeben wurde.

        :param handlers: Dictionary mit den Dateiendungen und den
            zugehörigen Interpretern. z.B.::

                {".php": "/usr/bin/php-cgi", ".py": "/usr/bin/python"}

            Es werden nur Dateien ausgeführt, denen ein Handler zugewiesen
            wurde. Wird die Dateiendung nicht im Dictionary gefunden, wird
            das Tool beendet, so dass die Abarbeitung des Requests z.B. von
            Staticdir ausgeliefert werden kann.

        :param server_admin: Enthält Namen/E-Mail-Adresse des
            Server-Administrators. Diese Information wird über die
            Umgebungsvariable SERVER_ADMIN an das CGI-Programm übergeben.

        :param response_file_max_size_in_memory: Gibt an, wieviel Speicher
            die Rückgabe des CGI-Interpreters im Speicher verwenden darf, bevor
            diese in eine temporäre Datei ausgelagert wird. Je mehr Speicher
            desto weniger oft muss auf die Festplatte geschrieben werden.
            Standard: 16 MB

        :param directory_index: Gibt die Datei(en) an, die angezeigt werden
            sollen, wenn statt einer Datei ein Verzeichnis angefordert wurde.
            Wird nichts angegeben, dann wird keine Standard-Datei zurück gegeben.
            Der Name dieses Parameters ist an die Apache-Direktive
            *DirectoryIndex* angelehnt. Wie beim Apachen kann hier ein String
            mit einer oder mehreren durch Leerzeichen getrennten Dateien
            übergeben werden. Auch eine Liste mit Dateinamen ist möglich.
            Siehe: http://httpd.apache.org/docs/2.2/mod/mod_dir.html#directoryindex

        :param timeout_seconds: Gibt in Sekunden an, wie lange auf eine
            Rückmeldung des CGI-Prozesses gewartet werden soll. Ist die Zeit
            abgelaufen, wird der CGI-Prozess terminiert und der HTTP-Fehler
            504-GATEWAY_TIMEOUT zurück geliefert. Der Standard ist 25 Sekunden.
            Das ist etwas weniger als der Standard-Timeout von PHP-CGI.
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
                msg = "CGI-Server requires an absolute dir (or root)."
                cherrypy.log(msg, 'TOOLS.CGISERVER')
                raise ValueError(msg)
            dir = os.path.join(root, dir)

        # Determine where we are in the object tree relative to 'base_url'
        # (copied from *cherrypy.lib.static*)
        if base_url == "":
            base_url = "/"
        base_url = base_url.rstrip(r"\/")

        # Dateiname des Skriptes und angehängten Pfad ermitteln
        script_filename, path_info = \
            _determine_script_filename_and_path_info(dir, base_url)
        if not script_filename:
            # Mit *directory_index* versuchen eine existierende Datei zu ermitteln
            if directory_index and request.path_info.endswith("/"):
                original_path_info = str(request.path_info)
                if isinstance(directory_index, basestring):
                    directory_index = directory_index.split()
                for indexfile_name in directory_index:
                    # Path-Info neu setzen, damit StaticFile zum Ausliefern
                    # verwendet werden kann, falls eine Nicht-CGI-Datei gefunden
                    # wird.
                    request.path_info = original_path_info + indexfile_name
                    script_filename, path_info = \
                        _determine_script_filename_and_path_info(dir, base_url)
                    if script_filename:
                        break
                else:
                    request.path_info = original_path_info
                    return
            else:
                return

        # URL des Skriptes ermitteln
        script_name = base_url + script_filename[len(dir):]

        # There's a chance that the branch pulled from the URL might
        # have ".." or similar uplevel attacks in it. Check that the final
        # filename is a child of dir.
        # (copied from *cherrypy.lib.static*)
        if not os.path.normpath(script_filename).startswith(os.path.normpath(dir)):
            raise cherrypy.HTTPError(httplib.FORBIDDEN)

        # Wenn Dateiendung unbekannt, dann Funktion beenden, damit ein
        # evt. eingestelltes Staticdir-Tool die Datei ausliefern kann
        ext = os.path.splitext(script_filename)[1]
        if ext not in handlers:
            return

        # Interpreter anhand der Dateiendung ermitteln
        handler_executable = handlers[ext]

        # Prüfen ob der Request über HTTPS gekommen ist.
        # Damit kann Pound http://www.apsis.ch/pound das HTTPS-Handling
        # übernehmen und unverschlüsselt an den CGI-Handler weitergeben.
        if "X-Ssl-Cipher" in headers:
            # request.scheme
            request.scheme = "https"

            # wsgi.url_scheme
            request.wsgi_environ["wsgi.url_scheme"] = "https"

            # request.base
            base_url_split = list(urlparse.urlsplit(request.base))
            base_url = urlparse.urlunsplit(
                item for item in ["https"] + base_url_split[1:]
            )
            request.base = str(base_url)




#        # TEST ---------
#        cherrypy.serving.response.body = [lib.format_.show_request()]
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
            # GATEWAY_INTERFACE
            # Enthält die Version der CGI-Schnittstelle, die von dem installierten
            # Server unterstützt wird, z.B. CGI/1.1, wenn die gegenwärtig übliche
            # Version 1.1 der Schnittstellendefinition unterstützt wird.
            "GATEWAY_INTERFACE": "CGI/1.1",

            # SERVER_SIGNATURE
            # Enthält eine erweiterte Selbstauskunft des Servers,
            # z.B. Apache/1.3.31 Server at localhost Port 80.
            "SERVER_SIGNATURE": "CherryPy CgiServer",

            # REMOTE_ADDR
            # Enthält die IP-Adresse des Server-Rechners, über den das CGI-Script
            # aufgerufen wurde. Es muss sich hierbei nicht unbedingt um die
            # IP-Adresse des aufrufenden Client-Rechners handeln - der Wert kann
            # beispielsweise auch von einem Proxy-Server stammen.
            "REMOTE_ADDR": request.remote.ip,

            # REMOTE_PORT
            # Ermittelt, über welchen Port des Client-Rechners das CGI-Script
            # aufgerufen wurde. Diese Zahl liegt gewöhnlich im Bereich ab 1024
            # aufwärts und wird vom aufrufenden Web-Browser zufällig ausgewählt.
            "REMOTE_PORT": str(request.remote.port),

            # SERVER_ADDR
            # Enthält die IP-Adresse des Server-Rechners.
            "SERVER_ADDR": request.local.ip,

            # SERVER_PORT
            # Enthält die Portnummer, die für den Webserver eingerichtet wurde.
            # Normalerweise ist dies für Webserver die Nummer 80.
            "SERVER_PORT": str(request.local.port),

            # DOCUMENT_ROOT
            # Enthält den physischen Pfad des Wurzelverzeichnisses für die Ablage
            # von Dateien, die im Webserver aufrufbar sind. Ein CGI-Script kann aus
            # dieser Angabe beispielsweise absolute Pfadnamen zum Öffnen von Dateien
            # errechnen.
            "DOCUMENT_ROOT": dir,

            # PATH_INFO
            # Wird einem CGI-Script eine Zeichenkette mit Daten übergeben,
            # dann enthält PATH_INFO den Teil der Zeichenkette nach dem Namen
            # des Scripts bis zum ersten ?. Wenn das Script beispielsweise die
            # Adresse http://meine.seite.net/cgi-bin/test.pl hat, aber mit
            # http://meine.seite.net/cgi-bin/test.pl/querys/musicbase.sql?cat=Mozart
            # aufgerufen wird, dann enthält diese Umgebungsvariable den Anteil
            # /querys/musicbase.sql. Sie ist dazu gedacht, Dateinamen mit Pfadangabe
            # als Übergabeparameter für Scripts zu ermöglichen.
            "PATH_INFO": path_info,

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
            "PATH_TRANSLATED": dir.rstrip("/") + path_info if path_info else "",

            # SCRIPT_FILENAME
            # Enthält den physischen Pfad des Scripts auf dem Server-Rechner,
            # also z.B. /usr/web/data/cgi-bin/test.pl.
            "SCRIPT_FILENAME": script_filename,

            # SCRIPT_NAME
            # Enthält den HTTP-Pfad des Scripts. Angenommen, das Script hat die
            # Adresse http://meine.seite.net/cgi-bin/test.pl. Dann liefert
            # SCRIPT_NAME den Wert /cgi-bin/test.pl.
            "SCRIPT_NAME": script_name,
        }

        # REMOTE_HOST
        # Enthält den Hostnamen des Rechners, über den das CGI-Script aufgerufen
        # wurde. Dieser Wert wird jedoch nur gesetzt, wenn der Webserver
        # entsprechend konfiguriert und dazu in der Lage ist, der IP-Adresse
        # den entsprechenden Hostnamen zuzuordnen. Es muss sich hierbei nicht
        # unbedingt um die IP-Adresse des aufrufenden Client-Rechners handeln -
        # der Wert kann beispielsweise auch von einem Proxy-Server stammen.
        if request.remote.name:
            env["REMOTE_HOST"] = request.remote.name

        # SERVER_NAME
        # Enthält den Namen des Server-Rechners, auf dem das CGI-Script läuft.
        # Normalerweise ist dies der eingetragene Hostname des Rechners.
        if request.local.name:
            env["SERVER_NAME"] = request.local.name

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
            env["CONTENT_TYPE"] = headers["content-type"]

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
                env["HTTP_ACCEPT_ENCODING"] = request.wsgi_environ[
                    "HTTP_ACCEPT_ENCODING"
                ]

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
        if "cookie" in request.headers:
            env["HTTP_COOKIE"] = request.headers["cookie"]

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
        if hasattr(request, "query_string"):
            env["QUERY_STRING"] = request.query_string
        elif hasattr(request, "wsgi_environ"):
            if "QUERY_STRING" in request.wsgi_environ:
                env["QUERY_STRING"] = request.wsgi_environ["QUERY_STRING"]

        # REMOTE_IDENT
        # Enthält Protokollinformationen, wenn auf dem Server das Protokoll
        # ident für geschützte Zugriffe läuft.

        # REMOTE_USER
        # Enthält den Benutzernamen, mit dem sich der aufrufende Benutzer
        # angemeldet hat, um das CGI-Script ausführen zu lassen. Wenn das
        # Script beispielsweise htaccess-geschützt ist, muss sich der
        # aufrufende Benutzer mit Benutzernamen und Passwort anmelden. Der
        # dabei eingegebene Benutzername kann mit dieser Variable ermittelt
        # werden.

        # Test it before use it
#        if hasattr(request, "login"):
#            if request.login and not request.login.lower() == "none":
#                env["REMOTE_USER"] = request.login


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
        elif hasattr(request, "wsgi_environ"):
            if "REQUEST_URI" in request.wsgi_environ:
                env["REQUEST_URI"] = request.wsgi_environ["REQUEST_URI"]

        # SERVER_ADMIN
        # Enthält Namen/E-Mail-Adresse des in der Webserver-Konfiguration
        # eingetragenen Server-Administrators.
        if server_admin:
            env["SERVER_ADMIN"] = server_admin

        # SERVER_PROTOCOL
        # Enthält die Version des HTTP-Protokolls, das der installierte
        # Webserver unterstützt, z.B. HTTP/1.1, wenn die gegenwärtig übliche
        # Version 1.1 des HTTP-Protokolls unterstützt wird.
        if hasattr(request, "server_protocol"):
            env["SERVER_PROTOCOL"] = request.server_protocol

        # SERVER_SOFTWARE
        # Enthält den Namen und die Versionsnummer der Webserver-Software auf
        # dem Server-Rechner.
        if hasattr(request, "wsgi_environ"):
            if "SERVER_SOFTWARE" in request.wsgi_environ:
                env["SERVER_SOFTWARE"] = request.wsgi_environ["SERVER_SOFTWARE"]
                env["REDIRECT_STATUS"] = "200"

        # HTTPS
        if request.scheme == "https":
            env["HTTPS"] = "on"
        
        # Alle oben noch nicht übernommenen Einträge aus dem Header an die
        # CGI-Umgebung weiterreichen.
        for header_key, header_value in headers.items():
            if header_key.upper() not in env:
                env[header_key.upper()] = header_value

        # Get response (header and body lines) into spooled temporary file
        response = tempfile.SpooledTemporaryFile(
            max_size = response_file_max_size_in_memory,
            mode = "w+b"
        )

        # call interpreter
        cmd_args = [handler_executable, script_filename]
        proc = subprocess.Popen(
            cmd_args,
            executable = handler_executable,
            stdin = subprocess.PIPE,
            stdout = response,
            stderr = subprocess.STDOUT,
            cwd = dir,
            env = env
        )
        proc.force_terminated = False
        proc.stdin.write(body_file.read())


        def terminate_cgi_process():
            """
            Terminiert nach einem Timeout den CGI-Prozess
            """

            proc.terminate()
            proc.force_terminated = True


        # Timeout-Timer starten, der nach Ablauf den CGI-Prozess terminiert
        timer = threading.Timer(timeout_seconds, terminate_cgi_process)
        timer.start()

        # Los geht's (hier wird gewartet bis das CGI-Programm fertig ist)
        proc.communicate()

        # Timeout-Timer abbrechen, da er hier nicht mehr benötigt wird
        timer.cancel()

        # Falls der Timeout-Timer den CGI-Prozess abbrechen musste, wird der
        # GATEWAY_TIMEOUT-Fehler ausgelöst.
        if proc.force_terminated:
            raise cherrypy.HTTPError(httplib.GATEWAY_TIMEOUT)

        # Get header lines
        response.seek(0)
        try:
            cherrypy.serving.response.headers = wsgiserver2.read_headers(
                response, cherrypy.serving.response.headers
            )
        except ValueError:
            response.seek(0)

        # Redirect if needed
        if "status" in cherrypy.serving.response.headers:
            if "location" in cherrypy.serving.response.headers:
                status_string = cherrypy.serving.response.headers["status"]
                status = None
                if status_string:
                    status = int(status_string[:3])
                if status in [
                    httplib.TEMPORARY_REDIRECT,
                    httplib.MOVED_PERMANENTLY,
                    httplib.FOUND
                ]:
                    location = cherrypy.serving.response.headers["location"]
                    if location:
                        raise cherrypy.HTTPRedirect(location, status)

        # Get body
        cherrypy.serving.response.body = response

        # finished: no more request handler needed
        cherrypy.serving.request.handler = None

cherrypy.tools.cgiserver = CgiServer()


#def get_version_string():
#    """
#    Tries to read the version file
#    """
#
#    for file_path in [
#        os.path.join(THISDIR, "version.txt"),
#        os.path.join(THISDIR, "..", "version.txt")
#    ]:
#        if os.path.isfile(file_path):
#            with open(file_path) as version_file:
#                return version_file.readline().strip()
#
#__version__ = get_version_string()



