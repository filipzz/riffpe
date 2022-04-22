from abc import abstractmethod
from Crypto.Cipher import AES


class TweakablePRNG:
    block_size: int

    @abstractmethod
    def __init__(self, key, tweak):
        raise NotImplementedError

    @abstractmethod
    def get_bytes(self, count: int) -> bytes:
        raise NotImplementedError


class CBCTweakablePRNG(TweakablePRNG):
    block_size = AES.block_size

    @abstractmethod
    def __init__(self, key, tweak):
        self.key = key
        self.tweak = tweak
        self.cipher = AES.new(self.key, AES.MODE_CBC, iv=bytes(AES.block_size))
        # Absorb tweak into CBC state, effectively computing CBC-MAC
        self.cipher.encrypt(tweak)

    @abstractmethod
    def get_bytes(self, count: int) -> bytes:
        # Use CBC-MAC as the IV for a regular CBC, used as a PRNG
        if count % 16 == 0:
            return self.cipher.encrypt(bytes(count))
        raise NotImplementedError