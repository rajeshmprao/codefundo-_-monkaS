from flaskapp_db.connections import cursor_conn

cursor, conn = cursor_conn()

cursor.execute('SHOW DATABASES')
result = cursor.fetchall()
print(result)
