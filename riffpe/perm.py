from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

class Perm:

    def __init__(self, c: int, key: bytearray, chop = 1):
        self.c = c
        self.key = key
        self.chop = chop

    def perm(self, iv: bytearray, x: int, inv: int):
        """
        For a given key and iv, generates self.c elements that are encrypted and then sorted.
        In this way a permutation of c elements is obtained (this is in fact Riffle Shuffle).
        :param iv: 
        :param x: 
        :param inv: 
        :return: 
        """
        cipher = AES.new(self.key, AES.MODE_CBC, iv)

        permutation = {}
        permutation_inv = {}

        steps = 0
        i = 0
        generated_parts = 0
        # this loop implements Riffle Shuffle:
        # each "card" is assigned pseudo-randomly generated bits
        # then a permutation is obtained by sorting the cards
        enc_calls = 0
        while generated_parts < self.c:
            msg_len = 32 * self.c
            encrypted = cipher.encrypt(pad((msg_len * " ").encode(), AES.block_size))
            part = 0
            enc_calls = enc_calls + 1
            while part < self.chop and generated_parts < self.c:
                from_i = part * (32  * self.c // self.chop)
                to_i = (part + 1) * (32 * self.c // self.chop) - 1
                k_id = encrypted.hex()[from_i:to_i]
                permutation[k_id] = generated_parts
                permutation_inv[str(generated_parts)] = k_id
                generated_parts = generated_parts + 1
                part = part + 1
                steps = steps + 1
                #print(part, from_i, to_i, k_id)
            i = i + 1
        w = sorted(permutation.keys())

        if inv == 0:
            id = permutation_inv[str(x)]
            return w.index(id)
        else:
            id = w[x]
            return permutation[id]