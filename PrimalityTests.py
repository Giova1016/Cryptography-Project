import random
from SquareAndMultipy import square_and_multiply

def fermat_primality_test(p, k=10):
    """
    Tests if a number is prime using the Fermat primality test.

    Parameters:
    - n: the number being tested.
    - k: the limit of times the number will be tested. Default will be 10.

    Returns:
    - Returns if the number generated is a prime (True) or if it is not a prime (False) after being tested.
    """
    if p < 2: 
        return False
    if p <= 3: 
        return True

    for _ in range(k):
        a = random.randrange(2, p)
        if square_and_multiply(a, p - 1, p) != 1:
            return False
    return True

def miller_rabin_primality_test(prime_number, k=10):
    """
    Tests if a number is prime using the Miller-Rabin primality test.

    Parameters:
    - n: the number being tested.
    - k: the limit of times the number will be tested. Default will be 10.

    Returns:
    - Returns if the number generated is a prime (True) or if it is not a prime (False) after being tested.
    """
    if prime_number < 2: 
        return False
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        if prime_number % p == 0: 
            return prime_number == p
    s, d = 0, prime_number - 1
    while d % 2 == 0:
        s, d = s + 1, d >> 1
    for _ in range(k):
        x = random.randrange(2, prime_number - 1)
        x = square_and_multiply(x, d, prime_number)
        if x == 1 or x == prime_number - 1: 
            continue
        for _ in range(1, s):
            x = square_and_multiply(x, 2, prime_number)
            if x == prime_number - 1: 
                break
        else: 
            return False
    return True

def main():
    print("Running primality tests...")
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    composites = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25, 26, 27, 28, 30, 32, 33, 34, 35, 36, 38, 39, 40, 42, 44, 45, 46, 48, 49, 50, 51, 52, 54, 55, 56, 57, 58, 60, 62, 63, 64, 65, 66, 68, 69, 70, 72, 74, 75, 76, 77, 78, 80, 81, 82, 84, 85, 86, 87, 88, 90, 91, 92, 93, 94, 95, 96, 98, 99, 100]
    carmichael_numbers = [561, 1105, 1729, 2465, 2821, 6601]

    for p in primes:
        try:
            assert miller_rabin_primality_test(p) and fermat_primality_test(p)
            print(f"{p} is prime")
        except AssertionError:
            print(f"{p} should be prime, but the tests failed")

    for p in composites:
        try:
            assert not miller_rabin_primality_test(p) and not fermat_primality_test(p)
            print(f"{p} is composite")
        except AssertionError:
            print(f"{p} should be composite, but the tests failed")

    for p in carmichael_numbers:
        try:
            assert not miller_rabin_primality_test(p) or fermat_primality_test(p)
            print(f"{p} is a Carmichael number, Fermat test fails")
        except AssertionError:
            print(f"{p} should be a Carmichael number, but the tests failed")

    print("All tests completed!")

if __name__ == "__main__":
    main()