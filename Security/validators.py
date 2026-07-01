import re
import decimal
from zxcvbn import zxcvbn
from datetime import datetime

class InputValidator:

    @staticmethod
    def validate_username(username):
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

      response = f"Password Score: {score}"

      if score >= 3:
        response = f"Good Password: Score of {score}"
      else:
        response = f"Weak Password: Score of {score}"
        response += f"\nWarning: {warning}"
        response += "\nSuggestions:"
        for suggestion in suggestions:
            response += f"\n- {suggestion}"

      return score, response
    
    @staticmethod
    def validate_passcode(passcode):
      if not isinstance(passcode, str):
        return False

      if not re.fullmatch(r"\d{4}", passcode):
        return False
      
      if len(set(passcode)) == 1:   #same number
        return False

      if passcode in ("1234", "4321"):
        return False

      return True

    
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
    def validate_city(city):
      if not isinstance(city, str):
        return False
      return bool(re.fullmatch(r"[A-Za-z\s\-']{2,50}", city))


    @staticmethod
    def validate_street(street):
      if not isinstance(street, str):
        return False
      return bool(re.fullmatch(r"[A-Za-z0-9\s\-',.()]{2,100}", street))


    @staticmethod
    def validate_postal_code(postal_code):
      if not isinstance(postal_code, str):
        return False
      return bool(re.fullmatch(r"[A-Za-z0-9\s\-]{3,20}", postal_code))
    ####################################################################################################################################

    @staticmethod
    def validate_id_number(id_number):
      if not isinstance(id_number, str):
        return False
      return bool(re.fullmatch(r"[A-Za-z0-9\-]{5,60}", id_number))

    @staticmethod
    def validate_given_names(given_names):
      if not isinstance(given_names, str):
        return False
      return bool(re.fullmatch(r"[A-Za-z\s\-']{2,200}", given_names))

    @staticmethod
    def validate_last_name(last_name):
      if not isinstance(last_name, str):
        return False
      return bool(re.fullmatch(r"[A-Za-z\s\-']{2,50}", last_name))

    @staticmethod
    def validate_id_type(id_type):
      if not isinstance(id_type, str):
        return False
      return bool(re.fullmatch(r"[A-Za-z\s\-']{2,50}", id_type))

    @staticmethod
    def validate_birthday(birthday):
      if not isinstance(birthday, str):
        return False
      try:
        datetime.strptime(birthday, '%Y-%m-%d')
        return True
      except ValueError:
        return False

    @staticmethod
    def validate_nationality(nationality):
      if not isinstance(nationality, str):
        return False
      return bool(re.fullmatch(r"[A-Za-z\s\-']{2,50}", nationality))

    @staticmethod
    def validate_emission_country(emission_country):
      if not isinstance(emission_country, str):
        return False
      return bool(re.fullmatch(r"[A-Za-z\s\-']{2,50}", emission_country))

    @staticmethod
    def validate_issue_date(issue_date):
      if not isinstance(issue_date, str):
        return False
      try:
        datetime.strptime(issue_date, '%Y-%m-%d')
        return True
      except ValueError:
        return False

    @staticmethod
    def validate_expiration_date(expiration_date):
      if not isinstance(expiration_date, str):
        return False
      try:
        datetime.strptime(expiration_date, '%Y-%m-%d')
        return True
      except ValueError:
        return False

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
        return bool(re.fullmatch(r"MZ[0-9]{30}", iban))


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
    





