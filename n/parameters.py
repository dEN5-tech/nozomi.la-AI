import os

DEBUG = False
START_EPOCH = 0

EXPLORE_PROB = .2
POOL_SIZE = int(os.environ.get('POOL_SIZE', None))
VIEW_RATIO = .2
ATTITUDE_TOWARDS_NOVEL_TAGS = 1

JOB_POOL_SIZE = int(os.environ.get('JOB_POOL_SIZE', None))
JSON_MAX = int(os.environ.get('JSON_MAX', None))
PORT = int(os.environ.get('PORT', None))

FILTER = os.environ.get('FILTER', None)

# Below are default values. 
# DEBUG = False
# START_EPOCH = 0

# EXPLORE_PROB = .2
# POOL_SIZE = 64
# VIEW_RATIO = .2
# ATTITUDE_TOWARDS_NOVEL_TAGS = 1

# JOB_POOL_SIZE = 8
# JSON_MAX = 16
# PORT = 2348

# FILTER = ''
