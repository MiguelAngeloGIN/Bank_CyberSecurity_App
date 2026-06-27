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


class Sql(): 
    #Insert methods
    @staticmethod
    def set_expire():   # all tokens will expire in 1 minute
            exp = datetime.now() + timedelta(seconds=60)
            return exp
    
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
    def insert_backupCode(client_id, code_hash):

                    sql = """INSERT INTO MFA_BackupCodes (client_id, code_hash)

                    VALUES (%s, %s)
                    """

                    values = (client_id, code_hash)

                    exe_cursor(sql, values)
                
    @staticmethod
    def insert_authHistory(client_id, auth_type, authMethod_hash):

                    sql = """INSERT INTO AuthMethodHistory (client_id, auth_type, authMethod_hash)

                    VALUES (%s, %s, %s)
                    """
                    
                    values = (client_id, auth_type, authMethod_hash)

                    exe_cursor(sql, values)
            
    @staticmethod
    def insert_passwordResetToken(client_id, token_hash):

                    sql = """INSERT INTO PasswordResetTokens (client_id, expires_at, token_hash)
                          VALUES (%s, %s, %s)
                           """
                    exp = Sql.set_expire()
                    values = (client_id, exp, token_hash )

                    exe_cursor(sql, values)

    @staticmethod
    def insert_loginAttempts(client_id, device_fingerprint, user_agent, ip_address,
                                location, outcome, risk_score):

                    sql = """INSERT INTO LoginAttempts (client_id, device_fingerprint, user_agent, ip_address,
                                                        location, outcome, risk_score)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)
                           """
                
                    values = (client_id, device_fingerprint, user_agent, ip_address,
                                location, outcome, risk_score )

                    exe_cursor(sql, values)

    @staticmethod
    def insert_notification(client_id, notification_type, notification_purpose, status):
            sql = """ INSERT INTO NotificationLog (client_id, notification_type, notification_purpose, status)

                      VALUES (%s, %s, %s, %s)
                  """
            values = (client_id, notification_type, notification_purpose, status)

            exe_cursor(sql, values)

    @staticmethod
    def insert_passcodeAttempt(client_id, account_id, outcome, ip_address, location, risk_score):
            sql = """
                   INSERT INTO PasscodeAttempts (client_id, account_id, outcome, ip_address, location, risk_score)
                   VALUES (%s, %s, %s, %s, %s, %s)
                  """
            values = (client_id, account_id, outcome, ip_address, location, risk_score)

            exe_cursor(sql, values)
######################################################################################################################################################
    
    # Update methods
    @staticmethod
    def mfa_on(client_id):
            sql = """
                    UPDATE Clients
                    SET mfa_active = %s
                    WHERE client_id = %s
                   """
            values = (True, client_id)

            exe_cursor (sql, values)
    
    @staticmethod
    def mfa_off(client_id):
            sql = """
                    UPDATE Clients
                    SET mfa_active = %s
                    WHERE client_id = %s
                   """
            values = (False, client_id)

            exe_cursor (sql, values)

    @staticmethod
    def lock_client(client_id):
            sql = """
                    UPDATE Clients
                    SET is_locked = %s
                    WHERE client_id = %s
                   """
            values = (True, client_id) 

            exe_cursor (sql, values)
    @staticmethod
    def unlock_client(client_id):
            sql = """
                    UPDATE Clients
                    SET is_locked = %s
                    WHERE client_id = %s
                   """
            values = (False, client_id) 

            exe_cursor (sql, values)
    
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
    
    @staticmethod
    def change_pwd(new_pwd, client_id):
            sql = """
                    UPDATE Clients
                    SET password_hash = %s
                    WHERE client_id = %s
                   """
                
            values = (new_pwd, client_id) 

            exe_cursor (sql, values)
    
    @staticmethod
    def change_passcode(new_passcode, client_id):
            sql = """
                    UPDATE Clients
                    SET passcode_hash = %s
                    WHERE client_id = %s
                   """
                
            values = (new_passcode, client_id) 

            exe_cursor (sql, values)
    
    @staticmethod
    def change_secret(new_secret, client_id):
            sql = """
                    UPDATE Clients
                    SET mfa_secret = %s
                    WHERE client_id = %s
                   """
                
            values = (new_secret, client_id) 

            exe_cursor (sql, values)
    
    @staticmethod
    def change_fidoKey(new_key, client_id):
            sql = """
                    UPDATE Clients
                    SET passkey_public_key = %s
                    WHERE client_id = %s
                   """
                
            values = (new_key, client_id) 

            exe_cursor (sql, values)
    
    @staticmethod
    def change_signKey(new_key, client_id):
            sql = """
                    UPDATE Clients
                    SET digital_signature_public_key = %s
                    WHERE client_id = %s
                   """
                
            values = (new_key, client_id) 

            exe_cursor (sql, values)

    @staticmethod
    def backup_used(client_id):
            sql = """
                    UPDATE MFA_BackupCodes
                    SET used = %s
                    WHERE client_id = %s
                   """
                
            values = (True, client_id) 

            exe_cursor (sql, values)

    @staticmethod
    def token_used(client_id):
            sql = """
                    UPDATE PasswordResetTokens
                    SET used = %s
                    WHERE client_id = %s
                   """
                
            values = (True, client_id) 

            exe_cursor (sql, values)
    
            
    
   
    
            
        

    
