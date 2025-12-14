from typing import Optional
from .._common.TweakablePRNG import TweakablePRNG


def _partition(lst: list, begin, end):
    count = end - begin
    if count == 0:
        raise ValueError("_partition called on an empty range")
    x = lst[end-1] 
    i = begin
    for j in range(i, end-1): 
        if lst[j] <= x: 
            lst[i], lst[j] = lst[j], lst[i] 
            i += 1
    lst[i], lst[end-1] = x, lst[i] 
    return i 

def _nth_element(lst: list, n: int, begin: int = 0, end: Optional[int] = None):
    if end is None:
        end = len(lst)
    if end - begin <= 25:
        tmp = lst[begin:end]
        tmp.sort()
        # If we want we can lst[begin:end] = tmp
        # but it's not required in this case
        return tmp[n-begin]
    else:
        pivot = _partition(lst, begin, end)
        if n < pivot:  # Recurse left
            return _nth_element(lst, n, begin, pivot)
        elif pivot < n:  # Recurse right
            return _nth_element(lst, n, pivot + 1, end)
        else:
            return lst[pivot] 


class Perm:

    def __init__(self, elements: int, bytes_per_value: int = 16):
        self.elements = elements
        self.bytes_per_value = bytes_per_value

    def perm(self, prng: TweakablePRNG, x: int, inv: bool):
        """
        For a given `prng`, generates `self.elements` elements that are encrypted and then sorted.
        In this way a permutation of `self.elements` elements is obtained (this is in fact Riffle Shuffle).
        :param prng: 
        :param x: 
        :param inv: 
        :return: 
        """

        # this loop implements Riffle Shuffle:
        # each "card" is assigned pseudo-randomly generated bits
        # then a permutation is obtained by sorting the cards

        msg_len = self.bytes_per_value * self.elements
        msg_len_padded = msg_len + (-msg_len % prng.block_size)
        stream = prng.get_bytes(msg_len_padded)
        cipher_value_pairs = [(stream[idx * self.bytes_per_value:(idx + 1) * self.bytes_per_value], idx)
                              for idx in range(self.elements)]

        if not inv:
            # Quick select
            # return _nth_element(cipher_value_pairs, x)[1]
            # Apparently the naive solution is still faster:
            cipher_value_pairs.sort()
            return cipher_value_pairs[x][1]
        else:
            n = cipher_value_pairs[x]
            # rank = sum(1 for it in cipher_value_pairs if it < n)
            rank = 0
            for it in cipher_value_pairs:
                if it < n:
                    rank += 1
            return rank
