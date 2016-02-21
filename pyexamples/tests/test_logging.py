__author__ = 'Fred'

import logging
# OUTPUT: '[D]:...'
logging.basicConfig(filename='logging.log', level=logging.DEBUG, format='[%(levelname).1s]:%(message)s')
# logging.
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')
