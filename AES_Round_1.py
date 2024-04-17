def byte_substitution(state):
    """ 
    Layer that performs byte substitution with the S-box lookup table.
    
    Parameter:
    - state: Current state of the data.
    
    Returns:
    - Result after byte substitution.
    """
    s_box = [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
             0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
             0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
             0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
             0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
             0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
             0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
             0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
             0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
             0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
             0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
             0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
             0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
             0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
             0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
             0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
    
    return [s_box[byte] for byte in state]

def shift_rows(state):
    """
    The first layer of diffusion that performs row shifting.
    
    Parameters:
    - state: Curent state of the data.
    
    Returns:
    - The shifted rows of the data.
    """
    return[state[0],  state[4],  state[8],  state[12],
           state[5],  state[9],  state[13], state[1],
           state[10], state[14], state[2],  state[6],
           state[15], state[3],  state[7],  state[11]]
    
def mix_columns(state):
    """
    The second layer of diffusion that performs column layer mixing using matrix multiplication.
    
    Parameters:
    - state: Current state of the data.
    
    Returns:
    - New state after mixing the columns.
    """
    matrix =[0x02, 0x03, 0x01, 0x01,
             0x01, 0x02, 0x03, 0x01, 
             0x01, 0x01, 0x02, 0x03,
             0x03, 0x01, 0x01, 0x02]
    
    new_state = [0] * 16
    for col in range(4):
        for row in range(4):
            total = 0
            for i in range(4):
                total ^= gf_multiply(matrix[row * 4 + i], state[col * 4 + i])
            new_state[col * 4 + row] = total
    
    return new_state

def key_addition(state, round_key):
    """
    Layer that performs key addition.
    
    Parameters:
    - state: Current state of the data.
    - round_key: Key for the current round.
    
    Returns:
    - Result after key addition.
    """
    if not round_key:  # Checks if round_key is empty
        return state
    return [state_byte ^ key_byte for state_byte, key_byte in zip(state, round_key)] # does an XOR of the current state of the data and the round key

def gf_multiply(a, b):
    """
    Multiplies two numbers in the Galois Field GF(2^8).
    
    Parameters:
    - a: first number.
    - b: second number.
    
    Returns:
    - Result after multiplying two numbers in the Galois Field
    """
    result = 0
    while a and b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x11B # XOR the irreducible polynomial x^8 + x^4 + x^3 + x + 1
        b >>= 1
    return result

def aes_first_round(plaintext, round_key):
    """
    Performs the first round of AES.
    
    Parameters:
    - plaintext: the input message to be encrypted.
    - key: the key of this round to encrypt the message.
    
    Returns:
    - The encrypted message after performing AES.
    """  
    # Key addition layer
    state = key_addition(plaintext, round_key)
    
    # Byte substitution layer
    state = byte_substitution(state)
    
    """ Diffusion Layer """
    # Shift row
    state = shift_rows(state)
    
    # Mix column
    state = mix_columns(state)
    """ Diffusion Layer """
    
    """Calculating round key 1 manually"""
    # W[3] = 1111 1111 1111 1111 1111 1111 1111 1111
    # rotate, but stays the same
    # bytewise with S-box
    # 1111 = (FF)_hex -> S-box -> (1C)_hex = 1100
    # W[3] after S-box = 0001 1100 0001 1100 0001 1100 0001 1100 
    # left most byte xor 0000 0001
    # W[3] -> g function  
    #      = 0001 1101 0001 1100 0001 1100 0001 1100
    # W[0] = 1111 1111 1111 1111 1111 1111 1111 1111
    
    # W[4] = 1110 0010 1110 0011 1110 0011 1110 0011 = 0xe2 0xe3 0xe3 0xe3
    #        1111 1111 1111 1111 1111 1111 1111 1111
    # W[5] = 0001 1101 0001 1100 0001 1100 0001 1100 = 0x1d 0x1c 0x1c 0x1c
    #        1111 1111 1111 1111 1111 1111 1111 1111
    # W[6] = 1110 0010 1110 0011 1110 0011 1110 0011 = 0xe2 0xe3 0xe3 0xe3
    #        1111 1111 1111 1111 1111 1111 1111 1111
    # W[7] = 0001 1101 0001 1100 0001 1100 0001 1100 = 0x1d 0x1c 0x1c 0x1c
    
    W4 = [0xe2, 0xe3, 0xe3, 0xe3]
    
    W5 = [0x1d, 0x1c, 0x1c, 0x1c]
    
    W6 = [0xe2, 0xe3, 0xe3, 0xe3]
    
    W7 = [0x1d, 0x1c, 0x1c, 0x1c]
    
    round_key_1 = W4 + W5 + W6 + W7
    
    # Key addition layer (with round key 1)
    state = key_addition(state, round_key_1)

    return state

def main():
    # Initialize the plaintext and key
    plaintext = [0xff] * 16 # 128-bit block of all 1's in hex
    round_key = [0xff] * 16 # 128-bit key of all 1's in hex
    
    # Perform the first round of AES
    result = aes_first_round(plaintext, round_key)
    
    # Display the result
    print("Result of the first round of AES in hexadecimal:")
    for i in range(4):
        print(" ".join(format(result[i * 4 + j], '02x') for j in range(4)))
    
    print("Result of the first round of AES converted to binary:")
    for i in range(4):
        print(" ".join(format(result[i * 4 + j], '08b') for j in range(4)))
        
    print("Result of the first round of AES converted to binary with spacing:")
    for i in range(4):
        binary_row = ''.join(format(result[i * 4 + j], '08b') for j in range(4))
        binary_row_spaced = ' '.join(binary_row[k:k+4] for k in range(0, len(binary_row), 4))
        print(binary_row_spaced)

if __name__=="__main__":
    main()