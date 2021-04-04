'''
Write a program that can perform a letter frequency attack on any monoalphabetic
substitution cipher. Your program should produce top-k possible plaintexts corresponding
to the given ciphertext. You can use hamming distance (not mandatory, you can use other
measures) to find the similarity between plaintext and ciphertext.
'''
from itertools import permutations
import random
from string import ascii_lowercase

#relative frequency of letters in english alphabet
fr = [('a', 8.2), ('b', 1.5),('c', 2.8),('d', 4.3),('e', 13),('f', 2.2),('g', 2), ('h', 6.1),('i', 7),('j',0.15),('k',0.77),('l',4),('m',2.4), ('n',6.7),('o',7.5),('p',1.9),('q',0.095),('r',6),('s',6.3),('t',9.1),('u',2.8),('v',0.98),('w',2.4),('x',0.15),('y',2),('z',0.074)]
fr.sort(key = lambda x : x[1], reverse = True) #sorting characters on the basis of relative frequencies

key = list(ascii_lowercase)
random.shuffle(key) #random permutation of alphabets

def substitution_cipher_encryption(plaintext):
    plaintext = plaintext.lower()
    ciphertext = ''
    for ch in plaintext:
        i = ord(ch) - ord('a')
        ciphertext += key[i]
    return ciphertext

def substitution_cipher_decryption(ciphertext):
    ciphertext = ciphertext.lower()
    decrypted_text = ''
    for ch in ciphertext:
        i = key.index(ch)
        decrypted_text += chr(i + ord('a'))
    return decrypted_text

def hamming_distance(text1, text2):
    h_d = 0
    for i in range(len(text1)):
        if text1[i] != text2[i]:
            h_d += 1
    return h_d

def top_k_possible_plaintexts(plaintext,ciphertext, k):
    freq = {}

    for ch in ciphertext:
        if not ch in freq.keys():
            freq[ch] = 1
        else:
            freq[ch] += 1
            
    freq = [(k, v) for k, v in freq.items()]
    freq.sort(key = lambda x : x[1], reverse = True)
    f = fr[:len(freq)]
    
    count = 0
    for perm in permutations(f):
        mapping = {}
        index = 0
        for i in range(len(freq)):
            mapping[freq[i][0]] = perm[i][0]
        
        possible = ''.join([mapping[char] for char in ciphertext])
        print('possible plaintext {}:\n{} '.format(count + 1, possible))
        print('hamming distance: ', hamming_distance(plaintext, possible), '\n')
        
        count += 1
        if count == k:
            break

if __name__ == "__main__":
    plaintext = 'itwasdisclosedyesterdaythatseveralinformationbutdirectcontactshavebeenmadewithpoliticalrepresentativesofthevietconginmoscow'
    ciphertext = substitution_cipher_encryption(plaintext)
    print('Original plaintext: ', plaintext)
    print('Ciphertext: ', ciphertext)
    print('Original length of plaintext: ', len(plaintext))
    print()
    top_k_possible_plaintexts(plaintext, ciphertext, 3)