from .._common.TweakablePRNG import TweakablePRNG
from Crypto.Cipher import AES

# Used in low-level access in reset
from Crypto.Cipher._mode_cbc import raw_cbc_lib, c_uint8_ptr, c_size_t


class CBCTweakablePRNG(TweakablePRNG):
    block_size = AES.block_size

    def __init__(self, key, tweak, iv=bytes(AES.block_size)):
        self.key = key
        self.tweak = tweak
        self.cipher = AES.new(self.key,
                              AES.MODE_CBC,
                              iv=iv)
        self.xcipher = AES.new(self.key, AES.MODE_ECB)
        # Absorb tweak into CBC state, effectively computing CBC-MAC
        self.cipher.encrypt(tweak)
        # Allocate temporary buffer for `reset` function
        self._buffer = bytearray(AES.block_size)
        self._buffer_p = c_uint8_ptr(self._buffer)
    
    def reset(self, tweak, iv=bytes(AES.block_size)):
        # Hack Crypto.Cipher into changing iv by forcing use of cbc decrypt
        # - this works because in CBC decrypt, the last input (ciphertext)
        # block becomes the new "iv/state" for the next block.
        # (this appears to be the fastest option available
        # without looking into cipher._state internal structure)
        p_iv = c_uint8_ptr(iv)
        raw_cbc_lib.CBC_decrypt(self.cipher._state.get(),
                                p_iv, self._buffer_p, c_size_t(AES.block_size))
        self.cipher.encrypt(tweak)

    def get_bytes(self, count: int) -> bytes:
        # Use CBC-MAC as the IV for a regular CBC, used as a PRNG
        if count % 16 == 0:
            return self.cipher.encrypt(bytes(count))
        raise NotImplementedError


__all__ = ('CBCTweakablePRNG',)
