import random 
from PrimalityTests import miller_rabin_primality_test
from affine_cipher import mod_inverse

def is_point_on_curve(P, a, b, p):
    """
    Checks if the given point P lies on the elliptic curve y^2 = x^3 + a*x + b mod p.

    Args:
    - P: the point (x, y) to be checked
    - a, b: coefficients of the elliptic curve equation
    - p: the prime modulus

    Returns:
    - True if the point lies on the curve, False otherwise
    """
    x, y = P
    
    left = y ** 2
    right = (x ** 3 + a * x + b) % p
    
    return left == right

def is_curve_valid(a, b, p):
    """
    Checks if the given elliptic curve parameters a, b, and p are valid.

    Args:
    - a, b: coefficients of the elliptic curve equation
    - p: the prime modulus

    Returns:
    - True if the elliptic curve parameters are valid, False otherwise
    """
    # checks if p is prime
    if not miller_rabin_primality_test(p):
        return False
    if (4 * a ** 3 + 27 * b ** 2) % p == 0:
        return False
    
    return True

def double_and_add(P, n, a, b, p):
    """
    Perform point multiplication on an elliptic curve using the Double-and-Add Algorithm.

    Parameters:
    - P: the base point (x, y) on the elliptic curve
    - n: the scalar to be multiplied with the base point
    - a, b: coefficients of the elliptic curve equation
    - p: the prime modulus

    Returns:
    - The resutl of the point multiplication (x, y)
    """
    Q = (0, 0)
    R = P
    
    for bit in bin(n)[2:]:
        if bit == '1':
            Q = point_addition(Q, R, a, b, p)
        R = point_doubling(R, a, b, p)
        
    return Q

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
        return point_doubling(P, a, b, p)
    if x1 == x2:
        return (0, 0)
    
    m = ((y2 - y1) * mod_inverse(x2 - x1, p)) % p
    x3 = (m ** 2 - x1 - x2) & p
    y3 = (m * (x1 - x3) - y1) % P
    
    return (x3, y3)

def point_doubling(P, a, b, p):
    """
    Performs point doubling on an elliptic curve.

    Parameters:
    - P: the point (x, y) on the elliptic curve
    - a, b: coefficients of the elliptic curve equation
    - p: the prime modulus

    Returns:
    - The result of the point doubling (x, y)
    """
    x1, y1 = P
    
    if y1 == 0:
        return (0, 0)
    
    m = ((3 * x1 ** 2 + a) * mod_inverse(2 * y1, p)) % p
    x3 = (m ** 2 - 2 * x1) % p
    y3 = (m * (x1 - x3) - y1) % p
    
    return (x3, y3)

def ecdh(p, a, b, P):
    """
    Performs the Elliptic Curve Diffie-Hellman Key Exchange.

    Parameters:
    - p: the prime modulus
    - a, b: coefficients of the elliptic curve equation
    - P: the base point (x, y) on the elliptic curve

    Returns:
    - The shared secret key (x, y) on the elliptic curve
    """
    # Alice's private and public keys
    a_private = random.randint(2, p - 2)
    A_public = double_and_add(P, a_private, a, b, p)
    
    # Bob's private and public keys
    b_private = random.randint(2, p - 2)
    B_public = double_and_add(P, b_private, a, b, p)
    
    # The secret key computed by Alice
    T_AB = double_and_add(B_public, a_private,a, b, p)
    # The secret key computed by Bob
    T_BA = double_and_add(A_public, b_private, a, b, p)
    
    assert T_AB == T_BA
    
    return T_AB

def main():
    # Choose a prime p and the elliptic curve parameters a, b
    p = 2**256 - 2**224 + 2**192 + 2**96 - 1
    a = -3
    b = 41058363725152142129326129780047268409114441015993725554835256314039467401291
    
    # Choose a private element P = (x_p, y_p)
    x_p = 48439561293906451612451812245956901550880174394880157880096106384 
    y_p = 36134677641873308953988598641663524294515194642976523804497193542
    
    P = (x_p, y_p)
    
    if is_curve_valid(a, b, p):
        print("The Curve is valid")
        
    if is_point_on_curve(P, a, b, p):
        print(f"Point {P} is on the elliptic curve")
        
    # Perform the Elliptic curve Diffie-Hellman Key Exchange
    joint_secret = ecdh(p, a, b, P)
    print(f"Joint secret: {joint_secret}")

if __name__ == "__main__":
    main()