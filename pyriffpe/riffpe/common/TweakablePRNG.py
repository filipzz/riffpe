from abc import abstractmethod


class TweakablePRNG:
    block_size: int

    @abstractmethod
    def __init__(self, key, tweak):
        raise NotImplementedError

    @abstractmethod
    def get_bytes(self, count: int) -> bytes:
        raise NotImplementedError


__all__ = ('TweakablePRNG',)
