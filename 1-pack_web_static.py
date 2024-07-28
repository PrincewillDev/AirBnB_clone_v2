#!/usr/bin/python3
"""
This module contains a Fabric function that generates a .tgz archive from
the contents of the web_static folder.
"""
from fabric.api import local
#from datetime import datetime

def do_pack():
    local('sudo mkdir -p versions')
 #   datetime = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
#    local(f"tar -cvzf versions/web_static_{datetime}.tgz web_static")
