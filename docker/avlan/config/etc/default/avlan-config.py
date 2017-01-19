#from avlan.settings.dev import *

import os
environ = os.environ

db_host = environ['MYSQL_HOST']
db_port = int(environ['MYSQL_PORT'])
db_username = environ['MYSQL_USER']
db_password = environ['MYSQL_PASSWORD']
db_database = environ['MYSQL_DATABASE']

redis_host = environ['REDIS_HOST']
redis_port = int(environ['REDIS_PORT'])
redis_db = 0

translation_dir = "src/translations/"
