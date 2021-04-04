#2. Encryption and decryption using Hill Cipher
import numpy as np

#converts string into array where characters [a-z] are mapped to [0-25]
def str_to_arr(x):
    return np.array([ord(char)-ord('a') for char in x])


#converts array to string where integers [0-25] are mapped to [a-z]
def arr_to_str(x):
    x = [chr(i + 97) for i in x]
    return ''.join(x)
   
#finds the modular multiplicative inverse of n with respect to m
def mod_inverse(n, m):
    for i in range(m):
        if (n * i) % m == 1:
            return i


def hill_cipher_encryption(text, key):
    
    n = np.sqrt(len(key))
    if n != int(n):
        raise KeyError('key length should be perfect square')
    n = int(n)
    text = text.lower()
    
    #constructing key matrix
    arr = str_to_arr(key)
    K = np.array(arr).reshape(n, n)
    
    #if text is not multiple of n, we append extra characters
    if (len(text)%n) != 0:
        text += (n - len(text)%n) * 'x'
    
    #dividing text into plaintexts of size n
    text = str_to_arr(text)
    arr = [text[i:i+n] for i in range(0, len(text), n)]
    
    result = ''
    for P in arr:
        C = (P @ K) % 26
        result += arr_to_str(C)
    return result

def hill_cipher_decryption(text, key):
    n = np.sqrt(len(key))
    
    if n != int(n):
        raise KeyError('key length should be perfect square')
        
    n = int(n)
    text = text.lower()
    arr = str_to_arr(key)
    K = np.array(arr).reshape(n, n)
    

    d = np.linalg.det(K) #determinant
    d_inv = mod_inverse(np.round(d), 26)
    adj = np.round(d * np.linalg.inv(K)) #adjoint of matrix
    K_inv = np.array(d_inv * adj, dtype = int) #inverse of matrix
    
    text = str_to_arr(text)
    arr = [text[i:i+n] for i in range(0, len(text), n)]
    result = ''
    for C in arr:
        P = (C @ K_inv) % 26
        result += arr_to_str(P)
    return result


if __name__ == "__main__":
    plaintext = 'paymoremoney'
    key = 'rrfvsvcct'
    '''
    17 17 5
    21 18 21
    2 2 19
    '''
    encrypted_text = hill_cipher_encryption(plaintext, key)
    decrypted_text = hill_cipher_decryption(encrypted_text, key)

    print('key: ', key, '\n')
    print('Text before encryption:\n', plaintext, '\n')
    print('Text after encryption:\n', encrypted_text, '\n')
    print('Decrypted text:\n', decrypted_text, '\n')