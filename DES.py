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
    
    premuted_pt_block = [block[i - 1] for i in initial_permute_table]
    return premuted_pt_block

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
    _summary_

    Parameters:
    - key (list): _description_

    Returns:
    - _description_
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
    
    round_keys = []
    key = [key[i - 1] for i in pc1_table]
    left_key = key[:28]
    right_key = key[28:]
    for i in range(16):
        left_key = left_key[key_shifts[i]:] + left_key[:key_shifts[i]]
        right_key = right_key[key_shifts[i]:] + right_key[:key_shifts[i]]
        round_key = [left_key[i] for i in pc2_table] + [right_key[i] for i in pc2_table]
        round_keys.append(round_key)
    return round_keys
