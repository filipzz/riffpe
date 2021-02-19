import hashlib


class Riffpe:
    def __init__(self, c, l):
        self.c = c
        self.l = l

    def rs(self, key: str, tag: str, x_left, x: int, x_right, f, inv: int):
        """
        This is the mock up of riffle shuffle
        (it is not RS at all but this gives "permutation functionality")

        :param key - the key
        :param tag - tag
        :param x_left - a list of integers representing "left dependents"
        :param x - an integer to be "encrypted"
        :param x_right - a list of integers representing "right dependents"
        :param inv - either 0 or 1 representing if we calculate RS or its inverse
        """
        sep_prev = "<"
        sep_next = ">"
        derived_seed = "f:" + str(f)  + "-l:" + sep_prev.join(map(str, x_left)) + "-r:" + sep_next.join(map(str, x_right)) + "-t:" + tag
        derived_key = hashlib.pbkdf2_hmac('sha256', b'abcdef', derived_seed.encode(), 100)
        derived_key_int = int(derived_key.hex(), 16)
        # print("%s %s %s %s" % (k, t, x, key_int))
        return (x + (-1) ** inv * derived_key_int) % self.c

    def round(self, key, tag, f, m):

        x_left = []

        for i in range(self.l):
            x = m[i]
            x_right = m[i + 1:]
            y = self.rs(key, tag, x_left, x, x_right, f, 0)
            x_left.append(y)

        return x_left

    def enc(self, key: str, tag: str, x):

        # absrobing phase
        y = self.round(key, tag, 0, x)
        # squeeze phase
        z = self.round(key, tag, 1, y)

        # print("%s\n%s\n%s" % (X, Y, Z))
        return z

    def round_inv(self, key, tag, f, m):

        x_right = []

        for i in range(self.l):
            y = m[self.l - 1 - i]
            x_left = m[:-1 - i]
            z = self.rs(key, tag, x_left, y, x_right, f, 1)
            x_right = [z] + x_right

        return x_right

    def dec(self, key, tag, z):

        y = self.round_inv(key, tag, 1, z)

        x = self.round_inv(key, tag, 0, y)

        # print("%s\n%s\n%s" % (Z, Y, X))
        return x
