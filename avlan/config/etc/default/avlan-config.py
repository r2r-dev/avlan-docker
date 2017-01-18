#from avlan.settings.dev import *

import os
environ = os.environ

admin_user = "admin",
admin_password = "password"

db_host = "mysql.internal"
db_port = 3306
db_username = "avlan"
db_password = "avlan"
db_database = "avlan"

redis_host = "redis.internal"
redis_port = 6379
redis_db = 0

translation_dir = "src/translations/"
