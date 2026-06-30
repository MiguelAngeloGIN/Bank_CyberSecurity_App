import re
import decimal
from zxcvbn import zxcvbn

class InputValidator:

    @staticmethod
    def validate_username(username: str):
        if not isinstance(username, str):
            return False
        return bool(re.fullmatch(r"[a-zA-Z0-9_]{3,30}", username))

    @staticmethod
    def validate_password(password):
        if not isinstance(password, str):
            return False

        if len(password) < 8 or len(password) > 20:
            return False
        
        if not re.search(r"\d", password):    #password should have at least 1 number
            return False                      
        
        if not re.search(r"[A-Z]", password): #password should have at least 1 uppercase character
            return False
        
        if not re.search(r"[a-z]", password): #password should have at least 1 lowercase character
            return False
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-\[\]/~`+=]", password): # password should have at least 1 special character
         return False

        return True
        

    @staticmethod
    def password_feedback(password):
     result = zxcvbn(password)
     score = result["score"]
     feedback = result.get("feedback", {})
     warning = feedback.get("warning") or "None"
     suggestions = feedback.get("suggestions", [])

     if score >= 3:
        return f"Good Password: Score of {score}"

     response = f"Weak password: Score of {score}"
     response += f"\nWarning: {warning}"
     response += "\nSuggestions:"

     for suggestion in suggestions:
        response += f"\n- {suggestion}"

     return response

    
    @staticmethod
    def validate_email(email):
        if not isinstance(email, str):
            return False
        return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", email))

    @staticmethod
    def validate_phone(phone):
        if not isinstance(phone, str):
            return False
        return bool(re.fullmatch(r"\d{7,15}", phone))

    @staticmethod
    def validate_amount(amount):
        try:
            value = decimal.Decimal(str(amount))
        except:
            return False

        if value <= 0:
            return False

        if value > decimal.Decimal("1000000"):  # safety cap
            return False

        return True

    @staticmethod
    def validate_iban(iban):
        if not isinstance(iban, str):
            return False

        iban = iban.replace(" ", "").upper()
        return bool(re.fullmatch(r"[A-Z]{2}[0-9A-Z]{13,34}", iban))


    @staticmethod
    def validate_bic(bic):
        if not isinstance(bic, str):
            return False
        return bool(re.fullmatch(r"[A-Z]{6}[A-Z0-9]{2}([A-Z0-9]{3})?", bic))


    @staticmethod
    def validate_country_code(code):
        if not isinstance(code, str):
            return False
        return bool(re.fullmatch(r"\+\d{1,4}", code))

    @staticmethod
    def validate_token(token):
        if not isinstance(token, str):
            return False
        return len(token) >= 32


    @staticmethod
    def validate_base64_signature(sig):
        if not isinstance(sig, str):
            return False
        return bool(re.fullmatch(r"[A-Za-z0-9+/=]+", sig))
    





