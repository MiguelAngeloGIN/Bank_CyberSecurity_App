from database.connection import Connections
from datetime import datetime, timedelta

def get_cursor():
    conn, cursor = Connections.connect_database()
    return conn, cursor

def exe_cursor(sql, values = None, commit = True):
    conn, cursor = get_cursor()
    try:
         if values:
          cursor.execute(sql, values)
         else:
           cursor.execute(sql)    #for queries without values
         if commit:
          conn.commit()

    except Exception:
        conn.rollback()
        raise 

    finally:
         cursor.close()
         conn.close()

class SessionSql(): 
    @staticmethod
    def set_expire():   # all tokens will expire in 1 minute
            exp = datetime.now() + timedelta(seconds=180)
            return exp
    
    #Insert method 
    @staticmethod
    def insert_session(session_id, client_id, session_token, ip_address):
                    

                    sql = """INSERT INTO UserSessions (session_id, client_id, session_token, ip_address, expires_at)

                    VALUES (%s, %s, %s, %s, %s)
                    """

                    exp = SessionSql.set_expire()
    
                    values = (session_id, client_id, session_token, ip_address, exp)

                    exe_cursor(sql, values)

    @staticmethod
    def insert_trustedDevice(client_id, device_fingerprint, ip_address):
                    

                    sql = """INSERT INTO TrustedDevices (client_id, device_fingerprint, ip_address)
                             VALUES (%s, %s, %s)
                    """
    
                    values = (client_id, device_fingerprint, ip_address)

                    exe_cursor(sql, values)




