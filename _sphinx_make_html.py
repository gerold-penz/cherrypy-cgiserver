#!/usr/bin/env python

import os
import shutil
import subprocess

THISDIR = os.path.dirname(os.path.abspath(__file__))
DOCDIR = os.path.join(THISDIR, "documentation")
HTMLDIR = os.path.join(DOCDIR, "build", "html")
DESTDIR = os.path.abspath(os.path.join(THISDIR, "..", "cherrypy-cgiserver-gh-pages"))

# Dokumentation erstellen
args = ["make", "html"]
returncode = subprocess.call(args, cwd = DOCDIR)
if returncode != 0:
    raw_input("Press ENTER to continue...")

# Dokumentation HTML kopieren
try:
    for dirpath, dirnames, filenames in os.walk(HTMLDIR):
        for filename in filenames:
            sourcepath = os.path.join(dirpath, filename)
            destdir = os.path.join(DESTDIR, dirpath[len(HTMLDIR) + 1:])
            if not os.path.isdir(destdir):
                os.makedirs(destdir)
            destpath = os.path.join(destdir, filename)
            shutil.copy2(sourcepath, destpath)
except Exception, err:
    print unicode(err)
    raw_input("Press ENTER to continue...")
