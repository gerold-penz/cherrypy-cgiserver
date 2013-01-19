#!/usr/bin/env python
#coding: utf-8
"""
Created
    2013-01-19 by Gerold - http://halvar.at/
"""

import cherrypy


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
        except StandardError:
            return unicode(repr(value))
    except StandardError:
        return unicode(repr(value))


def show_request():
    """
    Zeigt die Attribute des CherryPy-Requests als Text an.
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

