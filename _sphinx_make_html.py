#!/usr/bin/env python

import os
import subprocess

THISDIR = os.path.dirname(os.path.abspath(__file__))
DOCDIR = os.path.join(THISDIR, "documentation")

args = ["make", "html"]
returncode = subprocess.call(args, cwd = DOCDIR)
if returncode != 0:
    raw_input("Press ENTER to continue...")
