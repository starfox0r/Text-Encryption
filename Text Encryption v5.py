from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
from Crypto.Protocol.KDF import PBKDF2

class AESCipher:
    def __init__(self, key_file, salts_file):
        with open(key_file, 'rb') as f:
            self.key = f.read()
        if len(self.key) not in [16, 24, 32]:
            raise ValueError("Invalid key length. Must be 16, 24, or 32 bytes long.")

        with open(salts_file, 'rb') as f:
            salts = f.read().splitlines()
        if len(salts) != 3:
            raise ValueError("Three salts are required")
        self.salts = [salt if len(salt) == AES.block_size else pad(salt, AES.block_size) for salt in salts]

        for salt in self.salts:
            if len(salt) != AES.block_size:
                raise ValueError("Invalid salt length. Must be equal to block size.")

    def encrypt(self, plaintext):
        plaintext = plaintext.encode("utf-8")
        salt = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=salt)
        ciphertext, tag = cipher.encrypt_and_digest(pad(plaintext, AES.block_size))
        salt_index = int.from_bytes(tag[:2], byteorder='big') % 3
        return base64.b64encode(self.salts[salt_index] + salt + ciphertext + tag).decode()

    def decrypt(self, ciphertext):
        ciphertext = base64.b64decode(ciphertext.encode())
        if len(ciphertext) < AES.block_size + 18:
            raise ValueError("Invalid ciphertext length")
        salt_index = int.from_bytes(ciphertext[-18:-16], byteorder='big') % 3
        salt = ciphertext[AES.block_size:AES.block_size*2]
        ciphertext, tag = ciphertext[AES.block_size*2:-16], ciphertext[-16:]
        cipher = AES.new(self.key, AES.MODE_GCM, nonce=salt)
        plaintext = unpad(cipher.decrypt_and_verify(ciphertext, tag), AES.block_size)
        return plaintext.decode("utf-8")

key_file = "keyfile.txt"
salts_file = "salts.txt"
cipher = AESCipher(key_file, salts_file)

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
