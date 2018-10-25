import pymysql
from flaskapp_db.connections import cursor_conn

def users():
    c, conn = cursor_conn()
    c.execute('''CREATE TABLE IF NOT EXISTS FLASKAPP.users (
                email VARCHAR(55) NOT NULL,
                password VARCHAR(100) NOT NULL,
                username VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(20) NOT NULL,
                mobile VARCHAR(20) PRIMARY KEY,
                role ENUM('relief', 'report') NOT NULL);
                ''')
    c.close()
    conn.close()
    return

