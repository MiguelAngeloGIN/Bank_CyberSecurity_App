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


class UserSql(): 
    #Insert methods    
    @staticmethod
    def insert_client(username, email, phone_country_code, phone_number, city,
                    street, postal_code, password_hash, passkey_public_key, 
                    digital_signature_public_key, passcode_hash, mfa_secret):
                     

                    sql = """INSERT INTO Clients (username, email, phone_country_code, phone_number, city,
                    street, postal_code, password_hash, passkey_public_key, digital_signature_public_key
                    passcode_hash, mfa_secret)

                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

                    values = (username, email, phone_country_code, phone_number, city,
                    street, postal_code, password_hash, passkey_public_key,
                    digital_signature_public_key, passcode_hash, mfa_secret)

                    exe_cursor(sql, values)
                    
    @staticmethod
    def insert_clientId(client_id, given_names, last_name, id_type, birthday, 
                     nationality, emission_country, issue_date, expiration_date,
                     is_verified
                     ):

                    sql = """INSERT INTO Clients_ids (client_id, given_names, last_name, id_type, birthday, 
                     nationality, emission_country, issue_date, expiration_date,
                     is_verified)

                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

                    values = (client_id, given_names, last_name, id_type, birthday, 
                     nationality, emission_country, issue_date, expiration_date,
                     is_verified)
                    
                    exe_cursor(sql, values)

    @staticmethod
    def insert_notification(client_id, notification_type, notification_purpose, status):
            sql = """ INSERT INTO NotificationLog (client_id, notification_type, notification_purpose, status)

                      VALUES (%s, %s, %s, %s)
                  """
            values = (client_id, notification_type, notification_purpose, status)

            exe_cursor(sql, values)

    # Update methods    
    @staticmethod
    def deactivate_client(client_id):
            sql = """
                    UPDATE Clients
                    SET is_active = %s
                    WHERE client_id = %s
                   """
            values = (False, client_id)

            exe_cursor (sql, values)
    
    @staticmethod
    def activate_client(client_id):
            sql = """
                    UPDATE Clients
                    SET is_active = %s
                    WHERE client_id = %s
                   """
            values = (True, client_id) 

            exe_cursor (sql, values)
    
    @staticmethod
    def verify_id(client_id):
            sql = """
                    UPDATE Clients_ids
                    SET is_verified = %s
                    WHERE client_id = %s
                   """
            values = (True, client_id)

            exe_cursor (sql, values)
    
    @staticmethod
    def expire_id():
            sql = """
                    UPDATE Clients_ids
                    SET is_verified = %s
                    WHERE expiration_date < NOW ()
                   """
            values = (False,) 

            exe_cursor (sql, values)
    
   
    
    