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

class TransactionSql(): 
    #Insert method 
    @staticmethod
    def insert_transaction(from_account, to_account, amount, reference,
                            mac_signature, nonce, status = "pending"):

                    sql = """INSERT INTO Transactions (from_account, to_account,
                                          amount, status, reference, mac_signature, nonce)

                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """

                    values = (from_account, to_account, amount, status, reference, mac_signature, nonce)

      
                    exe_cursor(sql, values)    
    
    @staticmethod
    def insert_transactionLimit(account_id, daily_limit, per_transaction_limit):

                    sql = """INSERT INTO TransactionLimits (account_id, daily_limit, per_transaction_limit)

                    VALUES (%s, %s, %s)
                    """

                    values = (account_id, daily_limit, per_transaction_limit)

      
                    exe_cursor(sql, values)   

    @staticmethod
    def update_transaction_status(transaction_id, status):
        sql = """UPDATE Transactions 
                 SET status = %s
                 WHERE transaction_id = %s
              """
        values = (status, transaction_id)
        exe_cursor(sql, values) 


