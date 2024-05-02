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

def byte_substitution(state):
    """ 
    Layer that performs byte substitution with the S-box lookup table.
    
    Parameter:
    - state: current state of the data
    
    Returns:
    - Result after byte substitution
    """    
    return [s_box[byte] for byte in state]

def shift_rows(state):
    """
    The first layer of diffusion that performs row shifting.
    
    Parameters:
    - state: curent state of the data
    
    Returns:
    - The shifted rows of the data
    """
    return[state[0], state[4], state[8], state[12],
           state[5], state[9], state[13], state[1],
           state[10], state[14], state[2], state[6],
           state[15], state[3], state[7], state[11]]
    
def mix_columns(state):
    """
    The second layer of diffusion that performs column layer mixing using matrix multiplication.
    
    Parameters:
    - state: current state of the data
    
    Returns:
    - New state after mixing the columns
    """
    matrix = [0x02, 0x03, 0x01, 0x01,
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
    - state: current state of the data
    - round_key: key for the current round
    
    Returns:
    - Result after key addition
    """
    if not round_key:  # Checks if round_key is empty
        return state
    return [state_byte ^ key_byte for state_byte, key_byte in zip(state, round_key)] # does an XOR of the current state of the data and the round key

def gf_multiply(a, b):
    """
    Multiplies two numbers in the Galois Field GF(2^8).
    
    Parameters:
    - a: first number
    - b: second number
    
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

def key_schedule(key):
    """
    Generates the round keys from the master key for encryption.

    Parameters:
    - key: the master key (128-bit, 192-bit, or 256-bit key)

    Raises:
    - ValueError: Raises the exception if the value is not the correct length

    Returns:
    - The list of round keys for encryption
    """
    rcon = [0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]
    key_len = len(key)
    round_keys = []
    rounds = 0

    # Checks the key length and assign the number of rounds accordingly.
    if key_len == 16:
        rounds = 10
    elif key_len == 24:
        rounds = 12
    elif key_len == 32:
        rounds = 14
    else:
        raise ValueError("Invalid key length. Key must be 128, 192 or 256-bit.")
    
    # Initialize the round keys with the master key.
    round_keys.append(key)

    # Generate the remaining round keys.
    for i in range(rounds):
        prev_key = round_keys[-1]
        new_key = [0] * key_len

        # Perform the key schedule algorithm
        for j in range(key_len):
            if j == 0:
                new_key[j] = (s_box[prev_key[(j + 1) % key_len]] ^ prev_key[j] ^ rcon[i])
            elif (key_len > 24) and (j % key_len == 16):
                new_key[j] = (s_box[new_key[j - 1]] ^ prev_key[j])
            else:
                new_key[j] = (new_key[j - key_len] ^ prev_key[j])
        
        round_keys.append(new_key)
    
    return round_keys

def inv_mix_columns(state):
    """
    The second layer of diffusion that performs column layer mixing using matrix multiplication with the inverted matrix.
    
    Parameters:
    - state: current state of the data
    
    Returns:
    - New state after mixing the columns with the inverted matrix
    """
    inv_matrix = [0x0e, 0x0b, 0x0d, 0x09,
                  0x09, 0x0e, 0x0b, 0x0d,
                  0x0d, 0x09, 0x0e, 0x0b,
                  0x0b, 0x0d, 0x09, 0x0e]
    
    new_state = [0] * 16
    for col in range(4):
        for row in range(4):
            total = 0
            for i in range(4):
                total ^= gf_multiply(inv_matrix[row * 4 + i], state[col * 4 + i])
            new_state[col * 4 + row] = total
    
    return new_state

def inv_shift_rows(state):
    """
    The first layer of diffusion that performs inverse row shifting for decryption.
    
    Parameters:
    - state: curent state of the data
    
    Returns:
    - The inverted shifted rows of the data
    """
    return [state[0], state[13], state[10], state[7],
            state[4], state[1], state[14], state[11],
            state[8], state[5], state[2], state[15],
            state[12], state[9], state[6], state[3]]

def inv_byte_substitution(state):
    """ 
    Layer that performs the inverted byte substitution with the S-box lookup table for decryption.
    
    Parameter:
    - state: current state of the data
    
    Returns:
    - Result after inverted byte substitution
    """
    inv_s_box = [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
                 0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
                 0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
                 0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
                 0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
                 0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
                 0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
                 0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
                 0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
                 0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
                 0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
                 0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
                 0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
                 0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
                 0xa0, 0xe0, 0x38, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
                 0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]
    
    return [inv_s_box[byte] for byte in state]

def decryption_key_schedule(key):
    """
    Generates the round keys for decryption by inverting the list containing the encryption round keys.

    Parameters:
    - key: the master key (128-bit, 192-bit, or 256-bit key)

    Returns:
    - The list of round kyes for decryption
    """
    encryption_round_keys = key_schedule(key)
    decryption_round_keys = encryption_round_keys[::-1] # Reverse the list of round keys

    return decryption_round_keys


def aes_encryption(plaintext, round_key):
    """
    Performs the AES algorithm to encrypt the plaintext using the provided key.
    
    Parameters:
    - plaintext: the input message to be encrypted
    - key: the key to be used when encrypting the message

    Raises:
    - ValueError: Raises the exception if the value is not the correct length
    
    Returns:
    - The encrypted ciphertext.
    """  
    key_len = len(round_key)
    rounds = 0

    # Check the key length
    if key_len == 16:
        rounds = 10
    elif key_len == 24:
        rounds = 12
    elif key_len == 32:
        rounds = 14
    else:
        raise ValueError("Invalid key length. Key must be 128-bit, 192-bit, or 256-bit.")
    
    # Generate the round keys
    round_keys = key_schedule(round_key)

    # Initial key addition
    state = key_addition(plaintext, round_keys[0])
    
    # Perform the rounds
    for i in range(1, rounds):
        # Byte substitution
        state = byte_substitution(state)
        
        # Shift rows
        state = shift_rows(state)
        
        # Mix columns (except for the last round)
        if i != rounds - 1:
            state = mix_columns(state)
    
        # Key addition
        state = key_addition(state, round_keys[i])

    # Final round (without mixing columns)
    state = byte_substitution(state)
    state = shift_rows(state)
    state = key_addition(state, round_keys[-1])

    return state

def aes_decryption(ciphertext, key):
    """
    Performs the AES algorithm to decrypt the ciphertext using the provided key.

    Parameters:
    - ciphertext: the inputed ciphertext to be decrypted
    - key: the key to be used when decrypting the message

    Raises:
    - ValueError: Raises the exception if the value is not the correct length

    Returns:
    - The decrypted message
    """
    key_len = len(key)
    rounds = 0

    # Check the key length
    if key_len == 16:
        rounds = 10
    elif key_len == 24:
        rounds = 12
    elif key_len == 32:
        rounds = 14
    else:
        raise ValueError("Invalid key length. Key must be 128-bit, 192-bit, or 256-bit.")
    
    # Generate the round keys
    round_keys = decryption_key_schedule(key)

    # Initial key addition
    state = key_addition(ciphertext, round_keys[0])

    # Perform the rounds
    for i in range(rounds - 1, 0, -1):
        # Inverse shift rows
        state = inv_shift_rows(state)
        
        # Inverse byte substitution
        state = inv_byte_substitution(state)
        
        # Key addition
        state = key_addition(state, round_keys[i])

        # Inverse mix columns (except for the last round)
        if i !=1:
            state = inv_mix_columns(state)

    # Final round(without inverse mix columns)
    state = inv_shift_rows(state)
    state = inv_byte_substitution(state)
    state = key_addition(state, round_keys[-1])

    return state
         
def main():
    # Initialize the plaintext and key
    plaintext = [0xff] * 16 # 128-bit block of all 1's in hex

    # Define the key length (128-bit, 192-bit, or 256-bit)
    key_length = 16 # 128-bit key
    
    # Generate the master key
    master_key = [0xff] * key_length # 128-bit key of all 1's in hex
    
    # Perform the first round of AES
    ciphertext = aes_encryption(plaintext, master_key)
    
    # Uncomment to see the hexadecimal version
    # # Display the encrypted message
    # print("Encrypted message in hexadecimal:")
    # for i in range(4):
    #     print(' '.join(format(ciphertext[i * 4 + j], '02x') for j in range(4)))

    print("\nEncrypted message converted to binary:")
    for i in range(4):
        print(' '.join(format(ciphertext[i * 4 + j], '08b') for j in range(4)))
    
    decrypted_ciphertext = aes_decryption(ciphertext, master_key)

    # Uncomment to see the hexadecimal version
    # Display the decrypted message
    # print("\nDecrypted message in hexadecimal:")
    # for i in range(4):
    #     print(' '.join(format(decrypted_ciphertext[i * 4 + j], '02x') for j in range(4)))
        
    print("\nDecrypted message converted to binary:")
    for i in range(4):
        print(' '.join(format(decrypted_ciphertext[i * 4 + j], '08b') for j in range(4)))    

if __name__=="__main__":
    main()