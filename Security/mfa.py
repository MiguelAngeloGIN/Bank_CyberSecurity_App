import time
import pyotp
import qrcode
import secrets
import cryptography


class Time_OTP:
    @staticmethod
    def generate_totp(secret):
        totp = pyotp.TOTP(secret)
        return totp.now()
    
    @staticmethod
    def verify_totp(secret, totp_input): 
        totp = pyotp.TOTP(secret)
        return totp.verify(totp_input, valid_window=1)
    
    @staticmethod
    def generate_totp_QR(secret, username):
        uri = pyotp.TOTP(secret).provisioning_uri(username, issuer_name= "MG Bank")
        filename = f"{username}_totp.png"
        img = qrcode.make(uri)
        img.save(filename)
        img.show()


class Backup_MFAcode:
    @staticmethod
    def generate_backup():
        codes = []
        for _ in range(8):
            code = secrets.token_hex(4)
            codes.append(code)
        return codes
    

    


