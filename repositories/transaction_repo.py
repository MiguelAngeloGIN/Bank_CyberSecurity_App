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
                            mac_signature, nonce, status = "pending"):

                    sql = """INSERT INTO Transactions (from_account, to_account,
                                          amount, status, reference, mac_signature, nonce)

                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """

                    values = (from_account, to_account, amount, status, reference, mac_signature, nonce)

      
                    exe_cursor(sql, values)    
    
    @staticmethod
    def insert_transaction(account_id, daily_limit, per_transaction_limit):

                    sql = """INSERT INTO Transactions (account_id, daily_limit, per_transaction_limit))

                    VALUES (%s, %s, %s)
                    """

                    values = (account_id, daily_limit, per_transaction_limit)

      
                    exe_cursor(sql, values)    



create table Transactions ( 
    transaction_id int auto_increment primary key, 
    from_account int not null, 
    to_account int not null,
    amount decimal(15,2) not null check (amount > 0), 
    transaction_time timestamp default current_timestamp(), 
    status enum ('completed', 'failed', 'pending') not null,
    reference text,
    mac_signature varchar(255) not null,
    nonce varchar(255) not null unique,
    foreign key (from_account) references Accounts (account_id),
    foreign key (to_account) references Accounts (account_id)
);
 create table TransactionLimits (
    account_id int primary key,
    daily_limit decimal(10,2) default 100000,
    per_transaction_limit decimal (10,2) default 50000,
    foreign key (account_id) references Accounts(account_id)
);

   





