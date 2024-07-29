#!/usr/bin/python3
"""
This script that creates and distributes an archive to web server
"""
from fabric.api import local, env, put, run
from datetime import datetime
from os.path import exists, isdir
env.hosts = ['54.157.167.250', '18.234.105.180']


def do_pack():
    """Generates a .tgz archive
    """
    if isdir("versions") is False:
        local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = "versions/web_static_{}.tgz".format(date)
    local("tar -cvzf {} web_static".format(file_path))
    if exists(file_path):
        return file_path
    return None


def do_deploy(archive_path):
    """Distributes an archive to your web servers
    """
    if exists(archive_path) is False:
        return False
    try:
        put(archive_path, "/tmp/")
        filename = archive_path.split("/")[-1]
        foldername = filename.split(".")[0]
        run("mkdir -p /data/web_static/releases/{}".format(foldername))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format
            (filename, foldername))
        run("rm /tmp/{}".format(filename))
        run("mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/".format(foldername, foldername))
        run("rm -rf /data/web_static/releases/{}/web_static"
            .format(foldername))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{} /data/web_static/current"
            .format(foldername))
        return True
    except Exception as e:
        return False


def deploy():
    """Creates and distributes an archive to your web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

