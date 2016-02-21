# -*- coding: utf-8 -*-

import re


def parse_line(line):
    """ line -> (int, int, int), None if invalid
    """
    if not line.startswith('Xac:'):
        return None
    parts = re.split('[,Xac:YZ#?*]', line)
    parts = filter(lambda x: bool(x), parts)
    parts = map(lambda x: float(x), parts)
    return tuple(parts)

output = []
with open('input.txt') as f:
    for line in iter(f.readline, ''):
        axes = parse_line(line.strip())
        if axes:
            output.append(axes)
print output
