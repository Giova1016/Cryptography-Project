def initial_permutation(block):
    """
    Layer that performs the initial permutation on the block of plaintext.

    Parameters:
    - block (list): The block of plaintext provided.

    Returns:
    - The block of plaintext after permutation.
    """
    initial_permute_table = [58, 50, 42, 34, 26, 18, 10, 2,
                             60, 52, 44, 36, 28, 20, 12, 4,
                             62, 54, 46, 38, 30, 22, 14, 6,
                             64, 56, 48, 40, 32, 24, 16, 8,
                             57, 49, 41, 33, 25, 17, 9, 1,
                             59, 51, 43, 35, 27, 19, 11, 3,
                             61, 53, 45, 37, 29, 21, 13, 5,
                             63, 55, 47, 39, 31, 23, 15, 7]
    
    permuted_pt_block = [block[i - 1] for i in initial_permute_table]
    return permuted_pt_block

def final_permutation(block):
    """
    Layer that performs the final permutation oo the block of ciphertext. 

    Parameters:
    - block (list): The block of ciphertext provided.

    Returns:
    - The block of ciphertext after permutation.
    """
    final_permute_table = [40, 8, 48, 16, 56, 24, 64, 32,
                           39, 7, 47, 15, 55, 23, 63, 31,
                           38, 6, 46, 14, 54, 22, 62, 30,
                           37, 5, 45, 13, 53, 21, 61, 29,
                           36, 4, 44, 12, 52, 20, 60, 28,
                           35, 3, 43, 11, 51, 19, 59, 27,
                           34, 2, 42, 10, 50, 18, 58, 26,
                           33, 1, 41, 9, 49, 17, 57, 25]
    
    permuted_ct_block = [block[i - 1] for i in final_permute_table]
    return permuted_ct_block

def key_schedule(key):
    """
    Generates the key schedule from the original 64-bit key.

    Parameters:
    - key (list): The original key to generate the 16 keys for the rounds. 

    Returns:
    - The list containing the keys for the 16 rounds. 
    """
    pc1_table = [57, 49, 41, 33, 25, 17, 9, 1,
                 58, 50, 42, 34, 26, 18, 10, 2,
                 59, 51, 43, 35, 27, 19, 11, 3,
                 60, 52, 44, 36, 63, 55, 47, 39,
                 31, 23, 15, 7, 62, 54, 46, 38,
                 30, 22, 14, 6, 61, 53, 45, 37,
                 29, 21, 13, 5, 28, 20, 12, 4]
    
    pc2_table = [14, 17, 11, 24, 1, 5, 3, 28,
                 15, 6, 21, 10, 23, 19, 12, 4,
                 26, 8, 16, 7, 27, 20, 13, 2,
                 41, 52, 31, 37, 47, 55, 30, 40,
                 51, 45, 33, 48, 44, 49, 39, 56,
                 34, 53, 46, 42, 50, 36, 29, 32]
    
    key_shifts = [1, 1, 2, 2, 2, 2, 2, 2, 
                  1, 2, 2, 2, 2, 2, 2, 1]
    
    # Initialize an empty list for the round keys
    round_keys = []

    # Permute the original key using the PC-1 lookup table.
    key = [key[pc1_table[i] - 1] for i in range(56)]

    # Split the key into two halves.
    left_key = key[:28]
    right_key = key[28:]
    
    # Generate the 16 round keys.
    for shift in key_shifts:
        # Rotate the two halves
        left_key = left_key[shift:] + left_key[:shift]
        right_key = right_key[shift:] + right_key[:shift]

        # Combine the two halves.
        combined_key = left_key + right_key

        # Permute using the PC-2 lookup table.
        round_key = [combined_key[pc2_table[i] - 29] for i in range(48)]
        
        round_keys.append(round_key)

def reversed_key_schedule(key):
    """
    Generates the reversed key schedule for the 16 rounds.

    Parameters:
    - key (list): The original key to generate the 16 keys for the decryption rounds.

    Returns:
    - The list containing the reversed key order for decrypting in the 16 rounds. 
    """
    round_keys = key_schedule(key)
    reversed_keys = round_keys[::-1] # Reverses the list of round keys

    # Adjust the rotations for decryption
    for i in range(1, 16, 3):
        reversed_key_schedule[i] = reversed_keys[i][-3:] + reversed_keys[:-3]
    return reversed_keys

def expansion_e(block):
    """
    Increases the diffusion in the DES algorithm.

    Parameters:
    - block (list): The right half of the initial permutation.

    Returns:
    - The expanded right half of the initial permutation.
    """
    expansion_table = [32, 1, 2, 3, 4, 5, 
                       4, 5, 6, 7, 8, 9, 
                       8, 9, 10, 11, 12, 13, 
                       12, 13, 14, 15, 16, 17, 
                       16, 17, 18, 19, 20, 21, 
                       20, 21, 22, 23, 24, 25, 
                       24, 25, 26, 27, 28, 29, 
                       28, 29, 30, 31, 32, 1]
    
    expanded_block = [block[i - 1] for i in expansion_table]
    return expanded_block

def xor(block, key):
    """
    Does an XOR between the expanded right half and the round key.

    Parameters:
    - block (list): The output of the expansion function.
    - key (list): The key for the round.

    Returns:
    - The XOR between the output of the expansion function and the round key. 
    """
    return [b1 ^ b2 for b1, b2 in zip(block, key)]

