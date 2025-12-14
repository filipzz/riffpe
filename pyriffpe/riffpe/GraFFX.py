import hashlib
import struct
from typing import Literal

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from ._fallback.Riffpe import Riffpe

import os
import sys
_bench_ws_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../extras/', '.bench_ws'))
sys.path.append(_bench_ws_path)

import gofpe.go
import gofpe.ff1
import gofpe.ff3


class GraFFX(Riffpe):
    def __init__(self, radix: int, digits: int, key: bytes, tweak: bytes, ffx: Literal['ff1', 'ff3']):
        self.radix = radix
        self.digits = digits
        self.key = key
        self.tweak = tweak

        self._kdf_init(radix)

        self.perm_tweak_pfx = struct.pack(f'{self.__kdf_order__}IIQ{len(self.tweak)}s', self.radix,
                                          self.digits, len(self.tweak), self.tweak)
        self.perm_tweak_pfx = pad(self.perm_tweak_pfx,
                                  AES.block_size,
                                  style='pkcs7')
        
        if ffx == 'ff1':
            tweak_len = len(self.perm_tweak_pfx) + (self.digits + 1) * self._kdf_bytes
            tweak_len = len(pad(bytes(tweak_len), AES.block_size, style='pkcs7'))
            self.ffx = gofpe.ff1.NewCipher(10, tweak_len, gofpe.go.Slice_byte(self.key), gofpe.go.Slice_byte(b''))
        elif ffx == 'ff3':
            self.ffx = gofpe.ff3.NewCipher(10, gofpe.go.Slice_byte(self.key), gofpe.go.Slice_byte(b'01234567'))
        else:
            raise ValueError("Unsupported variant")

        if self.radix == 100:
            self.unpack = lambda x: format(x, "02d")
            self.pack = lambda x: int(x, 10)
        elif self.radix == 1000:
            self.unpack = lambda x: format(x, "03d")
            self.pack = lambda x: int(x, 10)
        elif self.radix == 10000:
            self.unpack = lambda x: format(x, "04d")
            self.pack = lambda x: int(x, 10)
        else:
            raise ValueError("Unsupported radix")

    def perm(self, x: int, tweak: bytes, inverse: bool):
        """
        Returns a value of a pseudorandom permutation (or its inverse)
        :param x: element to be permuted
        :param tweak: tweak that is used to generate the permutation
        :param inv: if equal to 0 then the permutation is evaluated if 1 then its inverse
        :return:
        """
        ftweak = (self.perm_tweak_pfx + tweak)
        if isinstance(self.ffx, gofpe.ff3.Cipher):
            ftweak = hashlib.sha256(ftweak).digest()[:8]
        y = self.unpack(x)
        if not inverse:
            y = self.ffx.EncryptWithTweak(y, gofpe.go.Slice_byte(ftweak))
        else:
            y = self.ffx.DecryptWithTweak(y, gofpe.go.Slice_byte(ftweak))
        return self.pack(y)

