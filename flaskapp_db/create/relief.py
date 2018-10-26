import pymysql
from flaskapp_db.connections import cursor_conn
def relief():
    c, conn = cursor_conn()
    c.execute('''CREATE TABLE IF NOT EXISTS FLASKAPP.relief (
                username VARCHAR(55) PRIMARY KEY,
                latitude VARCHAR(55) NOT NULL,
                longitude VARCHAR(55) NOT NULL);
                ''')
    c.close()
    conn.close()
    return

