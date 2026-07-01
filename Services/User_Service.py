from security.validators import InputValidator
from repositories.user_repo import UserSql
from repositories.auth_repo import AuthSql
from security.auth_hashing import Hasher
from security.mfa import Secrets, Backup_MFAcode


class UserServices:
    @staticmethod
    def signup (username, email, phone_country_code, phone_number,
               city, street, postal_code, password, passcode,
               given_names, last_name, id_type, id_number,
               birthday, nationality, emission_country, 
               issue_date, expiration_date):
        #1. Validate input (username, email, phone, password)
        #2. Check duplicates (username, email, phone, ID)
        #3. Hash password
        #4. Insert client (is_active = True, is_verified = False)
        #5. Insert ID (is_verified = False)
        #6. Create default account
        #7. Generate backup codes
        #8. Log action
        #9. Return success
        # 1. Input validation
        InputValidator.validate_username(username)
        InputValidator.validate_email(email)
        InputValidator.validate_password(password)
        if not InputValidator.validate_passcode(passcode):
          raise ValueError(
        "Passcode must be exactly 4 digits, should have more than one number and should't be sequential"
    ) 
        InputValidator.validate_nationality(nationality)
        InputValidator.validate_street(street)  
        InputValidator.validate_city(city)
        InputValidator.validate_postal_code(postal_code)
        InputValidator.validate_country_code(phone_country_code)
        InputValidator.validate_phone(phone_number)
        InputValidator.validate_given_names(given_names)
        InputValidator.validate_last_name(last_name)
        InputValidator.validate_id_type(id_type)
        InputValidator.validate_id_number(id_number)
        InputValidator.validate_birthday(birthday)
        InputValidator.validate_emission_country(emission_country)
        InputValidator.validate_issue_date(issue_date)
        InputValidator.validate_expiration_date(expiration_date) 

        #2. Duplicate check
        if UserSql.get_client_by_username(username):
          raise ValueError("Username already taken")
        
        if UserSql.get_client_by_email(email):
           raise ValueError("The email address is already associated with another client")
        
        if UserSql.get_client_by_phone(phone_country_code, phone_number):
           raise ValueError("The phone number is already associated with another client")
        
        if UserSql.get_client_by_id_number(id_number, emission_country):
           raise ValueError("The ID is already associated with another client")
        
        # 3. Check password strength and hash
        score, response = InputValidator.password_feedback(password)
        if score < 3:
           raise ValueError(response)
        password_hash = Hasher.hash(password)
        passcode_hash = Hasher.hash(passcode)
        backup_codes = Backup_MFAcode.generate_backup()
        mfa_secret = Secrets.generate_totp_secret()

        UserSql.insert_client(username, email, phone_country_code, phone_number, city,
                    street, postal_code, password_hash, passcode_hash, mfa_secret)
        
        client = UserSql.get_client_by_username(username)
        client_id = client[0]
        
        UserSql.insert_clientId(client_id, id_number, given_names, last_name, id_type, birthday, 
                     nationality, emission_country, issue_date, expiration_date
                     )
        codes = []
        for code in backup_codes:
         codes.append(code)
         backup_code_hash = Hasher.hash(code)
         AuthSql.insert_backupCode(client_id, backup_code_hash)
        return (
            "Signup successful.\n\n"
            "Save these backup codes in a safe place. They will not be shown again.\n\n"
             + "\n".join(codes)
            )

       

          

           
        
        



