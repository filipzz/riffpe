from .._common.TweakablePRNG import TweakablePRNG


class Perm:

    def __init__(self, c: int, chop=1):
        self.c = c
        self.bytes_per_value = 16 // chop

    def perm(self, prng: TweakablePRNG, x: int, inv: bool):
        """
        For a given key and iv, generates self.c elements that are encrypted and then sorted.
        In this way a permutation of c elements is obtained (this is in fact Riffle Shuffle).
        :param iv: 
        :param x: 
        :param inv: 
        :return: 
        """

        # this loop implements Riffle Shuffle:
        # each "card" is assigned pseudo-randomly generated bits
        # then a permutation is obtained by sorting the cards

        msg_len = self.bytes_per_value * self.c
        msg_len_padded = msg_len + (-msg_len % prng.block_size)
        stream = prng.get_bytes(msg_len_padded)
        cipher_value_pairs = [(stream[idx * self.bytes_per_value:(idx + 1) * self.bytes_per_value], idx)
                              for idx in range(self.c)]
        cipher_value_pairs.sort()

        if not inv:
            return cipher_value_pairs[x][1]
        else:
            for i, (_, y) in enumerate(cipher_value_pairs):
                if y == x:
                    return i
            raise RuntimeError
