from database.connection import Connections

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

def fetch_cursor(sql, values=None, fetch_one=False):
    """For SELECT queries - returns data"""
    conn, cursor = get_cursor()
    try:
        if values:
            cursor.execute(sql, values)
        else:
            cursor.execute(sql)
        if fetch_one:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()
        return result
    finally:
        cursor.close()
        conn.close()
        

class UserSql(): 
    #Insert methods    
    @staticmethod
    def insert_client(username, email, phone_country_code, phone_number, city,
                    street, postal_code, password_hash, passcode_hash, mfa_secret):
                     

                    sql = """INSERT INTO Clients (username, email, phone_country_code, phone_number, city,
                    street, postal_code, password_hash, passcode_hash, mfa_secret)

                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

                    values = (username, email, phone_country_code, phone_number, city,
                    street, postal_code, password_hash, passcode_hash, mfa_secret)

                    exe_cursor(sql, values)

             
    @staticmethod
    def insert_clientId(client_id, id_number, given_names, last_name, id_type, birthday, 
                     nationality, emission_country, issue_date, expiration_date
                    
                     ):

                    sql = """INSERT INTO Clients_ids (client_id, id_number, given_names, last_name, id_type, birthday, 
                     nationality, emission_country, issue_date, expiration_date
                     )

                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

                    values = (client_id, id_number, given_names, last_name, id_type, birthday, 
                     nationality, emission_country, issue_date, expiration_date
                     )
                    
                    exe_cursor(sql, values)
    @staticmethod
    def insert_notification(client_id, notification_type, notification_purpose, status):
            sql = """ INSERT INTO NotificationLog (client_id, notification_type, notification_purpose, status)

                      VALUES (%s, %s, %s, %s)
                  """
            values = (client_id, notification_type, notification_purpose, status)

            exe_cursor(sql, values)

    @staticmethod
    def insert_fraudAlert(client_id, cause, level, details):
            sql = """ INSERT INTO FraudAlerts (client_id, cause, level, details)

                      VALUES (%s, %s, %s, %s)
                  """
            values = (client_id, cause, level, details)

            exe_cursor(sql, values)

    # Update methods    
    @staticmethod
    def deactivate_client(client_id):
            sql = """
                    UPDATE Clients
                    SET is_active = False
                    WHERE client_id = %s
                   """
            values = (client_id,)

            exe_cursor (sql, values)
    
    @staticmethod
    def activate_client(client_id):
            sql = """
                    UPDATE Clients
                    SET is_active = True
                    WHERE client_id = %s
                   """
            values = (client_id,) 

            exe_cursor (sql, values)
    
    @staticmethod
    def verify_id(client_id):
            sql = """
                    UPDATE Clients_ids
                    SET is_verified = True
                    WHERE client_id = %s
                   """
            values = (client_id,)

            exe_cursor (sql, values)
    
    @staticmethod
    def expire_id():
            sql = """
                    UPDATE Clients_ids
                    SET is_expired = True
                    WHERE expiration_date < NOW ()
                   """
            
            exe_cursor (sql)
    
    @staticmethod
    def get_client_by_username(username):
     sql = "SELECT client_id FROM Clients WHERE username = %s"
     return fetch_cursor(sql, (username,), fetch_one=True)


    @staticmethod
    def get_client_by_email(email):
      sql = "SELECT client_id FROM Clients WHERE email = %s"
      return fetch_cursor(sql, (email,), fetch_one=True)


    @staticmethod
    def get_client_by_phone(phone_country_code, phone_number):
      sql = """
      SELECT client_id 
      FROM Clients 
      WHERE phone_country_code = %s AND phone_number = %s
      """
      return fetch_cursor(sql, (phone_country_code, phone_number), fetch_one=True)


    @staticmethod
    def get_client_by_id_number(id_number, emission_country):
      sql = """
      SELECT client_id 
      FROM Clients_ids 
      WHERE id_number = %s AND emission_country = %s
      """
      return fetch_cursor(sql, (id_number, emission_country), fetch_one=True)
   
    @staticmethod
    def is_verified(client_id):
      sql = """
      SELECT is_verified
      FROM Clients_ids
      WHERE client_id = %s
      """
      result = fetch_cursor(sql, (client_id,), fetch_one=True)

      if not result:
        return False

      return bool(result[0])

