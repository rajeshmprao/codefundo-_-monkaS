import pymysql
from flaskapp_db.connections import cursor_conn

def setup():
    c, conn = cursor_conn()
    c.execute("CREATE DATABASE IF NOT EXISTS FLASKAPP")