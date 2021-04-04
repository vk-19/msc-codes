from sympy import randprime
import random
from math import gcd

q = randprime(100, 1000)

# finds primitive roots of modulo
def primRoots(modulo):
    required_set = {num for num in range(1, modulo) if gcd(num, modulo)}
    return [g for g in range(1, modulo) if required_set == {pow(g, powers, modulo)
                                                            for powers in range(1, modulo)}]


alpha = random.choice(primRoots(q))
X_A = random.randint(1, q-1)
X_B = random.randint(1, q-1)

Y_A = (alpha ** X_A) % q
Y_B = (alpha ** X_B) % q

# secret key calculation by Alice
K_A = (Y_B ** X_A) % q

# secret key calculation by Bob
K_B = (Y_A ** X_B) % q

print("(q, alpha): ", (q, alpha))
print()

print('private key of Alice: ', X_A)
print('public key of Alice: ', Y_A)
print()

print('private key of Bob: ', X_B)
print('public key of Bob: ', Y_B)
print()

print('shared key calculated by Alice: ', K_A)
print('shared key calculated by Bob: ', K_B)
print()

if K_A == K_B:
    print('key exchange is successful between Alice and Bob')
else:
    print('error in key exchange process')
