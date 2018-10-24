import pymysql
import os
host = '127.0.0.1'
user = os.environ['user']
password = os.environ['pass']
def cursor_conn():
    conn = pymysql.connect(host=host,
                           user=user,
                           password=password,
                           cursorclass=pymysql.cursors.DictCursor,
                           charset='utf8')

    cursor = conn.cursor()
    conn.autocommit(True)
    return cursor, conn