import random

def gen_key(key):
    # While True:
    generated_key = random.randrange(2 ** key - 1, 2 ** key)
    return generated_key
    # ifisprime(generated_key)
print("Generated key:", gen_key(key = 2048))