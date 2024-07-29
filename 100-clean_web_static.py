#!/usr/bin/python3
"""This script that deletes out-of-date archives
"""
from fabric.api import *
import os
env.hosts = ['54.157.167.250', '18.234.105.180']


def do_clean(number=0):
    """Deletes out-of-date archives
    """
    number = int(number)
    if number == 0 or number == 1:
        number = 1
    else:
        number += 1
    with lcd('versions'):
        local('ls -t | tail -n +{} | xargs rm -rf'.format(number))
    with cd('/data/web_static/releases'):
        run('ls -t | tail -n +{} | xargs rm -rf'.format(number))
