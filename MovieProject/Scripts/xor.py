from __future__ import print_function, unicode_literals
from os import urandom
import random


def genkey(length: int) -> str:
    """Generate key."""
    max_letters = 26
    key = ""
    for i in range(length):
        key += chr(ord('a') + random.randrange(0,max_letters))
    return key


def xor_strings(s, t) -> str:
    """xor two strings together."""
    if isinstance(s, str):
        # Text strings contain single characters
        return "".join(chr(ord('a') + (ord(a) ^ ord(b)) % 26) for a, b in zip(s, t))


message = 'This is a secret message'
print('Message:', message)

key = genkey(len(message))
print('Key:', key)

cipherText = xor_strings(message, key)
print('cipherText:', cipherText)
print('decrypted:', xor_strings(cipherText, key))

# Verify
if xor_strings(cipherText, key) == message:
    print('Unit test passed')
else:
    print('Unit test failed')