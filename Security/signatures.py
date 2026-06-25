import hashlib
import hmac
import secrets
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
import time
   
class SignMAC:
  @staticmethod
  def sign_message (secret, message):
   signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
   return signature
 
  @staticmethod
  def compare_signature (expected, received):
    return hmac.compare_digest(expected, received)

class DigitalSignature:
  public_key = None
  private_key = None
  last_generated = 0

  @staticmethod
  def generate_keys():
    DigitalSignature.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    DigitalSignature.public_key = DigitalSignature.private_key.public_key()
    DigitalSignature.last_generated = time.time()
    return DigitalSignature.private_key, DigitalSignature.public_key

  @staticmethod
  def rotate_keys():
    rotation_interval = 6 * 30 * 24 * 60 * 60     # converting 6 months to seconds
    if time.time() - DigitalSignature.last_generated> rotation_interval:
       DigitalSignature.generate_keys()
    return "Digital signature keys rotated"
  
  @staticmethod
  def digitally_sign(message):
    signature = DigitalSignature.private_key.sign(message.encode(),
        padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
 )
    return signature
  
  def verify_digital_sign(message, signature):
    pass


  


       
    

  
  


