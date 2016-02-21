import base64
import sys
if len(sys.argv) < 3:
    print 'Generate base64 for username and password.'
    print 'Usage: base64_encode.py [user] [password]'
    quit()
print base64.b64encode(sys.argv[1] + ':' + sys.argv[2])
