#!/usr/bin/env python

"""
    Copyright (C) 2012 Bo Zhu http://about.bozhu.me

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in
    all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
"""


def KSA(key):
    keylength = len(key)

    S = range(256)

    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % keylength]) % 256
        S[i], S[j] = S[j], S[i]  # swap

    return S


def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]  # swap

        K = S[(S[i] + S[j]) % 256]
        yield K


def RC4(key):
    S = KSA(key)
    return PRGA(S)


def __convert_key(s):
    return [ord(c) for c in s]


def __get_key():
    key = 'better to keep the key scrambled if it is in the source code.'
    return __convert_key(key)


def encrypt(plain_text):
    keystream = RC4(__get_key())
    encrypted_plain_text = ''.join(["%02X" % (ord(character) ^ keystream.next()) for character in plain_text])
    return encrypted_plain_text


def decrypt(cipher_text):
    keystream = RC4(__get_key())
    decrypted_text = ''.join([chr(int(cipher_text[i:i+2], 16) ^ keystream.next()) for i in range(0, len(cipher_text), 2)])
    return decrypted_text


if __name__ == '__main__':
    plaintext = "Some Plain Text"

    cipher_text = encrypt(plaintext)
    print cipher_text

    plain_text = decrypt(cipher_text)
    print plain_text
