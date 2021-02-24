from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from riffpe.perm import Perm


class Riffpe:
    def __init__(self, c, l, key, chop = 1):
        self.c = c
        self.l = l
        self.key = key
        self.chop = chop
        print("here we go %s %s %s" % (c, l, chop))

    def perm(self, x: int, key: bytearray(16), inv: int):
        """
        Returns a value of a pseudorandom permutation (or its inverse)
        :param x: element to be permuted
        :param key: key that is used to generate the permutation
        :param inv: if equal to 0 then the permutation is evaluated if 1 then its inverse
        :return:
        """
        pi = Perm(self.c, key, self.chop)
        return pi.perm(bytearray(16), x, inv)

    def prf(self, x):
        """
        Returns a pseudo-random value
        :param x: input string
        :return: returns 16-pseudorandom bytes
        """
        cipher = AES.new(self.key, AES.MODE_CBC, bytearray(AES.block_size))
        encrypted = cipher.encrypt(pad(str(x).encode(), AES.block_size))
        return encrypted[-AES.block_size:]

    def round(self, tag, f, m):
        """
        Computes a single round of Riffpe
        :param tag:
        :param f: Phase id: 0 - absorbing phase, 1 - squeezing phase
        :param m: message to be transformed
        :return:
        """

        x_left = []

        for i in range(self.l):
            x = m[i]
            x_right = m[i + 1:]
            k_i = self.key_derivation(x_left, x_right, f, tag)
            y = self.perm(x, k_i, 0)
            x_left.append(y)

        return x_left

    def enc(self, tag, x):
        """
        Encrypts x for given tag by calling twice the round function
        :param tag:
        :param x: input message
        :return:
        """

        # absrobing phase
        y = self.round(tag, 0, x)
        # squeeze phase
        z = self.round(tag, 1, y)

        return z

    def round_inv(self, tag, f, m):
        """
        Computes the inverse of the round function
        :param tag:
        :param f: phase number: 0 - absoribing phase, 1 - squeezing phase
        :param m: message to be parsed
        :return:
        """

        x_right = []

        for i in range(self.l):
            y = m[self.l - 1 - i]
            x_left = m[:-1 - i]
            k_i = self.key_derivation(x_left, x_right, f, tag)
            z = self.perm(y, k_i, 1)
            x_right = [z] + x_right

        return x_right

    def dec(self, tag, z):
        """
        Decrypts z for given tag
        :param tag:
        :param z:
        :return:
        """

        # inverting squeezing phase
        y = self.round_inv(tag, 1, z)

        # inverting absorbing phase
        x = self.round_inv(tag, 0, y)

        return x

    def key_derivation(self, x_left, x_right, f, tag):
        """
        Derives encryption key for given input parameters
        :param x_left:
        :param x_right:
        :param f:
        :param tag:
        :return:
        """
        sep_prev = "<"
        sep_next = ">"
        r = sep_prev.join(map(str, x_left)) + \
            "-" + sep_next.join(map(str, x_right)) + \
            "-" + str(f) + "-" + tag
        k_i = self.prf(r)
        return k_i

