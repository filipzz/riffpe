from .._common.TweakablePRNG import TweakablePRNG
from Crypto.Cipher import AES
from Crypto.Util import Counter

from hashlib import sha256


class CTRTweakablePRNG(TweakablePRNG):
    block_size = AES.block_size

    def __init__(self, key, tweak):
        self.key = key
        self.tweak = tweak
        self.state = sha256(self.tweak).digest()
        self.counter = Counter.new(prefix=self.state[:12])
        self.cipher = AES.new(self.key,
                              AES.MODE_CTR,
                              counter=self.counter)

    def reset(self, tweak):
        self.tweak = tweak
        self.state = sha256(self.tweak).digest()
        # self.cipher = AES.new(self.key,
        #                       AES.MODE_CTR,
        #                       nonce=self.state[:12])
        self.counter

    def get_bytes(self, count: int) -> bytes:
        return self.cipher.encrypt(bytes(count))


__all__ = ('CTRTweakablePRNG',)

