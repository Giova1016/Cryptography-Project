def square_and_multiply(x, H, n):
    r = x
    for bit in reversed(bin(H)[2:]):
        if bit == '1':
            r = (r * x) % n
        x = (x * x) % n
        
    return r

if __name__ == "__main__":
    base = 7
    exponent = 640
    modulus = 990
    
    result= square_and_multiply(base, exponent, modulus)
    print(f"{base}^{exponent} mod {modulus} = {result}")