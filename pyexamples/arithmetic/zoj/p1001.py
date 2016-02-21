# A + B Problem.
import sys
for line in sys.stdin:
    a = line.split()
    # print type(line)
    print int(a[0]) + int(a[1])