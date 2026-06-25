import hashlib
import hmac
   
class SignMAC:
  @staticmethod
  def sign_message (secret, message):
   signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
   return signature
 
  @staticmethod
  def compare_signature (expected, received):
    return hmac.compare_digest(expected, received)

  
  


