# -*- coding: utf-8 -*-
from tempfile import NamedTemporaryFile
import tempfile


class TempFileF:
    def __init__(self):
        pass

    def do(self):
        file = NamedTemporaryFile()
        print file.name
        file.close()

# main

file = TempFileF()
file.do()
print tempfile.gettempdir()