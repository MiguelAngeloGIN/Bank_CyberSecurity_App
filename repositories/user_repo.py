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
    @staticmethod
    def set_expire():   # all tokens will expire in 1 minute
            exp = datetime.now() + timedelta(seconds=60)
            return exp
    
    @staticmethod
    def add_client(username, email, phone_country_code, phone_number, city,
                    street, postal_code, password_hash, passkey_public_key,
                    passcode_hash, mfa_secret):
                     

                    sql = """INSERT INTO Clients (username, email, phone_country_code, phone_number, city,
                    street, postal_code, password_hash, passkey_public_key,
                    passcode_hash, mfa_secret)

                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """

                    values = (username, email, phone_country_code, phone_number, city,
                    street, postal_code, password_hash, passkey_public_key,
                    passcode_hash, mfa_secret)

                    exe_cursor(sql, values)
                    
    @staticmethod
    def add_clientId(client_id, given_names, last_name, id_type, birthday, 
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
    def add_backupCode(client_id, code_hash):

                    sql = """INSERT INTO MFA_BackupCodes (client_id, code_hash)

                    VALUES (%s, %s)
                    """

                    values = (client_id, code_hash)

                    exe_cursor(sql, values)
                
    @staticmethod
    def add_authHistory(client_id, auth_type, authMethod_hash):

                    sql = """INSERT INTO AuthMethodHistory (client_id, auth_type, authMethod_hash)

                    VALUES (%s, %s, %s)
                    """
                    
                    values = (client_id, auth_type, authMethod_hash)

                    exe_cursor(sql, values)
            
    @staticmethod
    def add_passwordResetToken(client_id, token_hash):

                    sql = """INSERT INTO PasswordResetTokens (client_id, expires_at, token_hash)
                          VALUES (%s, %s, %s)
                           """
                    exp = Sql.set_expire()
                    values = (client_id, exp, token_hash )

                    exe_cursor(sql, values)

    @staticmethod
    def add_loginAttempts(client_id, device_fingerprint, user_agent, ip_address,
                                location, outcome, risk_score):

                    sql = """INSERT INTO LoginAttempts (client_id, device_fingerprint, user_agent, ip_address,
                                                        location, outcome, risk_score)
                          VALUES (%s, %s, %s, %s, %s, %s, %s)
                           """
                
                    values = (client_id, device_fingerprint, user_agent, ip_address,
                                location, outcome, risk_score )

                    exe_cursor(sql, values)

    @staticmethod
    def add_notification(client_id, notification_type, notification_purpose, status):
            sql = """ INSERT INTO NotificationLog (client_id, notification_type, notification_purpose, status)

                      VALUES (%s, %s, %s, %s)
                  """
            values = (client_id, notification_type, notification_purpose, status)

            exe_cursor(sql, values)

    @staticmethod
    def add_passcodeAttempt(client_id, account_id, outcome, ip_address, location, risk_score):
            sql = """
                   INSERT INTO PasscodeAttempts (client_id, account_id, outcome, ip_address, location, risk_score)
                   VALUES (%s, %s, %s, %s, %s, %s)
                  """
            values = (client_id, account_id, outcome, ip_address, location, risk_score)

            exe_cursor(sql, values)
            
    
            
        

    
