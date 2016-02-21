# -*- coding: utf-8 -*-

import subprocess

p = subprocess.Popen(['python.exe', 'foo.py'],
                     stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)
for line in iter(p.stdout.readline, ''):
    print("OUTPUT: " + line.rstrip())
