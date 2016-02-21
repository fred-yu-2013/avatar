__author__ = 'Fred'

# This file shows how to list files in a specified dir.
# and sort the file
# and output to a log file.

import os
from os.path import join
import sys
import operator


class File:
    def __init__(self, path):
        # print 'File.__init__', path
        self.path = path
        fstat = os.stat(path)
        self.size = fstat.st_size
        self.inode = fstat.st_ino

def main():
    log_file = open("log.txt", 'w')
    all_files = []
    # for root, dirs, files in os.walk(r'C:\MyWorkspace\pycharm\pyexamples'):
    for root, dirs, files in os.walk(r'C:\Users\Fred\Downloads'):
        print root, dirs, files
        for fname in files:
            # print "for", join(root, fname)
            # print fname
            if fname is not None and len(str(fname)) > 0:
                path = join(root, fname)
                f = File(path)
                all_files.append(f)
    print ">>>> get files"
    log_file.write(">>>> get files.\n")
    for f in all_files:
        print f.path
        log_file.write(f.path + '\n')
    all_files_size = sorted(all_files, key=operator.attrgetter('size'), reverse=True)
    print ">>>> sorted by file size."
    log_file.write(">>>> sorted by file size.\n")
    for f in all_files_size:
        print f.path
        log_file.write(f.path + '\n')
    log_file.close()


def get_all_file_paths(parent_dir):
    """ Get all file paths in parent dir.
    """
    paths = []
    for root, _, files in os.walk(parent_dir):
        for name in files:
            paths.append(os.path.join(root, name))
    print paths
    return paths


def get_all_files(parent):
    paths = []
    for root, dirs, files in os.walk(parent):
        print root, dirs, files
        break
        # for name in files:
        #     # print files
        #     paths.append(os.path.join(root, name))
    return paths


# main()
# get_all_file_paths(r'C:\Users\Fred\Downloads')
# print get_all_file_paths(r'.')
print get_all_files('.')
