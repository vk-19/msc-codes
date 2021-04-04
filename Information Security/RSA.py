from math import gcd
from sympy import *
from random import randint


def RSA_encryption(M, public_key):
    e, n = public_key

    C = (M ** e) % n
    return C


def RSA_decryption(C, private_key):
    d, n = private_key

    M = (C ** d) % n

    return M


def generate_keys():
    p = randprime(100, 1000)
    q = randprime(100, 1000)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    # 1 < e < phi_n
    e = randint(2, phi_n-1)
    while gcd(e, phi_n) != 1:
        e = randint(2, phi_n-1)

    d = mod_inverse(e, phi_n)

    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key


if __name__ == "__main__":
    public_key, private_key = generate_keys()
    _, n = public_key

    # 1 < M < n

    print('public key (e, n): ', public_key)
    print('private key (d, n): ', private_key)

    try:
        M = int(input('Enter a positive integer less than ' + str(n) + ': '))
        if M >= n or M <= 1:
            raise ValueError('invalid number entered')
        C = RSA_encryption(M, public_key)
        print('encrypted message:', C)
        P = RSA_decryption(C, private_key)
        print('decrypted message:', P)

    except ValueError as error:
        print(error)
