import random

# Fungsi untuk menghitung GCD
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Fungsi untuk menghitung modular inverse
def mod_inverse(e, phi):
    for d in range(1, phi):
        if (e * d) % phi == 1:
            return d
    return None

# Fungsi untuk menghasilkan pasangan kunci RSA
def generate_rsa_keys():
    p = 61  # Bilangan prima 1
    q = 53  # Bilangan prima 2
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 3
    while gcd(e, phi) != 1:
        e += 2

    d = mod_inverse(e, phi)
    return ((e, n), (d, n))  # Public key dan Private key

# Fungsi untuk enkripsi dengan RSA
def rsa_encrypt(public_key, plaintext):
    e, n = public_key
    ciphertext = [pow(ord(char), e, n) for char in plaintext]
    return ciphertext

# Fungsi untuk dekripsi dengan RSA
def rsa_decrypt(private_key, ciphertext):
    d, n = private_key
    plaintext = ''.join([chr(pow(char, d, n)) for char in ciphertext])
    return plaintext
  