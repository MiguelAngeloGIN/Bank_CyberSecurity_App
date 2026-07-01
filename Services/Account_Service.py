from repositories.account_repo import AccountSql
from repositories.transaction_repo import TransactionSql
import secrets

class AccountServices:

    @staticmethod
    def generate_iban():
         account_number = ''.join(str(secrets.randbelow(10)) for _ in range(20))
         return f"MZ{account_number}"
    
    @staticmethod
    def generate_bic():
         return "MGBKMZMAXXX"
    
    @staticmethod
    def create_account(client_id):
      iban = AccountServices.generate_iban()
      
      while AccountSql.get_account_by_iban(iban):
          iban = AccountServices.generate_iban()

      bic = AccountServices.generate_bic()

      AccountSql.insert_accounts(iban, bic, balance = 0)

      account = AccountSql.get_account_by_iban(iban)
      account_id = account[0]
         
      AccountSql.insert_accountsOwners (client_id, account_id, ownership_type = "primary")
  
      TransactionSql.insert_transactionLimit(account_id, 50000, 25000 )
        
        
    