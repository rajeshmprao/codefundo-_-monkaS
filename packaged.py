from flaskapp_db.connections import cursor_conn
import os
host = '127.0.0.1'
user = os.environ["user"]
password = os.environ["pass"]

cursor, conn = cursor_conn(host, user, password)

cursor.execute('SHOW DATABASES')
result = cursor.fetchall()
print(result)
