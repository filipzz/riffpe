from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


class Perm:
    def __init__(self, c: int, key: bytearray):
        self.c = c
        self.key = key

    def perm(self, iv: bytearray, x: int, inv: int):
        """
        For a given key and iv, generates c elements that are encrypted and then sorted.
        In this way a permutation of c elements is otained
        :param iv: 
        :param x: 
        :param inv: 
        :return: 
        """

        cipher = AES.new(self.key, AES.MODE_CBC, iv) 

        permutation = {}

        for i in range(self.c):
            encrypted = cipher.encrypt(pad(str(i).encode(), AES.block_size))
            permutation[encrypted.hex()] = i

        position = 0
        for m in sorted(permutation.keys()):
            if inv == 0 and permutation[m] == x:
                return position
            if inv == 1 and position == x:
                return permutation[m]
            position = position + 1