def s_box_substitution(block):
    """
    The S-boxes are the most crucial elements of DES because they introduce a non-linearity to the cipher.
    They are a lookup table that maps a 6-bit input to a 4-bit output.

    Parameters:
        block (list): The output of the expansion function E.

    Returns:
    - The ciphertext after being put through the nonlinear S-boxes.  
    """
    s_boxes = [
        [ # S-box S_1
            [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
            [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
            [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
            [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
        [ # S-box S_2
            [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
            [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
            [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
            [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
        [ # S-box S_3
            [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
            [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
            [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
            [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
        [# S-box S_4
            [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
            [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
            [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
            [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
        [ # S-box S_5
            [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
            [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
            [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
            [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
        [ # S-box S_6
            [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
            [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
            [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
            [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
        [ # S-box S_7
            [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
            [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
            [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
            [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
        [ # S-box S_8
            [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
            [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
            [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
            [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

    substituted_block =[]
    for i in range(8):
        s_box = s_boxes[i]
        row = (block[i * 6] << 1) + block[i * 6 + 5]
        column = (block [i * 6 + 1] << 3) + (block [i * 6 + 2] << 2) + (block[i * 6 + 3] << 1) + block[i * 6 + 4]
        value = s_box[row][column]
        substituted_block.extend([int(bit) for bit in format(value, '04b')])
    return substituted_block

def permutation_p(block):
    """
    Does a bitwise permutation to introduce more diffusion.

    Parameters:
    - block (list): The output block from the S-boxes.

    Returns:
    - The ciphertext after being put through the permutation P function.
    """
    permutation_table = [16, 7, 20, 21, 29, 12, 28, 17,
                         1, 15, 23, 26, 5, 18, 31, 10,
                         2, 8, 24, 14, 32, 27, 3, 9,
                         19, 13, 30, 6, 22, 11, 4, 25]
    
    permuted_block = [block[i - 1] for i in permutation_table]
    return permuted_block
    
def des_feistel_network(block, round_key):
    left_half = block[:32]
    right_half = block[32:]
    """ F-function """
    expanded_right = expansion_e(right_half)
    xor_result = xor(expanded_right, round_key)
    substituted = s_box_substitution(xor_result)
    permuted = permutation_p(substituted)
    new_right_half = xor(left_half, permuted)
    return right_half + new_right_half

def des_block_processing(block, keys):
    """
    Does the permutations for each round of the DES feistel network.

    Parameters:
    - block (list): The block to be proccesed on each round of encryption and decryption.
    - keys (list): The key for the round.

    Returns:
    - The block of text that has been procccesed after each round.
    """
    block = initial_permutation(block)
    for round_key in keys:
        block = des_feistel_network(block, round_key)
    block = block[32:] + block[:32] # Swap the halves before permutation
    block = final_permutation(block)
    return block

def des_encrypt(plaintext, key):
    """
    The entire run of the DES algorithm that will be used to encrypt the plaintext block.

    Parameters:
    - plaintext (list): The plaintext to be encrypted in the DES algorithm.
    - key (list): The key that will be used to generate the key schedule for the rounds.

    Returns:
    -  The ciphertext after going through the DES algorithm.
    """
    keys = key_schedule(key)
    ciphertext = []
    for block in plaintext:
        encrypted_block = des_block_processing(block, keys)
        ciphertext.extend(encrypted_block)
    return ciphertext

def des_decrypt(ciphertext, key):
    """
    The entire run of the DES algorithm that will be used to decrypt the ciphertext block.

    Parameters:
    - ciphertext (list): The ciphertext to be decrypted in the DES algorithm.
    - key (list):  The key that will be used to generate the reversed key schedule for the rounds.

    Returns:
    - The decrypted text after going through the DES algorithm.
    """
    keys = reversed_key_schedule(key)
    plaintext = []
    for block in ciphertext:
        decrypted_block = des_block_processing(block, keys)
        plaintext.extend(decrypted_block)
    return plaintext

def main():
    # 64 bit Plaintext as example for an input 
    plaintext = [[0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1,  
                  1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1,  # First 64-bit block
                  1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1,  
                  0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1],
                 
                 [0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1,  
                  1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1,  # Second 64-bit block
                  0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1,  
                  1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1],

                 [1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1,  
                  0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1,  # Third 64-bit block
                  1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1,  
                  0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1]]
    
    # Split the plaintext into 64-bit block
    plaintext_blocks = [plaintext[i:i + 64] for i in range(0, len(plaintext), 64)]
    
    # 64 bit key as example for an input 
    key = [1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0,
           1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1,
           1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0,
           1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1]
    
    ciphertext_blocks = []
    for block in plaintext_blocks:
        encrypted_blocks = des_encrypt(block, key)
        ciphertext_blocks.extend(encrypted_blocks)

    print("Ciphertext:", ciphertext_blocks)

    decrypted_blocks = []
    for block in ciphertext_blocks:
        decrypted_block = des_decrypt(block, key)
        decrypted_blocks.extend(decrypted_block)
    print("Decrypted ciphertext:", decrypted_blocks)

if __name__ == "__main__":
    main()
