import random 

def point_addition(P, Q, a, b, p):
    """
    Perform point addition on an elliptic curve. 

    Parameters:
    - P, Q: the two points (x, y) on the elliptic curve
    - a, b: coefficients of the elliptic curve equation
    - p: the prime modulus

    Returns:
    - The result of the point addition (x, y)
    """ 
    if P == (0, 0):
        return Q
    if Q == (0, 0):
        return P
    
    x1, y1 = P
    x2, y2 = Q
     
    if x1 == x2 and y1 == y2:
        beta = (3*x1*x2 + a) * pow(2*y1, -1, p)
    else:
        beta = (y2 - y1) * pow(x2 - x1, -1, p)
     
    x3 = (beta*beta - x1 - x2) % p
    y3 = (beta * (x1 - x3) - y1) % p
     
    is_point_on_curve((x3, y3), a, b, p)
         
    return x3, y3

def is_point_on_curve(P, a, b, p):
    """
    Checks if the given point P lies on the elliptic curve y^2 = x^3 + a*x + b mod p.

    Parameters:
    - P: the point (x, y) to be checked
    - a, b: coefficients of the elliptic curve equation
    - p: the prime modulus
    """
    x, y = P
    
    assert (y*y) % p == ( pow(x, 3, p) + a*x + b ) % p

def double_and_add(G, k, a, b, p):
    """
    Performs point doubling and adding on an elliptic curve.

    Parameters:
    - G: the point (x, y) on the elliptic curve
    - k: the key to be converted into a binary
    - a, b: coefficients of the elliptic curve equation
    - p: the prime modulus

    Returns:
    - The result of the point doubling and adding(x, y)
    """
    target_point = G
    
    k_binary = bin(k)[2:]
   
    for i in range(1, len(k_binary)):
        current_bit = k_binary[i: i + 1]
         
        # doubling - always
        target_point = point_addition(target_point, target_point, a, b, p)
         
        if current_bit == "1":
            target_point = point_addition(target_point, G, a, b, p)
     
    is_point_on_curve(target_point, a, b, p)
     
    return target_point



def ecdh(G, a, b, p):
    """
    Performs the Elliptic Curve Diffie-Hellman Key Exchange.

    Parameters:
    - B: the point (x, y) on the elliptic curve
    - p: the prime modulus
    - a, b: coefficients of the elliptic curve equation
    - P: the base point (x, y) on the elliptic curve

    Returns:
    - The shared secret key (x, y) on the elliptic curve
    """
    # Alice's private key
    private_key_a = random.getrandbits(256)
    
    # Bob's private key
    private_key_b = random.getrandbits(256)
    
    # Alice's  public keys
    public_key_a = double_and_add(G, private_key_a, a, b, p)
    
    # Bob's public keys
    public_key_b = double_and_add(G, private_key_b, a, b, p)
    
    # The secret key computed by Alice
    T_AB = double_and_add(public_key_b, private_key_a, a, b, p)
    
    # The secret key computed by Bob
    T_BA = double_and_add(public_key_a, private_key_b, a, b, p)
    
    if T_AB != T_BA:
        print("Error: Shared secret keys do not match.")
    
    return T_AB

def main():
    # Choose a prime p and the elliptic curve parameters a, b
    p = pow(2, 256) - pow(2, 32) - pow(2, 9) - pow(2, 8) - pow(2, 7) - pow(2, 6) - pow(2, 4) - pow(2, 0)
    a = 0
    b = 7
    
    # base point
    G = (55066263022277343669578718895168534326250603453777594175500187360389116729240, 
         32670510020758816978083085130507043184471273380659243275938904335757337482424)
    
    # Perform ECDH key exchange
    joint_secret = ecdh(G, a, b, p)
    print(f"Shared secret key: {joint_secret}")
    
if __name__ == "__main__":
    main()