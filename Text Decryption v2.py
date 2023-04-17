def vigenere_decipher(text, keyword):

    # create a list of shift values based on the keyword
    shifts = [ord(char) - 65 for char in keyword.upper()]
    shift_index = 0
    result = ""
    # loop through each character in the text
    for char in text:
        # check if the character is a letter
        if char.isalpha():
            # get the ASCII code of the character and subtract the shift amount
            shifted_code = ord(char) - shifts[shift_index % len(shifts)]
            # check if the shifted code is outside the range of uppercase or lowercase letters
            if char.isupper():
                if shifted_code < ord('A'):
                    shifted_code += 26
            else:
                if shifted_code < ord('a'):
                    shifted_code += 26
            # convert the shifted ASCII code back to a character and add it to the result
            result += chr(shifted_code)
            shift_index += 1
        else:
            # if the character is not a letter, add it to the result unchanged
            result += char
    return result

encrypted_text = "Zincs Pgvnu!"
keyword = "secret"
decrypted_text = vigenere_decipher(encrypted_text, keyword)
print(decrypted_text)
