import pytest

from dataclasses import dataclass
from typing import List

from riffpe import Riffpe

# Known answer tests: for now, just test with a few precomputed variants for regression.
# TODO: actually compute KAT vectors on small instances by hand and add to validate

@dataclass
class KATEntry:
    radix: int
    digits: int
    bytes_per_value: int
    key: bytes
    tag: bytes
    plaintext: List[int]
    ciphertext: List[int]


KAT_ENTRIES = [
    KATEntry(100, 8, 1,
             bytes.fromhex("00112233445566778899aabbccddeeff"), b'',
             # 3594761421525475
             [78, 56, 78, 56, 34, 12, 34, 12], [75, 54, 52, 21, 14, 76, 94, 35]),
    KATEntry(100, 8, 1,
             bytes.fromhex("00112233445566778899aabbccddeeff"), b'',
             [ 0, 11, 22, 33, 44, 55, 66, 77], [59, 11, 93,  5, 91, 60, 48,  0]),
    KATEntry(100, 8, 1,
             bytes.fromhex("00112233445566778899aabbccddeeff"), b'Alice',
             # 0284503011236181
             [ 0, 11, 22, 33, 44, 55, 66, 77], [81, 61, 23, 11, 30, 50, 84,  2]),
]


@pytest.mark.parametrize('kat_entry', KAT_ENTRIES)
def test_encrypt_kat(kat_entry: KATEntry):
    fpe = Riffpe(kat_entry.radix, kat_entry.digits, kat_entry.key, kat_entry.tag, kat_entry.bytes_per_value)
    ctx = fpe.encrypt(kat_entry.plaintext)
    assert ctx == kat_entry.ciphertext


@pytest.mark.parametrize('kat_entry', KAT_ENTRIES)
def test_decrypt_kat(kat_entry: KATEntry):
    fpe = Riffpe(kat_entry.radix, kat_entry.digits, kat_entry.key, kat_entry.tag, kat_entry.bytes_per_value)
    ptx = fpe.decrypt(kat_entry.ciphertext)
    assert ptx == kat_entry.plaintext
