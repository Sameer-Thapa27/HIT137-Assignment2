#Group Name: DAN/EXT 29

#Group Members:
#Faisal Shahriar - S390914
#Riad Sarkar Santo - S394943
#Kanij Fatema - S394326
#Sameer Thapa - S397773

# HIT137 Assignment 2 - Question 1

# Function to encrypt text
def encrypt_text(text, shift1, shift2):
    result = ""

    for char in text:
        # Lowercase letters
        if char.islower():
            if 'a' <= char <= 'm':
                result += chr((ord(char) - ord('a') + (shift1 * shift2)) % 26 + ord('a'))
            else:
                result += chr((ord(char) - ord('a') - (shift1 + shift2)) % 26 + ord('a'))

        # Uppercase letters
        elif char.isupper():
            if 'A' <= char <= 'M':
                result += chr((ord(char) - ord('A') - shift1) % 26 + ord('A'))
            else:
                result += chr((ord(char) - ord('A') + (shift2 ** 2)) % 26 + ord('A'))

        # Other characters remain unchanged
        else:
            result += char

    return result


# Function to decrypt text
def decrypt_text(text, shift1, shift2):
    result = ""

    for char in text:
        # Lowercase letters
        if char.islower():
            if 'a' <= char <= 'm':
                result += chr((ord(char) - ord('a') - (shift1 * shift2)) % 26 + ord('a'))
            else:
                result += chr((ord(char) - ord('a') + (shift1 + shift2)) % 26 + ord('a'))

        # Uppercase letters
        elif char.isupper():
            if 'A' <= char <= 'M':
                result += chr((ord(char) - ord('A') + shift1) % 26 + ord('A'))
            else:
                result += chr((ord(char) - ord('A') - (shift2 ** 2)) % 26 + ord('A'))

        # Other characters remain unchanged
        else:
            result += char

    return result


# Encryption function (file handling)
def encryption():
    with open("raw_text.txt", "r") as file:
        text = file.read()

    encrypted = encrypt_text(text, shift1, shift2)

    with open("encrypted_text.txt", "w") as file:
        file.write(encrypted)


# Decryption function (file handling)
def decryption():
    with open("encrypted_text.txt", "r") as file:
        text = file.read()

    decrypted = decrypt_text(text, shift1, shift2)

    with open("decrypted_text.txt", "w") as file:
        file.write(decrypted)


# Verification function
def verify():
    with open("raw_text.txt", "r") as file1:
        original = file1.read()

    with open("decrypted_text.txt", "r") as file2:
        decrypted = file2.read()

    if original == decrypted:
        print("Verification Successful: Decryption matches original text.")
    else:
        print("Verification Failed: Decryption does not match.")
def encrypt_text(text, shift1, shift2):
    result = ""

    for ch in text:
        if ch.islower():
            if 'a' <= ch <= 'm':
                shift = shift1 * shift2
                encrypted = chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
                result += "L1" + encrypted  # L1 = lowercase range 1 (a-m)
            else:  # n-z
                shift = shift1 + shift2
                encrypted = chr((ord(ch) - ord('a') - shift) % 26 + ord('a'))
                result += "L2" + encrypted  # L2 = lowercase range 2 (n-z)

        elif ch.isupper():
            if 'A' <= ch <= 'M':
                shift = shift1
                encrypted = chr((ord(ch) - ord('A') - shift) % 26 + ord('A'))
                result += "U1" + encrypted  # U1 = uppercase range 1 (A-M)
            else:  # N-Z
                shift = shift2 ** 2
                encrypted = chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
                result += "U2" + encrypted  # U2 = uppercase range 2 (N-Z)

        else:
            result += "NN" + ch  # NN = non-alphabetic

    return result


def decrypt_text(text, shift1, shift2):
    result = ""
    i = 0

    while i < len(text):
        # Read the 2-character prefix
        if i + 2 < len(text):
            prefix = text[i:i+2]
            ch = text[i+2] if i+2 < len(text) else ''

            if prefix == "L1":  # Lowercase a-m
                shift = shift1 * shift2
                result += chr((ord(ch) - ord('a') - shift) % 26 + ord('a'))
                i += 3

            elif prefix == "L2":  # Lowercase n-z
                shift = shift1 + shift2
                result += chr((ord(ch) - ord('a') + shift) % 26 + ord('a'))
                i += 3

            elif prefix == "U1":  # Uppercase A-M
                shift = shift1
                result += chr((ord(ch) - ord('A') + shift) % 26 + ord('A'))
                i += 3

            elif prefix == "U2":  # Uppercase N-Z
                shift = shift2 ** 2
                result += chr((ord(ch) - ord('A') - shift) % 26 + ord('A'))
                i += 3

            elif prefix == "NN":  # Non-alphabetic
                result += ch
                i += 3

            else:
                # If no prefix found, treat as regular character (shouldn't happen)
                result += ch
                i += 1
        else:
            break

    return result


def main():
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    with open("raw_text.txt", "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Encrypt
    encrypted = encrypt_text(raw_text, shift1, shift2)
    with open("encrypted_text.txt", "w") as f:
        f.write(encrypted)
    #print("Encryption successful: 'encrypted_text.txt' created.")
    #print(f"Encrypted text: {encrypted}")

    # Decrypt
    decrypted = decrypt_text(encrypted, shift1, shift2)
    with open("decrypted_text.txt", "w") as f:
        f.write(decrypted)
    print("Decryption successful: 'decrypted_text.txt' created.")

    # Verify
    if raw_text == decrypted:
        print("Verification: SUCCESS.")
    else:
        print("Verification: FAILED.")
        print("Original:  ", raw_text)
        print("Decrypted:", decrypted)


if __name__ == "__main__":
    main()
