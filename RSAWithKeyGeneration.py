import random
from affine_cipher import gcd
from SquareAndMultipy import square_and_multiply
from PrimalityTests import miller_rabin_primality_test

def extended_gcd(a, b):
    """
    Computes the greatest common divisor of two integers and the coefficients of Bézout's identity, 
    which are integers x and y such that ax + by = gcd(a, b)

    Parameters:
    - a: first number.
    - b: second number.

    Returns:
    - The GCD of two integers and the Bézout's identity
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1

    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t

def mod_inverse(a, m):
    """
    Computes the modular inverse of a number a mod m using the Extended Euclidean algorithm. 

    Parameters:
    - a: the number for which the inverse is going to be found
    - m: the modulus

    Returns:
    - The modular inverse of a mod m if it exists, otherwise it returns an error
    """
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"{a} has no modular inverse modulo {m}")
    else:
        return x % m

def generate_key_pair(key_size):
    """
    Generates an RSA key pair with the specified key size.

    Parameters:
    - key_size: the desired size of the key (1024, 2048, etc...)

    Returns:
    - The public and private key pair generated
    """
    # Choose two distinct prime numbers p and q
    p = generate_prime(key_size // 2)
    q = generate_prime(key_size // 2)
    
    # Compute n = p * q
    n = p * q
    
    # Compute Phi(n) = (p - 1) * (q - 1)
    phi_n = (p - 1) * (q - 1)
    
    # Choose the public exponent e such that 1 < e < phi_n and gcd(e, phi_n) = 1
    e = random.randrange(1, phi_n)
    while gcd(e, phi_n) != 1:
        e = random.randrange(1, phi_n)
    
    # Compute the private exponent d such that d * e ≡ 1 (mod phi_n)
    d = mod_inverse(e, phi_n)
    
    return (n, e), (n, d)

def generate_prime(bit_length):
    """
    Generates a random prime number with the specified bit length.

    Parameters:
    - bit_length: the length of the exponent for the prime numbers to be generated

    Returns:
    - The number of the specified length generated after being checked if it is a prime using the Miller-Rabin Primality test
    """
    while True:
        p = random.randrange(2 ** (bit_length - 1), 2 ** bit_length)
        if miller_rabin_primality_test(p):
            return p
        
def rsa_encrypt(plaintext, public_key):
    """
    Encrypts the plaintext message with the public key generated using the RSA Cyptosystem.

    Parameters:
    - plaintext: the plaintext to be encrypted using the RSA Cryptosystem
    - public_key: the public key used to encrypt the message

    Returns:
    - The encrypted ciphertext
    """
    n, e = public_key
    ciphertext = square_and_multiply(plaintext, e, n)
    return ciphertext

def rsa_decrypt(ciphertext, private_key):
    """
    Decrypts the ciphertext message with the private key generated using the RSA Cyptosystem.

    Parameters:
    - ciphertext: the ciphertext to be decrypted using the RSA Cryptosystem
    - private_key: the private key used to decrypt the ciphertext

    Returns:
    - The decrypted message
    """
    n, d = private_key
    plaintext = square_and_multiply(ciphertext, d, n)
    return plaintext

def main():
    # Generate the key pair
    key_size = 1024
    public_key, private_key = generate_key_pair(key_size)
    
    print(f"Public key:{public_key}\n")
    print(f"Private key:{private_key}\n")

    # Encrypt the message using RSA encryption
    plaintext = 777
    ciphertext = rsa_encrypt(plaintext, public_key)
    print(f"Plaintext: {plaintext}")
    print(f"Ciphertext: {ciphertext}")

    # Decrypt the ciphertext using RSA decryption
    decrypted_message = rsa_decrypt(ciphertext, private_key)
    print(f"Decrypted message: {decrypted_message}")

if __name__ == "__main__":
    main()