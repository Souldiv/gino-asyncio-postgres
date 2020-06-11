import os

# database config
db_host = ''
db_port = ''
db_user = ''
db_password = ''
db_name = ''

DB_ARGS = dict(
    host=os.getenv('DB_HOST', db_host),
    port=os.getenv('DB_PORT', db_port),
    user=os.getenv('DB_USER', db_user),
    password=os.getenv('DB_PASS', db_password),
    database=os.getenv('DB_NAME', db_name),
)

