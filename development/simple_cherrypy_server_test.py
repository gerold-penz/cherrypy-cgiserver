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

#    CONTENT_LENGTH 	Enthält die Anzahl der Zeichen, die beim Aufruf des CGI-Scripts über die POST-Methode übergeben wurden. Wenn das CGI-Script beispielsweise beim Absenden eines HTML-Formulars aufgerufen wurde und dort als Übertragungsmethode POST angegeben ist, steht in dieser Umgebungsvariablen, wie viele Zeichen das Script von der Standardeingabe lesen muss, um die übermittelten Formulardaten vollständig einzulesen.
#    CONTENT_TYPE 	Enthält beim Aufruf über die POST-Methode den Seite MIME-Typ der übergebenen Daten. Wenn das CGI-Script beispielsweise beim Absenden eines HTML-Formulars aufgerufen wurde und dort als Übertragungsmethode POST angegeben ist, steht in dieser Umgebungsvariablen der für HTML-Formulare typische MIME-Typ application/x-www-form-urlencoded (zu diesem MIME-Typ siehe auch Seite Datenstrom bei Übertragung von Formulardaten).
#    DOCUMENT_ROOT 	Enthält den physischen Pfad des Wurzelverzeichnisses für die Ablage von Dateien, die im Webserver aufrufbar sind. Ein CGI-Script kann aus dieser Angabe beispielsweise absolute Pfadnamen zum Öffnen von Dateien errechnen.
#    GATEWAY_INTERFACE 	Enthält die Version der CGI-Schnittstelle, die von dem installierten Server unterstützt wird, z.B. CGI/1.1, wenn die gegenwärtig übliche Version 1.1 der Schnittstellendefinition unterstützt wird.
#    HTTP_ACCEPT 	Enthält die Liste der MIME-Typen, die der aufrufende Web-Browser akzeptiert. Die Angabe */* bedeutet: der Web-Browser akzeptiert alles.
#    HTTP_ACCEPT_CHARSET 	Enthält die Liste der Zeichenkodierungen, die der aufrufende Web-Browser akzeptiert, beispielsweise iso-8859-1, utf-8, utf-16, *;q=0.1.
#    HTTP_ACCEPT_ENCODING 	Enthält eine Liste der Kodierungsmethoden, die der aufrufende Browser akzeptiert. Manche Browser akzeptieren beispielsweise auch den Kodierungstyp gzip, was bedeutet, dass der Browser auch Dateien empfangen kann, die nach dem GNU-Zip-Algorithmus komprimiert an ihn übertragen werden.
#    HTTP_ACCEPT_LANGUAGE 	Enthält, welche Landessprache der aufrufende Browser bei seiner Benutzeroberfläche verwendet. Häufige Werte sind z.B. de (für deutschsprachige Browser) oder en (für englischsprachige Browser). Ein CGI-Script kann aufgrund dieser Angabe beispielsweise entscheiden, ob es eine deutschsprachige oder eine englischsprachige Antwort an den Browser sendet.
#    HTTP_CONNECTION 	Enthält Informationen über den Status der HTTP-Verbindung zwischen Server und aufrufendem Browser. Der Wert Keep-Alive bedeutet, der Browser wartet auf Antwort.
#    HTTP_COOKIE 	Enthält Namen und Wert von Cookies, sofern solche vom aufrufenden Browser gesendet werden. Mit der Perl-Anweisung:
#    my @cookies = split(/[;,]\s*/,$ENV{'HTTP_COOKIE'});
#    können Sie alle gesetzten Cookies ermitteln. Jedes Element des Seite Arrays namens @cookies enthält dann jeweils einen Cookie, bestehend aus einem Namen und einem Wert, die durch ein Gleichheitszeichen = getrennt sind. Der Wert eines Cookies ist im Format des Seite MIME-Typs application/x-www-form-urlencoded gespeichert (zu diesem MIME-Typ siehe auch Seite Datenstrom bei Übertragung von Formulardaten).
#    HTTP_HOST 	Enthält den Domain-Namen oder die IP-Adresse aus der Adresszeile des aufrufenden Browsers. Für ein CGI-Script kann diese Angabe wichtig sein, falls es mehrere Server bedienen muss.
#    HTTP_REFERER 	Enthält den URI der Web-Seite, von der aus das CGI-Script aufgerufen wurde. Der Wert wird jedoch nicht von allen Web-Browsern korrekt übermittelt, ist also nicht in jedem Fall verfügbar.
#    Anmerkung: Wenn Ihnen die englische Sprache geläufig ist, werden Sie feststellen, dass HTTP_REFERER eigentlich HTTP_REFERRER heißen müsste. Den Autoren der ersten Spezifikation von HTTP ist dieser Fehler unterlaufen, der sich aus historischen Gründen und aufgrund der Abwärtskompatibilität von HTTP bis heute hält.
#    HTTP_USER_AGENT 	Enthält Produkt- und Versionsinformationen zum aufrufenden Web-Browser. Ein CGI-Script kann auf diese Weise ermitteln, welchen Browser ein Anwender verwendet.
#    PATH_INFO 	Wird einem CGI-Script eine Zeichenkette mit Daten übergeben, dann enthält PATH_INFO den Teil der Zeichenkette nach dem Namen des Scripts bis zum ersten ?. Wenn das Script beispielsweise die Adresse http://meine.seite.net/cgi-bin/test.pl hat, aber mit http://meine.seite.net/cgi-bin/test.pl/querys/musicbase.sql?cat=Mozart aufgerufen wird, dann enthält diese Umgebungsvariable den Anteil /querys/musicbase.sql. Sie ist dazu gedacht, Dateinamen mit Pfadangabe als Übergabeparameter für Scripts zu ermöglichen.
#    PATH_TRANSLATED 	Enthält wie PATH_INFO den Anteil des URI nach dem Scriptnamen bis zum ersten ?, jedoch mit dem Unterschied, dass nicht der Anteil selbst aus dem URI zurückgegeben wird, sondern der vom Webserver übersetzte Datenpfad dieses Anteils. Angenommen, das Script hat die Adresse http://meine.seite.net/cgi-bin/test.pl, wurde aber mit http://meine.seite.net/cgi-bin/test.pl/querys/musicbase.sql aufgerufen. Dann könnte der zusätzliche Adressanteil /querys/musicbase.sql aus Sicht des Webservers beispielsweise in einen physischen Pfadnamen wie /usr/web/seite/querys/musicbase.sql aufgelöst werden. Diesen Pfadnamen würde PATH_TRANSLATED zurückgeben.
#    QUERY_STRING 	Enthält eine Zeichenkette mit Daten, die dem Script im URI nach dem ersten ? übergeben wurden. Angenommen, das Script hat die Adresse http://meine.seite.net/cgi-bin/test.pl, wurde aber mit http://meine.seite.net/cgi-bin/test.pl?User=Stefan aufgerufen. Dann würde QUERY_STRING den Wert User=Stefan enthalten. Wenn ein Anwender ein HTML-Formular ausgefüllt hat, bei dessen Absenden das CGI-Script mit der GET-Methode aufgerufen wurde, dann stehen in dieser Umgebungsvariablen die ausgefüllten Formulardaten. Die Daten sind nach den Regeln des MIME-Typs application/x-www-form-urlencoded kodiert.
#    REMOTE_ADDR 	Enthält die IP-Adresse des Server-Rechners, über den das CGI-Script aufgerufen wurde. Es muss sich hierbei nicht unbedingt um die IP-Adresse des aufrufenden Client-Rechners handeln - der Wert kann beispielsweise auch von einem Proxy-Server stammen.
#    REMOTE_HOST 	Enthält den Hostnamen des Rechners, über den das CGI-Script aufgerufen wurde. Dieser Wert wird jedoch nur gesetzt, wenn der Webserver entsprechend konfiguriert und dazu in der Lage ist, der IP-Adresse den entsprechenden Hostnamen zuzuordnen. Es muss sich hierbei nicht unbedingt um die IP-Adresse des aufrufenden Client-Rechners handeln - der Wert kann beispielsweise auch von einem Proxy-Server stammen.
#    REMOTE_IDENT 	Enthält Protokollinformationen, wenn auf dem Server das Protokoll ident für geschützte Zugriffe läuft.
#    REMOTE_PORT 	Ermittelt, über welchen Port des Client-Rechners das CGI-Script aufgerufen wurde. Diese Zahl liegt gewöhnlich im Bereich ab 1024 aufwärts und wird vom aufrufenden Web-Browser zufällig ausgewählt.
#    REMOTE_USER 	Enthält den Benutzernamen, mit dem sich der aufrufende Benutzer angemeldet hat, um das CGI-Script ausführen zu lassen. Wenn das Script beispielsweise htaccess-geschützt ist, muss sich der aufrufende Benutzer mit Benutzernamen und Passwort anmelden. Der dabei eingegebene Benutzername kann mit dieser Variable ermittelt werden.
#    REQUEST_METHOD 	Enthält die HTTP-Anfragemethode, mit der das CGI-Programm aufgerufen wurde. Beispielsweise GET oder POST. Ein CGI-Script kann diese Variable auslesen und danach entscheiden, wie es Formulardaten einlesen kann: entweder von der Standardeingabe (bei Methode POST) oder aus der Umgebungsvariablen QUERY_STRING (bei Methode GET).
#    REQUEST_URI 	Enthält den HTTP-Pfad des Scripts inklusive der im Aufruf übergebenen Daten. Angenommen, das Script hat die Adresse http://meine.seite.net/cgi-bin/test.pl und wurde mit http://meine.seite.net/cgi-bin/test.pl?User=Stefan aufgerufen. Dann liefert REQUEST_URI den Wert /cgi-bin/test.pl?User=Stefan.
#    SCRIPT_FILENAME 	Enthält den physischen Pfad des Scripts auf dem Server-Rechner, also z.B. /usr/web/data/cgi-bin/test.pl.
#    SCRIPT_NAME 	Enthält den HTTP-Pfad des Scripts. Angenommen, das Script hat die Adresse http://meine.seite.net/cgi-bin/test.pl. Dann liefert SCRIPT_NAME den Wert /cgi-bin/test.pl.
#    SERVER_ADDR 	Enthält die IP-Adresse des Server-Rechners.
#    SERVER_ADMIN 	Enthält Namen/E-Mail-Adresse des in der Webserver-Konfiguration eingetragenen Server-Administrators.
#    SERVER_NAME 	Enthält den Namen des Server-Rechners, auf dem das CGI-Script läuft. Normalerweise ist dies der eingetragene Hostname des Rechners.
#    SERVER_PORT 	Enthält die Portnummer, die für den Webserver eingerichtet wurde. Normalerweise ist dies für Webserver die Nummer 80.
#    SERVER_PROTOCOL 	Enthält die Version des HTTP-Protokolls, das der installierte Webserver unterstützt, z.B. HTTP/1.1, wenn die gegenwärtig übliche Version 1.1 des HTTP-Protokolls unterstützt wird.
#    SERVER_SIGNATURE 	Enthält eine erweiterte Selbstauskunft des Servers, z.B. Apache/1.3.31 Server at localhost Port 80.
#    SERVER_SOFTWARE 	Enthält den Namen und die Versionsnummer der Webserver-Software auf dem Server-Rechner.


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

