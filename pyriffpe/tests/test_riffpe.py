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
             [78, 56, 78, 56, 34, 12, 34, 12], [19, 81, 89, 54, 92, 76, 23, 31]),
    KATEntry(100, 8, 1,
             bytes.fromhex("00112233445566778899aabbccddeeff"), b'',
             [ 0, 11, 22, 33, 44, 55, 66, 77], [79, 91, 99, 80, 26, 46, 71, 40]),
    KATEntry(100, 8, 1,
             bytes.fromhex("00112233445566778899aabbccddeeff"), b'Alice',
             [ 0, 11, 22, 33, 44, 55, 66, 77], [60, 26, 85, 84, 39, 18,  1, 26]),
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
