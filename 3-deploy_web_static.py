#!/usr/bin/python3

"""This script creates and distributes an archive to web servers.
"""
from fabric.api import local, env, put, run
from datetime import datetime
from os.path import exists, isdir

env.hosts = ['54.157.167.250', '18.234.105.180']

def do_pack():
    """Generates a .tgz archive."""
    if isdir("versions") is False:
        local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = "versions/web_static_{}.tgz".format(date)
    result = local("tar -cvzf {} web_static".format(file_path))
    if result.failed:
        return None
    return file_path

def do_deploy(archive_path):
    """Distributes an archive to web servers."""
    if exists(archive_path) is False:
        return False
    try:
        filename = archive_path.split("/")[-1]
        foldername = filename.split(".")[0]

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Create the directory where the archive will be uncompressed
        run("mkdir -p /data/web_static/releases/{}".format(foldername))

        # Uncompress the archive to the folder
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(filename, foldername))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(filename))

        # Move the contents of the archive to the correct folder
        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(foldername, foldername))

        # Delete the symbolic link if it exists
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link
        run("ln -s /data/web_static/releases/{} /data/web_static/current".format(foldername))

        print("New version deployed!")
        return True
    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False

def deploy():
    """Creates and distributes an archive to web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
