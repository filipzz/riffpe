import struct

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from .Perm import Perm
from .CBCTweakablePRNG import CBCTweakablePRNG


class Riffpe:

    def __init__(self, c: int, l: int, key: bytes(16), tweak: bytes, chop=1):
        self.c = c
        self.l = l
        self.key = key
        self.tweak = tweak
        self.chop = chop

        self.kdf_order = 'little'
        if c < 256:
            self.kdf_bytes = 1
        elif c < 65536:
            self.kdf_bytes = 2
        elif c < 4294967296:
            self.kdf_bytes = 4
        else:
            raise ValueError(f"Radix {c} too big (must be < 32 bits)")

        self.perm_tweak_pfx = struct.pack(f'<IcIc{len(self.tweak)}s', self.c,
                                          b'_', self.l, b'^', self.tweak)
        self.perm_tweak_pfx = pad(self.perm_tweak_pfx,
                                  AES.block_size,
                                  style='pkcs7')
        self.perm_fun = Perm(self.c, self.chop)
        #print("here we go %s %s %s" % (c, l, tweak, chop))

    def perm(self, x: int, tweak: bytes, inv: int):
        """
        Returns a value of a pseudorandom permutation (or its inverse)
        :param x: element to be permuted
        :param tweak: tweak that is used to generate the permutation
        :param inv: if equal to 0 then the permutation is evaluated if 1 then its inverse
        :return:
        """
        prng = CBCTweakablePRNG(self.key, self.perm_tweak_pfx + tweak)
        return self.perm_fun.perm(prng, x, inv)

    def round(self, f, m):
        """
        Computes a single round of Riffpe
        :param tag:
        :param f: Phase id: 0 - absorbing phase, 1 - squeezing phase
        :param m: message to be transformed
        :return:
        """
        for i, x in enumerate(m):
            tweak = self.tweak_derivation(m[:i], m[i + 1:], f, i)
            y = self.perm(x, tweak, False)
            m[i] = y

    def enc(self, x):
        """
        Encrypts x by calling twice the round function
        :param x: input message
        :return:
        """
        x = list(x)
        assert len(x) == self.l

        # absorbing phase
        self.round(0, x)
        # squeezing phase
        self.round(1, x)

        return x

    def round_inv(self, f, m):
        """
        Computes the inverse of the round function
        :param f: phase number: 0 - absoribing phase, 1 - squeezing phase
        :param m: message to be parsed
        :return:
        """
        for i in range(self.l - 1, -1, -1):
            x = m[i]
            tweak = self.tweak_derivation(m[:i], m[i + 1:], f, i)
            y = self.perm(x, tweak, True)
            m[i] = y

    def dec(self, x):
        """
        Decrypts z for given tag
        :param tag:
        :param z:
        :return:
        """
        x = list(x)
        assert len(x) == self.l

        # inverting squeezing phase
        self.round_inv(1, x)
        # inverting absorbing phase
        self.round_inv(0, x)

        return x

    def _kdf_el_to_bytes(self, el):
        return el.to_bytes(self.kdf_bytes, self.kdf_order)

    def tweak_derivation(self, x_left, x_right, f, i):
        """
        Derives encryption key for given input parameters
        :param x_left:
        :param x_right:
        :param f:
        :return:
        """
        tweak_len = (self.l + 1) * self.kdf_bytes
        tweak_buf = bytearray(tweak_len + (-tweak_len) % 16)
        idx = 0
        for x in x_left:
            tweak_buf[idx:idx + self.kdf_bytes] = self._kdf_el_to_bytes(x)
            idx += self.kdf_bytes
        # The place with f can serve as a neat separator between left and right sides;
        # to avoid "looking like" regular element, another marking could be used, e.g. A5 for f=0 amd 5A for f=1
        tweak_buf[idx:idx + self.kdf_bytes] = self._kdf_el_to_bytes(f)
        idx += self.kdf_bytes
        for x in x_right:
            tweak_buf[idx:idx + self.kdf_bytes] = self._kdf_el_to_bytes(x)
            idx += self.kdf_bytes
        tweak_buf[idx:idx + self.kdf_bytes] = self._kdf_el_to_bytes(i)

        return tweak_buf

    def _aes_engine_id(self):
        import Crypto
        return f"PyCryptodome {Crypto.__version__}"
