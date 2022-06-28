from typing import Iterable

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from .Riffpe import Riffpe
from .Perm import Perm
from .CBCTweakablePRNG import CBCTweakablePRNG


class RiffpeX(Riffpe):
    """
    A variant of Riffpe that allows each "digit" to be from a different domain; this allows domains such as Z26 x Z_100 x Z_100 x Z_1000 for '[a-z][0-9]{7}' regex.
    NOTE: due to how tweak is derived, RiffpeX will have different outputs from Riffpe even for identical domains, e.g. RiffpeX([10, 10]) will have different outputs
    from Riffpe(10, 2).
    """

    def __init__(self, cs: Iterable[int], key: bytes(16), tweak: bytes, chop=1):
        self.cs = cs
        self.l = len(cs)
        maxc = max(cs)
        self.key = key
        self.tweak = tweak
        self.chop = chop

        self._kdf_init(maxc)

        # Using ':' as a digit separator to ensure different tweaks from regular Riffpe even for the same key.
        self.perm_tweak_pfx = b':'.join(c.to_bytes(4, 'little') for c in cs) + b'^' + self.tweak
        self.perm_tweak_pfx = pad(self.perm_tweak_pfx,
                                  AES.block_size,
                                  style='pkcs7')
        self.perm_funs = [Perm(c, self.chop) for c in cs]
        # This is a precomputed part, used later as an IV,
        # which is equivalent to including the whole prefix
        self.tweak_iv = AES.new(self.key, AES.MODE_CBC, iv=bytes(AES.block_size))\
                           .encrypt(self.perm_tweak_pfx)[-AES.block_size:]
        self.prng = CBCTweakablePRNG(self.key, b'', iv=self.tweak_iv)

    def perm(self, i: int, x: int, tweak: bytes, inv: int):
        """
        Returns a value of a pseudorandom permutation (or its inverse)
        :param i: index of the permutation (due to )
        :param x: element to be permuted
        :param tweak: tweak that is used to generate the permutation
        :param inv: if equal to 0 then the permutation is evaluated if 1 then its inverse
        :return:
        """
        self.prng.reset(tweak, iv=self.tweak_iv)
        return self.perm_funs[i].perm(self.prng, x, inv)

    def round(self, f, m, inverse=False):
        """
        Computes a single round of Riffpe
        :param tag:
        :param f: Phase id: 0 - absorbing phase, 1 - squeezing phase
        :param m: message to be transformed
        :param inverse: select whether to run forward or reverse operation
        :return:
        """
        tdstate = self._td_state_init(m)
        i_range = range(self.l - 1, -1, -1) if inverse else range(self.l)
        for i in i_range:
            tweak = self._td_state_update(tdstate, m, i, f, inverse)
            m[i] = self.perm(i, m[i], tweak, inverse)
