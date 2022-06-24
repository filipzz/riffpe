import pytest

from dataclasses import dataclass

try:
    from random import randbytes
except ImportError:
    from os import urandom as randbytes
from random import choices

try:
    from riffpe._fallback import Riffpe as RiffpeF
    from riffpe._native import Riffpe as RiffpeN
    skip_parity = False
except ImportError:
    skip_parity = True


@dataclass
class ConfEntry:
    c: int
    l: int
    chops: int
    tag_len: int


TEST_ENTRIES = [
    ConfEntry(100, 8, 1, 10),
    ConfEntry(100, 8, 1, 32),
    ConfEntry(47, 13, 1, 10),
    ConfEntry(47, 13, 4, 10),
]

TEST_REPEATS = 32


@pytest.mark.parametrize('test_entry', TEST_ENTRIES)
def test_parity(test_entry: ConfEntry):
    if skip_parity:
        pytest.skip("Native implementation missing")
    key = randbytes(16)
    tag = randbytes(test_entry.tag_len)
    imp_f = RiffpeF(test_entry.c, test_entry.l, key, tag, test_entry.chops)
    imp_n = RiffpeN(test_entry.c, test_entry.l, key, tag, test_entry.chops)
    for _ in range(TEST_REPEATS):
        val_a = choices(range(test_entry.c), k=test_entry.l)
        # test: b = enc_n(a); c = dec_f(b); a == c
        val_b = imp_f.enc(val_a)
        val_c = imp_n.dec(val_b)
        assert val_a == val_c
        # and : b = dec_n(a); c = enc_f(b); a == c
        val_b = imp_f.dec(val_a)
        val_c = imp_n.enc(val_b)
        assert val_a == val_c
