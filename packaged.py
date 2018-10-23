from flaskapp_db.connections import cursor_conn
user = 'root'
password = 'bakra123'
host = '127.0.0.1'

cursor, conn = cursor_conn(host, user, password)

cursor.execute('SHOW DATABASES')
result = cursor.fetchall()
print(result)
