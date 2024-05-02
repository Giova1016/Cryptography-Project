def lfsr(initial_state, polynomial_degree, cycles):
    """
    Generates a pseudo-random key using Linea Feedback Shift Register (LFSR). 

    Parameters:
    - initial_state: the initial state of the bits (binary representation)
    - polynomial_degree: the degree of the polynomial that indicates the position of the flip-flops
    - cycles: the number of cycles to be performed in the LFSR

    Returns:
    The Pseudo-random key generated by the LFSR
    """
    state = list(initial_state) # Converts the initial state to a list.
    key = '' # Initialize an empty string to store the key
    
    for _ in range(cycles):
        feedback = int(state[-1]) # Assigns the variable 'feedback' the Right most bit.
        for i in range (1, polynomial_degree):
            feedback ^= int(state[-(i + 1)]) # Performs XOR operation for feedback from other flip-flops
        state.pop() # Removes the rightmost bit
        state.insert(0, str(feedback)) # Inserts the feedback bit at the beginning.
        key += state[-1] # Appends the rightmost bit to key.
    
    return key

def main():
    # Example values
    initial_state = "1011010" # Initial state of the bits
    polynomial_degree = 5 # Degree of the polynomial
    cycles = 10 # Number of cycles

    initial_state2 = "0101101" # Initial state of the bits
    polynomial_degree2 = 4 # Degree of the polynomial
    cycles2 = 15 # Number of cycles

    generated_key = lfsr(initial_state, polynomial_degree, cycles)
    print(f"\nGenerated key after {cycles} cycles:", generated_key)

    generated_key2 = lfsr(initial_state2, polynomial_degree2, cycles2)
    print(f"\nGenerated key after {cycles2} cycles:", generated_key2)
    
if __name__ == "__main__":
    main()
