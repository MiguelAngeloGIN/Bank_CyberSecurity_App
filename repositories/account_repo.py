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

class AccountSql(): 
    #Insert methods
    @staticmethod
    def insert_accounts(iban, bic, balance):

        sql = """INSERT INTO Accounts (iban, bic, balance)
                 VALUES (%s, %s, %s)
               """

        values = (iban, bic, balance)

        exe_cursor(sql, values)

    @staticmethod
    def insert_accountsOwners (client_id, account_id, ownership_type):
       sql = """
                INSERT INTO AccountsOwners (client_id, account_id, ownership_type)
                VALUES (%s, %s, %s)
             """
       
       values = (client_id, account_id, ownership_type)

       exe_cursor(sql, values)

    @staticmethod
    def deactivate_account(account_id):
       sql = """
                UPDATE Accounts
                SET is_active = %s
                WHERE account_id = %s
               """
       values = (False, account_id)
        
       exe_cursor (sql, values)
         


