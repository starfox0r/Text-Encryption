from Crypto.Random import get_random_bytes

salts = [get_random_bytes(16) for _ in range(3)]
with open("salts.txt", "wb") as f:
    for salt in salts:
        f.write(salt)
        f.write(b"\n")

print(salts)
