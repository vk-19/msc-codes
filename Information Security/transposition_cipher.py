#3. Encryption and decryption using Transposition Cipher.
import numpy as np

def transposition_cipher_encryption(text, key):
    key = np.array(key) - 1
    text = text.lower()
    n = len(key) #columns
    m = int(np.ceil(len(text) / n)) #rows
    temp = (m * n) - len(text) #extra elements
    text += int(temp) * 'x' #concatenating x if extra elements required to fill the matrix
    
    arr = list(text) #converting text in matrix
    matrix = np.array(arr).reshape(m, n)
    result = np.empty((m, n), dtype = str)
    result[:, key] = matrix
    return ''.join(result.T.flatten().tolist())
    
    

def transposition_cipher_decryption(text, key):
    key = np.array(key) - 1
    text = text.lower()
    n = len(key)
    m = int(len(text) / n)
    arr = list(text)
    arr = np.array([arr[i:i+m] for i in range(0, len(text), m)])
    return ''.join(arr[key].T.flatten())
    

if __name__ == "__main__":
    plaintext = 'attackpostponeduntiltwoam'
    key = [4, 3, 1, 2, 5, 6, 7]
    encrypted_text = transposition_cipher_encryption(plaintext, key)
    decrypted_text = transposition_cipher_decryption(encrypted_text, key)

    print('key: ', key, '\n')
    print('Text before encryption:\n', plaintext, '\n')
    print('Text after encryption:\n', encrypted_text, '\n')
    print('Decrypted text:\n', decrypted_text, '\n')