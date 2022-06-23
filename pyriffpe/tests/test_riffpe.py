import pytest

from dataclasses import dataclass
from typing import List

from riffpe import Riffpe

# Known answer tests: for now, just test with a few precomputed variants for regression.
# TODO: actually compute KAT vectors on small instances by hand and add to validate

@dataclass
class KATEntry:
    c: int
    l: int
    chops: int
    key: bytes
    tag: bytes
    plaintext: List[int]
    ciphertext: List[int]


KAT_ENTRIES = [
    KATEntry(100, 8, 1,
             bytes.fromhex("00112233445566778899aabbccddeeff"), b'',      
             [78, 56, 78, 56, 34, 12, 34, 12], [28, 52, 19,  8,  4,  5, 14,  9]),
    KATEntry(100, 8, 1,
             bytes.fromhex("00112233445566778899aabbccddeeff"), b'',
             [ 0, 11, 22, 33, 44, 55, 66, 77], [68, 16, 93, 31, 23, 50, 35, 44]),
    KATEntry(100, 8, 1,
             bytes.fromhex("00112233445566778899aabbccddeeff"), b'Alice',
             [ 0, 11, 22, 33, 44, 55, 66, 77], [60, 31, 10, 74, 88, 21, 96, 63]),
]


@pytest.mark.parametrize('kat_entry', KAT_ENTRIES)
def test_encrypt_kat(kat_entry: KATEntry):
    fpe = Riffpe(kat_entry.c, kat_entry.l, kat_entry.key, kat_entry.tag, kat_entry.chops)
    ctx = fpe.enc(kat_entry.plaintext)
    assert ctx == kat_entry.ciphertext


@pytest.mark.parametrize('kat_entry', KAT_ENTRIES)
def test_decrypt_kat(kat_entry: KATEntry):
    fpe = Riffpe(kat_entry.c, kat_entry.l, kat_entry.key, kat_entry.tag, kat_entry.chops)
    ctx = fpe.enc(kat_entry.plaintext)
    assert ctx == kat_entry.ciphertext
