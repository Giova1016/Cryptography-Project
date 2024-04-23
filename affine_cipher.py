def gcd(a, b):
    """
    Computes the greatest common divisor (GCD) of the two numbers using the Euclidean algorithm. 

    Parameters:
    - a: first number.
    - b: second number.

    Returns:
    - GCD of a and b.
    """
    while b != 0:
        a, b = b, a % b # Update a and b using the Euclidean algorithm 
    return a

def mod_inverse(a, m):
    """
    Computes the modular inverse of a number a mod m using the Extended Euclidean algorithm. 

    Parameters:
    - a: the number for which the inverse is going to be found.
    - m: the modulus.

    Returns:
    - The modular inverse of a mod m if it exists, otherwise it returns None
    """
    for i in range(1, m):
        if (a * i) % m == 1:
            return i # Return the modular inverse if found
    return None

def encrypt(plaintext, a, b):
    """
    Encrypts a given plaintext using Affine Cipher.

    Parameters:
    - plaintext: the input message to be encrypted.
    - a: The multiplier in the encryption formula.
    - b: The constant term in the encryption formula.

    Returns:
    - The encrypted message.
    """
    result = "" # Initialize an empty string
    m = 26 # Size of the English alphabet 
    
    for char in plaintext:
        if char.isalpha():
            if char.isupper():
                result += chr((a * (ord(char) - ord('A')) + b) % m + ord('A')) # Encrypts capital letters
            else:
                result += chr((a * (ord(char) - ord('a')) + b) % m + ord('a')) # Encrypts lower-case letters
        else:
            result += char # Non-alphabetic characters are not encrypted
            
    return result

def decrypt(ciphertext, a, b):
    """
    Decrypts a given ciphertext using Affine Cipher.

    Parameters:
    - ciphertext: the encrypted message to be decrypted.
    - a: The multiplier in the decryption formula.
    - b: The constant term in the decryption formula.

    Returns:
    - The decrypted plaintext message.
    """
    # Initialize an empty string
    result = ""
    m = 26 # Size of the English alphabet 
    a_inv = mod_inverse(a, m)
    
    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                result += chr((a_inv * (ord(char) - ord('A') - b)) % m + ord('A')) # Decrypts capital letters
            else:
                result += chr((a_inv * (ord(char) - ord('a') - b)) % m + ord('a')) # Decrypts lower-case letters
        else:
            result += char # Non-alphabetic characters are not decrypted
            
    return result

def main():
    # Example values for a and b 
    a = 7
    b = 22
    
    # Example plaintext message
    plaintext = "Hello World!"
    
    # Encryption
    encrypted_text = encrypt(plaintext, a, b)
    # Test with affine cipher excercise also in the asignment:
    # encrypted_text = "falszztysyjzyjkywjrztyjztyynaryjkyswarztyegyyj"
    print("Encrypted: ", encrypted_text)
    
    # Decryption
    decrypted_text = decrypt(encrypted_text, a, b)
    print("Decrypted: ", decrypted_text)
    
if __name__ == "__main__":
    main()