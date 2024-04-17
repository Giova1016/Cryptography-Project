import random

def generate_key(length):
    """
    Generates a random key of 1's and 0's (binary) of the same length as the plaintext provided. 

    Parameters:
    - length(int): The length of the key to be generated.

    Returns:
    - A string of random 1's and 0's representing the generated key.
    """
    key = ''.join(random.choice('01') for _ in range(length)) # Selects 1 or 0 at random to generate the key that is the same length as the plaintext provided.
    return key

def text_to_binary(text):
    """
    Converts the plaintext message to binary.

    Parameters:
    - text (str): The plaintext message to be converted.

    Returns:
    - The binary conversion of the plaintext message. 
    """
    binary_message = ''.join(format(ord(char), '08b') for char in text)
    return binary_message

def encrypt_message(message, key):
    """
    Encrypts a given plaintext message using Stream Cipher.

    Parameters:
    - message(str): The input message to be encrypted.
    - key(str): The key used to encrypt the message.

    Returns:
    - The encrypted ciphertext message.
    """
    encrypted_message = '' # Initialize an empty string
    for i in range(len(message)):
        key_index = i % len(key)
        encrypted_char = chr(ord(message[i]) ^ ord(key[key_index]))
        encrypted_message += encrypted_char
    return encrypted_message # Return the encrypted message after being XORed with the key

def decrypt_message(encrypted_message, key):
    """
    Decrypts a given ciphertext using Stream Cipher.

    Parameters:
    - encrypted_message(str): The encrypted message to be decrypted.
    - key(str): The key used to decrypt the message.

    Returns:
    - The decrypted plaintext message.
    """
    decrypted_message = '' # Initialize an empty string
    for i in range(len(encrypted_message)):
        key_index = i % len(key)
        decrypted_char = chr(ord(encrypted_message[i]) ^ ord(key[key_index]))
        decrypted_message += decrypted_char
    return decrypted_message # Return the decrypted message after being XORed with key key

def main():
    # Example plaintext message 
    plaintext_message = "Hello World"
    binary_plaintext_message = text_to_binary(plaintext_message)
    # print("Plaintext(binary):", binary_plaintext_message) # remove comment to see the binary conversion of the plaintext.
    
    # Generate a random key 
    key = generate_key(len(binary_plaintext_message))
    # print("Random generated key:", key) # remove comment to see the random key generated.
    
    # Encrypt the plaintext message
    encrypted_message = encrypt_message(plaintext_message, key)
    print("Encrypted message:", text_to_binary(encrypted_message))
    
    # Decrypt the encrypted message
    decrypted_message = decrypt_message(encrypted_message, key)
    print("Decrypted message:", decrypted_message)
    
if __name__ == "__main__":
    main()