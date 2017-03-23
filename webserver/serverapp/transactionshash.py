#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Crypto.Random
from Crypto.Cipher import AES
import hashlib


# salt size in bytes
SALT_SIZE = 16
    
# number of iterations in the key generation
NUMBER_OF_ITERATIONS = 20
    
# the size multiple required for AES
AES_MULTIPLE = 16

class TransctionHash(object):
    """docstring for TransctionHash"""
    def __init__(self, **kwargs):
        super(TransctionHash, self).__init__(**kwargs)
    
    def generate_key(self, password, salt, iterations):
        assert iterations > 0
    
        key = password + salt
    
        for i in range(iterations):
            key = hashlib.sha256(key).digest()  
    
        return key
    
    def pad_text(self, text, multiple):
        extra_bytes = len(text) % multiple
    
        padding_size = multiple - extra_bytes
    
        padding = chr(padding_size) * padding_size
    
        padded_text = text + padding
    
        return padded_text
    
    def unpad_text(self, padded_text):
        padding_size = ord(padded_text[-1])
    
        text = padded_text[:-padding_size]
    
        return text
    
    def encrypt(self, plaintext, password):
        salt = Crypto.Random.get_random_bytes(SALT_SIZE)
    
        key = self.generate_key(password, salt, NUMBER_OF_ITERATIONS)
    
        cipher = AES.new(key, AES.MODE_ECB)
    
        padded_plaintext = self.pad_text(plaintext, AES_MULTIPLE)
    
        ciphertext = cipher.encrypt(padded_plaintext)
    
        ciphertext_with_salt = salt + ciphertext
    
        return ciphertext_with_salt
    
    def decrypt(self, ciphertext, password):
        salt = ciphertext[0:SALT_SIZE]
    
        ciphertext_sans_salt = ciphertext[SALT_SIZE:]
    
        key = self.generate_key(password, salt, NUMBER_OF_ITERATIONS)
    
        cipher = AES.new(key, AES.MODE_ECB)
    
        padded_plaintext = cipher.decrypt(ciphertext_sans_salt)
    
        plaintext = self.unpad_text(padded_plaintext)
    
        return plaintext


if __name__ == '__main__':
    text = encrypt("fakhermeddeb", "password")
    print text
    print "Encrypt"
    text2 = decrypt(text, "password")
    print "Decrypted"
    print text2
