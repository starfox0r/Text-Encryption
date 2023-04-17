import string

def encrypt(text, shift):
    # Create a dictionary with each letter mapped to its shifted counterpart
    alphabet = string.ascii_lowercase
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    mapping = str.maketrans(alphabet, shifted_alphabet)

    # Use the dictionary to encrypt the text
    return text.translate(mapping)

def decrypt(text, shift):
    # Decrypt by shifting in the opposite direction
    return encrypt(text, -shift)

plaintext = "Hello World!"
shift = 3

ciphertext = encrypt(plaintext, shift)
print(ciphertext)

decryptedtext = decrypt(ciphertext, shift)
print(decryptedtext)
