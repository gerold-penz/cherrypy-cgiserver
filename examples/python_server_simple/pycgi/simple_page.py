#!/usr/bin/env python
# coding: utf-8
"""
Simple Python-CGI-Page
"""

import cgitb; cgitb.enable()

html = """Content-type: text/html\r
\r
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Simple HTML-Page</title>
  <style type="text/css">
    body {
      font-family: sans-serif;
    }
  </style>
</head>
<body>
  <h1>Simple Python-CGI-Page</h1>
  <p>Powered by CherryPy</p>

  %(dynamic_content)s

</body>
</html>
"""

dynamic_content = "<p>This is dynamic content.</p>\n" * 3

print html % {"dynamic_content": dynamic_content}
