# -*- coding: utf-8 -*-

import subprocess
import time
import os

def foo1():
    p = subprocess.Popen(['python.exe', 'foo1.py'],
                         stdin=subprocess.PIPE)
    p.stdin.write('A\n')
    p.stdin.write('A\n')
    time.sleep(2)

SERVER_NAME="server"
CLIENT_NAME="client"
EASY_RSA=os.getcwd()
KEY_CONFIG=EASY_RSA+"/openssl.cnf"
KEY_DIR=EASY_RSA+"/keys"

def shell_source(script):
    """Sometime you want to emulate the action of "source" in bash,
    settings some environment variables. Here is a way to do it."""
    import subprocess, os
    pipe = subprocess.Popen(". %s; env" % script, stdout=subprocess.PIPE, shell=True)
    output = pipe.communicate()[0]
    env = dict((line.split("=", 1) for line in output.splitlines()))
    os.environ.update(env)

def source_env():
    shell_source(EASY_RSA+'/vars')


def foo2():
    source_env()
    cmd = 'openssl req -days 3650 -nodes -new -newkey rsa:1024 -sha1 -x509 -keyout ca.key -out ca.crt -config openssl.cnf'
    p = subprocess.Popen(cmd.split(),
                         stdin=subprocess.PIPE)
    p.stdin.write('A\n')
    p.stdin.write('A\n')
    time.sleep(2)

foo2()

