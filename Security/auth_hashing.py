from argon2 import PasswordHasher, VerifyMismatchError      

class PwdHasher:
 ph = PasswordHasher()

 @staticmethod
 def hash_password(password):
  hashed_password = PwdHasher.ph.hash(password)
  return hashed_password
 
 @staticmethod
 def verify_password(stored_hash, new_pwd):
  try: 
   PwdHasher.ph.verify(stored_hash, new_pwd)
   return True
  except VerifyMismatchError:
   return False
  
class MfaBackupHasher:
 mh = PasswordHasher()

 @staticmethod
 def hash_mfaCode(code):
  hashed_password = MfaBackupHasher.mh.hash(code)
  return hashed_password
 
 @staticmethod
 def verify_password(stored_hash, new_code):
  try: 
   MfaBackupHasher.mh.verify(stored_hash, new_code)
   return True
  except VerifyMismatchError:
   return False
  
  
  


  


