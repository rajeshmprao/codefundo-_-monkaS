import pymysql
from flaskapp_db.connections import cursor_conn

def victims():
    c, conn = cursor_conn()
    c.execute('''CREATE TABLE IF NOT EXISTS FLASKAPP.victims (
                name VARCHAR(20) NOT NULL,
                reporterMobile VARCHAR(20),
                mobile VARCHAR(20) PRIMARY KEY,
                latitude VARCHAR(55) NOT NULL,
                longitude VARCHAR(55) NOT NULL,
                status ENUM('rescued', 'not_rescued', 'dead') NOT NULL,
                FOREIGN KEY (reporterMobile) REFERENCES users(mobile));
                ''')
    c.close()
    conn.close()
    return