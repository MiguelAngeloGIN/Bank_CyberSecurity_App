import hashlib
import hmac
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization   
import base64
import os
from dotenv import load_dotenv
import uuid

load_dotenv()
def add_nonce(message):       # nonce will be added in messages in order to prevent relay attacks by making same messages have different outputs
    nonce = str(uuid.uuid4())  
    return f"{message}|{nonce}"

class KeyStorage: 
  password = os.getenv("KEY_PASSWORD")
  if password:
    password = password.encode()
  else:
    raise ValueError("KEY_PASSWORD not set") 

  # Private keys stored in a .pem file for more security
  @staticmethod
  def save_private_key(private_key, filename="private_key.pem"):
     pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.BestAvailableEncryption(KeyStorage.password) 
     )

     with open(filename, "wb") as f:
        f.write(pem)
  
  # Read the private key from the PEM file so we can use it
  @staticmethod
  def load_private_key():
    with open("private_key.pem", "rb") as f:
     pem_data = f.read()
     key = serialization.load_pem_private_key(
         pem_data,
         password=KeyStorage.password
     )
     return key
    
  # Use to transform the signatures from bytes so they can be safely sent (or stored if needed)
  # PEM iss the format most used for keys

  @staticmethod
  def public_key_to_pem(key):
    pem = key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return pem

  #Use to transform the signatures into readable data from bytes so they can be stored and safely sent
  @staticmethod
  def signature_to_base64(signature):
   sign_64 = base64.b64encode(signature)
   sign_text = sign_64.decode()          
   return sign_text 


class SignMAC:
 # The mac signatures will be used by the program to verify integrity in the transfers
  # Because it is symetric is faster than digital signature 
  # It is used inside the backend only so it is okay for the key to be 1 shared 

  secret = os.getenv("HMAC_SIGNATURE") # the secret is stored in the env
  if not secret:
        raise ValueError("HMAC_SIGNATURE not set in environment")
  secret = secret.encode()

  @staticmethod
  def sign_message(message): 
   message = add_nonce(message)
   signature = hmac.new(SignMAC.secret, message.encode(), hashlib.sha256).digest() 
   return signature
 
  @staticmethod
  def compare_signature(expected, received):
    return hmac.compare_digest(expected, received)


class DigitalSignature:
  @staticmethod
  def digitally_sign(message):            # first hash message then use private key to sign
    private_key = KeyStorage.load_private_key()
    message_nonced = add_nonce(message)

    signature = private_key.sign(
        message_nonced.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature, message_nonced
  
  @staticmethod
  def verify_digital_sign(signature, message_nonced): # # verify by hashing the message, then compare with the decrypted signature (by the public key)
    try:
      public_key = KeyStorage.load_private_key().public_key()

      public_key.verify(
          signature, 
          message_nonced.encode(), 
          padding.PSS(
              mgf=padding.MGF1(hashes.SHA256()),
              salt_length=padding.PSS.MAX_LENGTH
          ),
          hashes.SHA256()
      )
      return True

    except InvalidSignature:
      return False