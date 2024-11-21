import random
from math import gcd

def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(num**0.5) + 1):
            if num % i == 0:
                return False
        return True

# Generate RSA keys
def generate_rsa_keys():

    def generate_prime():
        while True:
            p = random.randint(100, 999)
            if is_prime(p):
                return p

    p = generate_prime()
    q = generate_prime()
    while p == q:
         q = generate_prime()

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.choice([x for x in range(2, phi) if gcd(x, phi) == 1])
    d = pow(e, -1, phi)
    return (e, n), (d, n)

def encrypt_rsa(message, public_key):
    e, n = public_key
    return ' '.join([str(pow(ord(char), e, n)) for char in message])

def decrypt_rsa(encrypted_message, private_key):
    d, n = private_key
    return ''.join([chr(pow(int(char), d, n)) for char in encrypted_message.split()])
