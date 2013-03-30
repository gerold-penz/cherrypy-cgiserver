#!/usr/bin/env python

import os
import sys
import subprocess

THISDIR = os.path.dirname(os.path.abspath(__file__))

# Upload current setup file to Google-Code
args = [sys.executable, "setup.py", "upload", "--src"]
returncode = subprocess.call(args, cwd = THISDIR)
if returncode != 0:
    raw_input("Press ENTER to continue...")
