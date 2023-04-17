from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64

class AESCipher:
    def __init__(self, key):
        # Convert the key to bytes if it's not already
        if not isinstance(key, bytes):
            key = key.encode()

        # Ensure the key is exactly 16, 24, or 32 bytes long (for AES-128, AES-192, or AES-256)
        if len(key) not in [16, 24, 32]:
            raise ValueError("Invalid AES key length. Must be 16, 24, or 32 bytes long.")

        self.key = key

    def encrypt(self, plaintext):
        # Convert the plaintext to bytes if it's not already
        if not isinstance(plaintext, bytes):
            plaintext = plaintext.encode()

        # Generate a new initialization vector (IV) for each encryption
        iv = AES.new(self.key, AES.MODE_EAX).nonce

        # Create a new AES cipher using the key and IV
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        # Encrypt the plaintext and pad it to a multiple of 16 bytes
        ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

        # Return the IV and ciphertext as a single string
        return base64.b64encode(iv + ciphertext).decode()

key = b't\xdd#\x96\xf7\xb7\x8a\x04p30\x1do\xaf\xc2\x14Z\x1a\xd2\xcd\x80\x15&f\xcc\xa2\xa0\xe9\xa7\x85\xe8&'
cipher = AESCipher(key)

plaintext = "Hello World!"
ciphertext = cipher.encrypt(plaintext)
print(ciphertext)
