import hashlib


class Riffpe:
    def __init__(self, c, l):
        self.c = c
        self.l = l

    def rs(self, key: str, tag: str, x_prev, x: int, x_next, inv: int):
        '''
        This is the mock up of riffle shuffle
        (it is not RS at all but this gives "permutation functionality")

        :param str key - the key
        :param str tag - tag
        :param x_prev - a list of integers representing "left dependents"
        :param x - an integer to be "encrypted"
        :param x_next - a list of integers representing "right dependents"
        :param inv - either 0 or 1 representing if we calculate RS or its inverse
        '''
        sep_prev = "<"
        sep_next = ">"
        derived_seed = "k:" + key + "-t:" + tag + "-l:" + sep_prev.join(map(str, x_prev)) + "-r:" + sep_next.join(
            map(str, x_next))
        derived_key = hashlib.pbkdf2_hmac('sha256', b'abcdef', derived_seed.encode(), 100)
        derived_key_int = int(derived_key.hex(), 16)
        # print("%s %s %s %s" % (k, t, x, key_int))
        return (x + (-1) ** inv * derived_key_int) % self.c

    def phase_enc(self, key, tag, m):

        prev = []

        for i in range(self.l):
            x = m[i]
            next = m[i + 1:]
            y = self.rs(key, tag, prev, x, next, 0)
            prev.append(y)

        return prev

    def enc(self, key: str, tag: str, X):

        # absrobing phase
        Y = self.phase_enc(key, tag, X)

        # squeeze phase
        Z = self.phase_enc(key, tag, Y)

        # print("%s\n%s\n%s" % (X, Y, Z))
        return Z

    def phase_dec(self, key, tag, m):

        prev = m[:-1]
        y = m[self.l - 1]
        next = []

        for i in range(self.l):
            y = m[self.l - 1 - i]
            prev = m[:-1 - i]
            z = self.rs(key, tag, prev, y, next, 1)
            next = [z] + next

        return next

    def dec(self, key, tag, Z):

        Y = self.phase_dec(key, tag, Z)

        X = self.phase_dec(key, tag, Y)

        # print("%s\n%s\n%s" % (Z, Y, X))
        return X
