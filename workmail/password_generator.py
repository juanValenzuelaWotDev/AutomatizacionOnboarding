import random
import string

# Standard that we use in wot dev
# Reference: https://pynative.com/python-generate-random-string/
# The choice() method can repeat characters.
# If you don’t want repeated characters in a resultant string, then use the random.sample() method.
'''
Random password
16 characters long
Includes:
special characters
lowercase
uppercase
numbers
'''

def generate_password(length):
    print("Generating random password")
    # choose from all lowercase, uppercase, digits and special characters options
    letters = string.ascii_letters + string.digits + "!@$#%&/()=++*~"
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Generated password of length", length)
    return result_str

# Generates a random string from any length
def get_random_string(length):
    # choose from all lowercase, uppercase, digits and special characters options
    letters = string.ascii_letters + string.digits + "!@$#%&/()=++*~"
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)



