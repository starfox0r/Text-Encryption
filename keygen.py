from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(32)  # generate a 32-byte (256-bit) AES key
with open("keyfile.txt", "wb") as f:
    f.write(key)

print(key)