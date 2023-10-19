import hashlib
import base64
from cryptography.fernet import Fernet

class EncryptionManager:

    def __init__(self):  # constructor to create an EncryptionManager instance
        pass


    # function that generates an encryption key based on the users account id and password    
    def generate_encryption_key(self, user_id, master_password):
        key = hashlib.pbkdf2_hmac('sha256', master_password.encode(), str(user_id).encode(), 100000)  # generate a key

        """
        PBKDF2 - Password-Based Key Derivation Function 2
        HMAC - Hash-based Message Authentication Code
        pbkdf2_hmac - securely derives a key from the users password and user id
        sha256 - hash function - processes password and user id and turns them into a key
        .encode converts password and userid to a byte sequence (computer readable version of user_id and master_password)
        the number at the end '100000' shows how many time the hashing function is performed
        """

        fernet_key = base64.urlsafe_b64encode(key[:32]).decode()

        """
        base64.urlsafe_b64encode - encodes data into base64 format - urlsafe means it uses characters that are safe to be in URLs
        key[:32] - this will take the first 32 bytes of the key produced earlier
        .decode - returns text to a string format
        """

        return Fernet(fernet_key)  # produces a key for symmetrical encryption