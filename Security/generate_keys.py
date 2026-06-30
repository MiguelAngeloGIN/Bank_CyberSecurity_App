# This will be used to generate the keys for digital signatures once  and save into the PEM file
# Will not be put into the program so keys don't change all the time
# The public key will be derived from the private key when needed 
# Can run the code periodically to rotate the keys

from cryptography.hazmat.primitives.asymmetric import rsa
from signatures import KeyStorage 

def generate_initial_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    KeyStorage.save_private_key(private_key)
    print("Keys generated and saved.")

if __name__ == "__main__":    
    generate_initial_keys()