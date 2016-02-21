# -*- coding: utf-8 -*-

import utils
import sys


def run(script_name, input_file):
    tr = utils.TimeRecorder()
    sys.stdin = iter(open(input_file).readline, '')
    exec 'import %s' % script_name
    tr.record()

# 0.0318075597253 s
# Accepted by c++.
run('p1008_3', 'p1008.in')


