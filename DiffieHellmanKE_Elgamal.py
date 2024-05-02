from PrimalityTests import miller_rabin_primality_test
from affine_cipher import mod_inverse
from SquareAndMultipy import square_and_multiply
from RSAWithKeyGeneration import generate_prime
import random
import time

def is_primitive_root(g, p):
    """
    Checks if g is a primitive root of p.

    Parameters:
    - g: possible primitive root
    - p: number to test the possible primitive root

    Returns:
    - True if g is a primitive root of p, False otherwise
    """
    if not miller_rabin_primality_test(p):
        return False
    
    phi = p - 1
    prime_divisors = []
    for q in range(2, phi + 1):
        if phi % q == 0:
            phi //= q
            prime_divisors.append(q)
            if square_and_multiply(g, (p - 1) // q, p) == 1:
                return False
            
    return True

def dhke(p, alpha):
    """
    The Diffie-Hellman Key Exchange Protocol.

    Parameters:
    - p: a large prime number

    Returns:
    - A random primitive integer, alpha, and the shared session key
    """
       
    a = random.randint(2, p - 2)
    A = square_and_multiply(alpha, a, p)
    
    b = random.randint(2, p - 2)
    B = square_and_multiply(alpha, b, p)
    
    k_ab = square_and_multiply(B, a, p)
    k_ba = square_and_multiply(A, b, p)
    
    assert k_ab == k_ba
    
    return alpha, k_ab

def elgamal_encrypt(message, p, alpha, k_pub, k=None):
    """
    Performs Elgamal encryption on the given message. 

    Parameters:
    - message: the message to be encrypted.
    - p: a large prime number.
    - alpha: a primitive element.
    - k_pub: the receiver's public key

    Returns:
    - The Elgamal ciphertext components delta and Beta
    """
    if k is None:
        k = random.randint(2, p - 2)
    delta = square_and_multiply(alpha, k, p)
    Beta = (message * square_and_multiply(k_pub, k, p)) % p
    return delta, Beta

def elgamal_decrypt(delta, Beta, p, k_priv, alpha):
    """
    Performs Elgamal decryption on the given ciphertext.

    Parameters:
    - delta: the first component of the Elgamal ciphertext
    - Beta: the second component of the Elgamal ciphertext
    - p: a large prime number
    - k_priv: the receiver's private key
    - alpha: a primitive element

    Returns:
    - The decrypted message
    """
    s = square_and_multiply(delta, k_priv, p)
    s_inv = mod_inverse(s, p)
    if s_inv is None:
        raise ValueError("The modular inverse does not exist.")
    message = (Beta * s_inv) % p
    return message

def main():
    # Generate the Diffie-Hellman paramaters
    random_prime = generate_prime(bit_length=28) 
    p = random_prime
    print(f"Large prime number: {p}")
    
    # Find a primitive root modulo p
    start_time=time.time()
    alpha = random.randint(2, p - 1)
    while not is_primitive_root(alpha, p):
        alpha = random.randint(2, p - 1)
    end_time=time.time()
    print(f"alpha = {alpha}")
    print(f"Time taken to find the primitive root alpha:{end_time-start_time: .2f}s")
    
    # Perform the key exchange
    k_ab = dhke(p, alpha)
    print(f"k_ab = {k_ab}")

    # Key pair of the receiver
    k_priv = random.randint(2, p - 2)
    k_pub = square_and_multiply(alpha, k_priv, p)
    
    # Sender's encrypted message sent to the receiver   
    message = 26 # Plaintext message
    k = random.randint(2, p - 2)
    print(f"k = {k}")
    delta, Beta = elgamal_encrypt(message, p, alpha, k_pub, k)
    print(f"Encrypted message (delta): {delta}")
    print(f"Encrypted message (Beta): {Beta}")
    
    # Receiver decrypts the message
    start_time=time.time()
    decrpted_message = elgamal_decrypt(delta, Beta, p, k_priv, alpha)
    end_time=time.time()
    print(f"Decrypted message: {decrpted_message}")
    print(f"Time taken to decrypt:{end_time-start_time: .2f}s")
    
if __name__ == "__main__":
    main()