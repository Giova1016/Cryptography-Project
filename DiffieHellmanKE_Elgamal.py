from affine_cipher import gcd, mod_inverse
from SquareAndMultipy import square_and_multiply
import random

def is_primitive_root(g, p):
    phi = p - 1
    for x in range(2, phi):
        if gcd(x, phi) == 1:
            if square_and_multiply(g, x, p) == 1:
                return False
    return True

def dhke(p):
    alpha = random.randint(2, p - 1)
    while not is_primitive_root(alpha, p):
        alpha = random.randint(2, p - 1)
        
    a = random.randint(2, p - 2)
    A = square_and_multiply(alpha, a, p)
    
    b = random.randint(2, p - 2)
    B = square_and_multiply(alpha, b, p)
    
    k_ab = square_and_multiply(B, a, p)
    k_ba = square_and_multiply(A, b, p)
    
    assert k_ab == k_ba
    
    return alpha, k_ab

def elgamal_encrypt(message, p, alpha, k_pub):
    k = random.randint(2, p - 2)
    delta = square_and_multiply(alpha, k, p)
    Beta = (message * square_and_multiply(k_pub, k, p)) % p
    return delta, Beta

def elgamal_decrypt(delta, Beta, p, k_priv, alpha):
    s = square_and_multiply(delta, k_priv, p)
    s_inv = mod_inverse(s, p)
    message = (Beta * s_inv) % p
    return message

def main():
    # Generate the Diffie-Hellman paramaters
    p = 29
    alpha, k_ab = dhke(p)
    
    # Key pair of the receiver
    k_priv = random.randint(2, p - 2)
    k_pub = square_and_multiply(alpha, k_priv, p)
    
    # Sender's encrypted message sent to the receiver   
    message = 26 # Plaintext message
    delta, Beta = elgamal_encrypt(message, p, alpha, k_pub)
    print(f"Encrypted message: {delta}")
    print(f"Encrypted message: {Beta}")
    
    # Receiver decrypts the message
    decrpted_message = elgamal_decrypt(delta, Beta, p, k_priv, alpha)
    print(f"Decrypted message: {decrpted_message}")
    
if __name__ == "__main__":
    main()