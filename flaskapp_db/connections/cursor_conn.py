import pymysql

def cursor_conn(host, user, password):
    conn = pymysql.connect(host=host,
                           user=user,
                           password=password,
                           cursorclass=pymysql.cursors.DictCursor,
                           charset='utf8')

    cursor = conn.cursor()
    conn.autocommit(True)
    return cursor, conn