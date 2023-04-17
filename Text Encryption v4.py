from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

class AESCipher:
    def __init__(self, key):
        if not isinstance(key, bytes):
            raise TypeError("Key must be bytes")
        if len(key) not in [16, 24, 32]:
            raise ValueError("Invalid key length. Must be 16, 24, or 32 bytes long.")
        self.key = key

    def encrypt(self, plaintext):
        if not isinstance(plaintext, str):
            raise TypeError("Plaintext must be a string")
        plaintext = plaintext.encode("utf-8")
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=iv)
        ciphertext, tag = cipher.encrypt_and_digest(pad(plaintext, AES.block_size))
        return base64.b64encode(iv + ciphertext + tag).decode()

    def decrypt(self, ciphertext):
        if not isinstance(ciphertext, str):
            raise TypeError("Ciphertext must be a string")
        ciphertext = base64.b64decode(ciphertext.encode())
        if len(ciphertext) < AES.block_size + 16:
            raise ValueError("Invalid ciphertext length")
        iv, ciphertext, tag = ciphertext[:AES.block_size], ciphertext[AES.block_size:-16], ciphertext[-16:]
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=iv)
        plaintext = unpad(cipher.decrypt_and_verify(ciphertext, tag), AES.block_size)
        return plaintext.decode("utf-8")

key = b"\xf4\xed\xf3\xf3L\xfb\xd2\x9e\xd9\x89\x0b\xac'\xdaR\x9e\x80r*\x1b\x80G\xde;;qJ\x10\x87\x9f\xe0y"
cipher = AESCipher(key)

while True:
    choice = input("Enter 'e' to encrypt or 'd' to decrypt, or 'q' to quit: ")
    if choice == 'q':
        break
    elif choice == 'e':
        plaintext = input("Enter plaintext to encrypt: ")
        ciphertext = cipher.encrypt(plaintext)
        print("Ciphertext: ", ciphertext)
    elif choice == 'd':
        ciphertext = input("Enter ciphertext to decrypt: ")
        decrypted_plaintext = cipher.decrypt(ciphertext)
        print("Decrypted plaintext: ", decrypted_plaintext)
    else:
        print("Invalid choice. Please enter 'e' to encrypt or 'd' to decrypt, or 'q' to quit.")