from sympy import randprime, mod_inverse
import random
from math import gcd


# generates q and alpha
def generate_q_and_alpha():
    q = randprime(50, 100)
    alpha = random.choice(primRoots(q))
    return q, alpha


# finds primitive roots of modulo
def primRoots(modulo):
    required_set = {num for num in range(1, modulo) if gcd(num, modulo)}
    return [g for g in range(1, modulo) if required_set == {pow(g, powers, modulo)
                                                            for powers in range(1, modulo)}]


class Sender:

    def encrypt(self, M, receiver_public_key):
        # k:random integer 1 <= k <= q-1
        q, alpha, Y = receiver_public_key
        k = random.randint(1, q-1)

        # One time key, K = Y^k mod q
        K = (Y ** k) % q

        C1 = (alpha ** k) % q
        C2 = (K * M) % q
        return C1, C2


class Receiver:

    def __init__(self):

        X = random.randint(2, q-1)
        Y = (alpha ** X) % q

        self.public_key = (q, alpha, Y)
        self.private_key = X

    def decrypt(self, C1, C2):
        q, _, _ = self.public_key
        X = self.private_key

        K = (C1 ** X) % q
        K_inv = mod_inverse(K, q)
        M = (C2 * K_inv) % q

        return M


if __name__ == "__main__":
    q, alpha = generate_q_and_alpha()

    Bob = Sender()
    Alice = Receiver()

    print('Bob is sender')
    print('Alice is receiver')
    print()
    print('public key of Alice (q, alpha, Y): ', Alice.public_key)
    print('private key of Alice: ', Alice.private_key)
    print()

    try:
        print("q = ", q)
        print()
        # 0 <= M <= q-1
        M = int(input('Enter an integer M in the range 0 <= M < ' + str(q) + ": "))
        if M < 0 or M >= q:
            raise ValueError('invalid input')

        C1, C2 = Bob.encrypt(M, Alice.public_key)

        print("Message encrypted by Bob (C1 C2): ", (C1, C2))
        print()

        _M = Alice.decrypt(C1, C2)
        print("Message decrypted by Alice: ", _M)

    except ValueError as error:
        print(error)
