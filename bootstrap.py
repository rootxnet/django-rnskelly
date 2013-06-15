#!/usr/bin/env python

"""
    Author: Michal Lech <rootx@rootxnet.com>
    Website: http://rootxnet.com/    
"""

import os, shutil, getpass, random
from distutils.sysconfig import get_python_lib

ROOT_DIR = os.getcwd()
PROJECT_NAME = os.path.basename(ROOT_DIR)
REPLACEMENTS = [
    ("#PROJECT_NAME#", PROJECT_NAME),
    ("#PROJECT_ROOT#", ROOT_DIR),
    ("#DOMAIN_NAME#", raw_input("Domain name [example.com]: ") or "example.com"),
    ("#ENV_USER#", raw_input("WSGI User [%s]: " % getpass.getuser()) or getpass.getuser()),
    ("#PYTHON_PATH#", raw_input("Python site-packages dir [%s]: " % get_python_lib()) or get_python_lib()),
    ("#SECRET_KEY#", ''.join([random.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])),
]
FORBIDDEN_FILES = []
INTERNAL_PROJECT_DIR = os.path.join(ROOT_DIR, "PROJECT_NAME")

# build tree ignoring hidden dirs
tree = filter(lambda y: not y[0].startswith("."), os.walk(ROOT_DIR))

# scan all files and replace keywords
for root, subFolders, filenames in tree:
    for filename in filenames:
        fullpath = os.path.join(root, filename)
        # Ignore current and forbidden files
        if fullpath == os.path.abspath(__file__) or filename in FORBIDDEN_FILES:
            continue

        with open(fullpath, "r") as fl:
            orig_data = new_data = fl.read()
            for replacement in REPLACEMENTS:
                new_data = new_data.replace(replacement[0], replacement[1])

        if new_data is not orig_data:
            print "Changed: " + os.path.join(root, filename), filename
            with open(os.path.join(root, filename), "w") as fl:
                fl.write(new_data)

# rename internal project stuff to proper names
if os.path.isdir(INTERNAL_PROJECT_DIR):
    try:
        shutil.move(INTERNAL_PROJECT_DIR, os.path.join(ROOT_DIR, PROJECT_NAME))
    except shutil.Error, e:
        print "Error occured while moving %s to %s: %s" % ( e.srcname, e.dstname, e.exception )
