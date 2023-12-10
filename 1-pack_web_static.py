#!/usr/bin/python3
"""
generates a tgz archive from the contents of the web_static folder
"""

from datetime import datetime
from fabric.api import local
from os.path import isdir


def do_pack():
    """
    All archives stored in the folder versions
    (your function should create this folder if it doesn’t exist)
    """
    local("mkdir -p versions")
    status = local("tar -cvzf versions/web_static_{}.tgz web_static"
                   .format(datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")),
                   capture=True)
    if status.failed:
        return None
    print(status)
    return status
