from __future__ import print_function

import base64

import pyaes
from six import text_type, binary_type
# guarantee unicode string
_u = lambda t: t.decode(
    'UTF-8', 'replace') if isinstance(t, binary_type) else t
_uu = lambda *tt: tuple(_u(t) for t in tt)
# guarantee byte string in UTF8 encoding
_u8 = lambda t: t.encode('UTF-8', 'replace') if isinstance(t, text_type) else t
_uu8 = lambda *tt: tuple(_u8(t) for t in tt)


class AESCipher:

    """
    implements an AES encoder that returns a base64 encoded
    ciphertext, and converts from a base64 encoded ciphertext
    back to cleartext.

    Use:
      aes = AESCipher(key)
      b64_cipher = aes.encrypt(plaintext)
      cleartext = aes.decrypt(b64_ciphe)
      assert cleartext == plaintext
    """
    def __init__(self, key):
        self.bs = 32
        if len(key) >= 32:
            self.key = key[:32]
        else:
            self.key = self._pad(key)
        self.key = _u8(self.key)

    def encrypt(self, plaintext):
        plaintext = _u8(plaintext)
        cipher = pyaes.AESModeOfOperationCTR(self.key)
        ciphertext = cipher.encrypt(plaintext)
        return _u(base64.encodebytes(ciphertext))

    def decrypt(self, ciphertext):
        ciphertext = _u8(ciphertext)
        cipher = pyaes.AESModeOfOperationCTR(self.key)
        cleartext = cipher.decrypt(base64.decodebytes(ciphertext))
        return _u(cleartext)

    def _pad(self, s):
        delta = self.bs - len(s) % self.bs
        return s + "{}".format((delta * chr(delta)))

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]


if __name__ == '__main__':
    # test pure implementation
    from pyaes import AESModeOfOperationCTR as AES
    aes = AES(b'This_key_for_demo_purposes_only!')
    plaintext = b'thequickbrownfoxjumpsoverthelazydog'
    cipher = aes.encrypt(plaintext)
    # -- we have to reinitialize the AES to decrypt
    aes = AES(b'This_key_for_demo_purposes_only!')
    decrypt = aes.decrypt(cipher)
    assert decrypt == plaintext, "expected >%s<==>%s<" % (decrypt, plaintext)
    print("OK pure mode")
    # test wrapper
    aes = AESCipher('testkey')
    plaintext = 'thequickbrownfoxjumpsoverthelazydog'
    cipher = aes.encrypt(plaintext)
    decrypt = aes.decrypt(cipher)
    assert decrypt == plaintext, "expected >%s<==>%s<" % (decrypt, plaintext)
    print("OK wrapped mode")
