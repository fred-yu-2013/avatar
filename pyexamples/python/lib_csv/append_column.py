# -*- coding: utf-8 -*-

import csv

data = [86, 87, 88, 89]

with open('in.txt') as fin, open('out.txt', 'w') as fout:
        index = 0
        for line in iter(fin.readline, ''):
            fout.write(line.replace('\n', ', ' + str(data[index]) + '\n'))
            index += 1

