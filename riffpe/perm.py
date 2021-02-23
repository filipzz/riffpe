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

        for i in range(self.c // 2):
            encrypted = cipher.encrypt(pad(str(i).encode(), AES.block_size))
            #print(str(encrypted.hex()[0:8]))
            permutation[encrypted.hex()[0:8]] = 4 * i
            #print(str(encrypted.hex()[8:16]))
            permutation[encrypted.hex()[8:16]] = 4 * i + 1
            #print(str(encrypted.hex()[16:24]))
            permutation[encrypted.hex()[16:24]] = 4 * i + 2
            #print(str(encrypted.hex()[24:32]))
            permutation[encrypted.hex()[24:32]] = 4 * i + 3

        position = 0
        for m in sorted(permutation.keys()):
            if inv == 0 and permutation[m] == x:
                return position
            if inv == 1 and position == x:
                return permutation[m]
            position = position + 1

