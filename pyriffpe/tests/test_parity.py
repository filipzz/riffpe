import pytest

from dataclasses import dataclass
from typing import List

try:
    from random import randbytes
except ImportError:
    from os import urandom as randbytes
from random import choices, randrange

try:
    from riffpe._fallback import Riffpe as RiffpeF, RiffpeX as RiffpeXF
    from riffpe._native import Riffpe as RiffpeN, RiffpeX as RiffpeXN
    skip_parity = False
except ImportError:
    skip_parity = True


@dataclass
class ConfEntry:
    radix: int
    digits: int
    bytes_per_value: int
    tweak_len: int


TEST_ENTRIES = [
    ConfEntry(100, 8, 16, 10),
    ConfEntry(100, 8, 16, 32),
    ConfEntry(47, 13, 16, 10),
    ConfEntry(47, 13, 4, 10),
    ConfEntry(100, 8, 1, 10),
    ConfEntry(100, 8, 27, 10),
]

TEST_REPEATS = 32


@pytest.mark.parametrize('test_entry', TEST_ENTRIES)
def test_parity(test_entry: ConfEntry):
    if skip_parity:
        pytest.skip("Native implementation missing")
    key = randbytes(16)
    tweak = randbytes(test_entry.tweak_len)
    imp_f = RiffpeF(test_entry.radix, test_entry.digits, key, tweak, test_entry.bytes_per_value)
    imp_n = RiffpeN(test_entry.radix, test_entry.digits, key, tweak, test_entry.bytes_per_value)
    for _ in range(TEST_REPEATS):
        val_a = choices(range(test_entry.radix), k=test_entry.digits)
        # test: b = enc_n(a); c = dec_f(b); a == c
        val_b = imp_f.encrypt(val_a)
        val_c = imp_n.decrypt(val_b)
        assert val_a == val_c
        # and : b = dec_n(a); c = enc_f(b); a == c
        val_b = imp_f.decrypt(val_a)
        val_c = imp_n.encrypt(val_b)
        assert val_a == val_c


# RiffpeX
@dataclass
class ConfEntryX:
    radices: List[int]
    bytes_per_value: int
    tweak_len: int


TEST_ENTRIES_X = [
    ConfEntryX([10, 20, 30, 40], 16, 10),
    ConfEntryX([10, 20, 30, 40], 16, 32),
    ConfEntryX([40, 50, 50, 100], 16, 10),
    ConfEntryX([40, 50, 50, 100], 4, 10),
    ConfEntryX([40, 50, 50, 100], 1, 10),
    ConfEntryX([40, 50, 50, 100], 27, 10),
]

TEST_REPEATS_X = 32


@pytest.mark.parametrize('test_entry', TEST_ENTRIES_X)
def test_parity_x(test_entry: ConfEntryX):
    if skip_parity:
        pytest.skip("Native implementation missing")
    key = randbytes(16)
    tweak = randbytes(test_entry.tweak_len)
    imp_f = RiffpeXF(test_entry.radices, key, tweak, test_entry.bytes_per_value)
    imp_n = RiffpeXN(test_entry.radices, key, tweak, test_entry.bytes_per_value)
    for _ in range(TEST_REPEATS_X):
        val_a = [randrange(c) for c in test_entry.radices]
        # test: b = enc_n(a); c = dec_f(b); a == c
        val_b = imp_f.encrypt(val_a)
        val_c = imp_n.decrypt(val_b)
        assert val_a == val_c
        # and : b = dec_n(a); c = enc_f(b); a == c
        val_b = imp_f.decrypt(val_a)
        val_c = imp_n.encrypt(val_b)
        assert val_a == val_c
