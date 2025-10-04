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
    KATEntry(4, 1, 16,
             bytes.fromhex("00112233445566778899aabbccddeeff"), b'Alice',
             [2], [0]),
    KATEntry(4, 2, 16,
             bytes.fromhex("00112233445566778899aabbccddeeff"), b'Alice',
             [2, 3], [2, 0]),
    KATEntry(5, 3, 16,
             bytes.fromhex("00112233445566778899aabbccddeeff"), b'Alice',
             [2, 3, 4], [4, 3, 3]),
    KATEntry(100, 8, 16,
             bytes.fromhex("00112233445566778899aabbccddeeff"), b'',
             [78, 56, 78, 56, 34, 12, 34, 12], [28, 36, 5, 6, 31, 54, 58, 51]),
    KATEntry(100, 8, 16,
             bytes.fromhex("00112233445566778899aabbccddeeff"), b'',
             [ 0, 11, 22, 33, 44, 55, 66, 77], [33, 86, 47, 42, 11, 62, 2, 36]),
    KATEntry(100, 8, 16,
             bytes.fromhex("00112233445566778899aabbccddeeff"), b'Alice',
             [ 0, 11, 22, 33, 44, 55, 66, 77], [63, 83, 10, 79, 18, 16, 44, 47]),
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
