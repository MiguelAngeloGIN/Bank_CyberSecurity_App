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
    def insert_transactionReceipt(transaction_id, pdf_hash, digital_signature):

                    sql = """INSERT INTO TransactionReceipts (transaction_id, pdf_hash, digital_signature)

                    VALUES (%s, %s, %s)
                    """

                    values = (transaction_id, pdf_hash, digital_signature)

                    exe_cursor(sql, values)

    @staticmethod
    def insert_transaction(from_account, to_account, amount, reference,
                            mac_signature, status = "pending"):

                    sql = """INSERT INTO Transactions (from_account, to_account,
                                          amount, status, reference, mac_signature)

                    VALUES (%s, %s, %s, %s, %s, %s)
                    """

                    values = (from_account, to_account, amount, status, reference, mac_signature)

                    exe_cursor(sql, values)    

    @staticmethod
    def insert_transactionLog(transaction_id, from_account, to_account,
                                   amount, status, reference, mac_signature):

                    sql = """INSERT INTO TransactionsLog (transaction_id, from_account, to_account,
                                          amount, status, reference, mac_signature)

                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """

                    values = (transaction_id, from_account, to_account,amount, status, reference, mac_signature)

                    exe_cursor(sql, values)    

    #update
    @staticmethod
    def update_failed_transactionStatus(transaction_id):
            sql = """
                    UPDATE Transactions
                    SET status = %s
                    WHERE transaction_id = %s
                   """

            values =  ("failed", transaction_id)

            exe_cursor(sql, values)
    
    @staticmethod
    def update_complete_transactionStatus(transaction_id):
            sql = """
                    UPDATE Transactions
                    SET status = %s
                    WHERE transaction_id = %s
                   """

            values =  ("completed", transaction_id)

            exe_cursor(sql, values)






