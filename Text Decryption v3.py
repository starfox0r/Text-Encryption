from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
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

    def decrypt(self, ciphertext):
        # Convert the ciphertext to bytes
        ciphertext = base64.b64decode(ciphertext.encode())

        # Split the IV and ciphertext
        iv = ciphertext[:16]
        ciphertext = ciphertext[16:]

        # Create a new AES cipher using the key and IV
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        # Decrypt the ciphertext and remove the padding
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

        # Return the plaintext as a string
        return plaintext.decode()

key = b't\xdd#\x96\xf7\xb7\x8a\x04p30\x1do\xaf\xc2\x14Z\x1a\xd2\xcd\x80\x15&f\xcc\xa2\xa0\xe9\xa7\x85\xe8&'
cipher = AESCipher(key)

ciphertext = "QuuU4v/3+5MiXh2MBocm3mpIWsmWsLd3bI9O/vikDlA="
plaintext = cipher.decrypt(ciphertext)
print(plaintext)
