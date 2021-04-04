#1. Encryption and decryption using Caesar Cipher
from string import ascii_lowercase

def caesar_cipher_encryption(text, key):
    key %= 26 #making key in the range [0-25]
    encrypted_text = ''
    text = text.lower()
    
    for ch in text:
        temp = (ord(ch) - ord('a') + key) % 26 #adding key
        encrypted_text += chr(temp + ord('a'))
    
    return encrypted_text

def caesar_cipher_decryption(text, key):
    key %= 26
    decrypted_text = ''
    text = text.lower()
    
    for ch in text:
        temp = (ord(ch) - ord('a') - key) % 26 #subtracting key
        decrypted_text += chr(temp + ord('a'))
    
    return decrypted_text

if __name__ == "__main__":
    key = 3
    plaintext = ascii_lowercase
    encrypted_text = caesar_cipher_encryption(plaintext, key)
    decrypted_text = caesar_cipher_decryption(encrypted_text, key)

    print('key: ', key, '\n')
    print('Text before encryption:\n', plaintext, '\n')
    print('Text after encryption:\n', encrypted_text, '\n')
    print('Decrypted text:\n', decrypted_text, '\n')