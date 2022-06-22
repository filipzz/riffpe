from .._common.TweakablePRNG import TweakablePRNG
from Crypto.Cipher import AES

class CBCTweakablePRNG(TweakablePRNG):
    block_size = AES.block_size

    def __init__(self, key, tweak):
        self.key = key
        self.tweak = tweak
        self.cipher = AES.new(self.key,
                              AES.MODE_CBC,
                              iv=bytes(AES.block_size))
        # Absorb tweak into CBC state, effectively computing CBC-MAC
        self.cipher.encrypt(tweak)

    def get_bytes(self, count: int) -> bytes:
        # Use CBC-MAC as the IV for a regular CBC, used as a PRNG
        if count % 16 == 0:
            return self.cipher.encrypt(bytes(count))
        raise NotImplementedError


__all__ = ('CBCTweakablePRNG',)
