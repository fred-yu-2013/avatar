# __author__ = 'Fred'

import module

# print 'dir() in hello: ', dir()
# print 'dir(module) in hello: ', dir(module)
# print module.__dict__['x']
for k, v in module.__dict__.items():
    print k, v