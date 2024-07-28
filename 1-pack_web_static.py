#!/usr/bin/python3
"""
This module contains a Fabric function that generates a .tgz archive from
the contents of the web_static folder.
"""
from fabric.api import local
from datetime import datetime
from time import strftime
import os

def do_pack():
    """ A script that generates archive the contents of web_static folder"""

    dt = strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -czvf versions/web_static_{}.tgz web_static/"
              .format(dt))
        print("web_static packed: {} -> {}".format(result, os.stat(result)))
        return "versions/web_static_{}.tgz".format(dt)

    except Exception as e:
        return None
