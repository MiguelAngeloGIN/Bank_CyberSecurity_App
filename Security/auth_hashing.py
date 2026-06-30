from argon2 import PasswordHasher, VerifyMismatchError      

# will be used to hash the password, the passcode and the mfa backup codes
class Hasher:
 h = PasswordHasher()

 @staticmethod
 def hash(value):
  hashed = Hasher.h.hash(value)
  return hashed
 
 @staticmethod
 def verify_hash(stored_hash, value):
  try: 
   Hasher.h.verify(stored_hash, value)
   return True
  except VerifyMismatchError:
   return False
  

  


  
  
  


  


