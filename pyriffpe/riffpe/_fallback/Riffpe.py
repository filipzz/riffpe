import struct

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from .Perm import Perm
from .CBCTweakablePRNG import CBCTweakablePRNG


class Riffpe:

    @classmethod
    def _get_kdf_params(cls, c: int):
        kdf_order = '<'
        if c < 256:
            kdf_bytes = 1
            kdf_el_struct = struct.Struct('B')
        elif c < 65536:
            kdf_bytes = 2
            kdf_el_struct = struct.Struct('H')
        elif c < 4294967296:
            kdf_bytes = 4
            kdf_el_struct = struct.Struct('I')
        else:
            raise ValueError(f"Radix {c} too big (must be < 32 bits)")
        assert kdf_el_struct.size == kdf_bytes
        return (kdf_order, kdf_bytes, kdf_el_struct)
    
    def _kdf_init(self, c: int):
        self._kdf_params = self._get_kdf_params(c)
        self._kdf_struct = self._kdf_params[2]
        self._kdf_bytes = self._kdf_params[1]

        self._kdf_el_to_bytes = self._kdf_struct.pack

    def __init__(self, c: int, l: int, key: bytes(16), tweak: bytes, chop=1):
        self.c = c
        self.l = l
        self.key = key
        self.tweak = tweak
        self.chop = chop

        self._kdf_init(c)

        self.perm_tweak_pfx = struct.pack(f'<IcIc{len(self.tweak)}s', self.c,
                                          b'_', self.l, b'^', self.tweak)
        self.perm_tweak_pfx = pad(self.perm_tweak_pfx,
                                  AES.block_size,
                                  style='pkcs7')
        self.perm_fun = Perm(self.c, self.chop)
        # This is a precomputed part, used later as an IV,
        # which is equivalent to including the whole prefix
        self.tweak_iv = AES.new(self.key, AES.MODE_CBC, iv=bytes(AES.block_size))\
                           .encrypt(self.perm_tweak_pfx)[-AES.block_size:]
        self.prng = CBCTweakablePRNG(self.key, b'', iv=self.tweak_iv)

    def perm(self, x: int, tweak: bytes, inv: int):
        """
        Returns a value of a pseudorandom permutation (or its inverse)
        :param x: element to be permuted
        :param tweak: tweak that is used to generate the permutation
        :param inv: if equal to 0 then the permutation is evaluated if 1 then its inverse
        :return:
        """
        self.prng.reset(tweak, iv=self.tweak_iv)
        return self.perm_fun.perm(self.prng, x, inv)

    def round(self, f, m, inverse=False):
        """
        Computes a single round of Riffpe
        :param f: Phase id: 0 - absorbing phase, 1 - squeezing phase
        :param m: message to be transformed
        :param inverse: select whether to run forward or reverse operation
        :return:
        """
        tdstate = self._td_state_init(m)
        i_range = range(self.l - 1, -1, -1) if inverse else range(self.l)
        for i in i_range:
            tweak = self._td_state_update(tdstate, m, i, f, inverse)
            m[i] = self.perm(m[i], tweak, inverse)

    def _td_state_init(self, m):
        # Buffer is: self.l elements of self._kdf_bytes, which includes a round marker at ith position
        # +1 element of kdf_bytes for 'i' after the array.
        tweak_len = (self.l + 1) * self._kdf_bytes
        tweak_buf = bytearray(tweak_len + (-tweak_len) % 16)
        idx = 0
        for x in m:
            self._kdf_struct.pack_into(tweak_buf, idx, x)
            idx += self._kdf_bytes
        return tweak_buf
    
    def _td_set_element(self, tweak_buf, i, el):
        self._kdf_struct.pack_into(tweak_buf, i * self._kdf_bytes, el)
    
    def _td_state_update(self, state, m, i, f, inverse):
        """
        :param state: tweak derivation state as returned by _td_state_init
        :param m: message buffer state
        :param i: index of currently processed element
        :param f: round index (0 or 1)
        :param inverse: whether it's an inverse round (determines which element in state needs updating)
        """
        tweak_buf = state
        l = self.l
        if not inverse:
            # forward round and element > 0 -> previous element needs updating
            if i != 0:
                self._td_set_element(tweak_buf, (i-1), m[i-1])
            # forward round and element 0 in round 1 -> last element of round 0 needs updating
            elif f == 1:
                self._td_set_element(tweak_buf, (l-1), m[-1])
        else:
            # inverse round and element < l-1 -> previous element needs updating
            if i != l-1:
                self._td_set_element(tweak_buf, (i+1), m[i+1])
            # inverse round and element l-1 in round 0 -> first element of round 1 needs updating
            elif f == 0:
                self._td_set_element(tweak_buf, 0, m[0])
        # Current index needs to be set to f
        self._td_set_element(tweak_buf, i, f)
        # Last element needs to be set to i
        self._td_set_element(tweak_buf, l, i)
        return tweak_buf

    def encrypt(self, x):
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

    def decrypt(self, x):
        """
        Decrypts z for given tag
        :param tag:
        :param z:
        :return:
        """
        x = list(x)
        assert len(x) == self.l

        # inverting squeezing phase
        self.round(1, x, True)
        # inverting absorbing phase
        self.round(0, x, True)

        return x

    def _aes_engine_id(self):
        import Crypto
        return f"PyCryptodome {Crypto.__version__}"
