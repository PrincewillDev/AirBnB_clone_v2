#!/usr/bin/python3

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['54.157.167.250', '18.234.105.180']


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
