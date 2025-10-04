import pytest

from dataclasses import dataclass
from typing import Sequence

from riffpe import find_best_bases


@dataclass
class FBBEntry:
    x: int
    t: int
    expected: Sequence[int]

FBB_ENTRIES = [
    FBBEntry(x=7_000_000_000, t=30, expected=(35, 40, 40, 50, 50, 50)),
    FBBEntry(x=  227_840_000, t=24, expected=(40, 40, 40, 40, 89)),
]

@pytest.mark.parametrize('fbb_entry', FBB_ENTRIES)
def test_find_best_bases_kat(fbb_entry: FBBEntry):
    out = find_best_bases(fbb_entry.x, fbb_entry.t)
    assert out == fbb_entry.expected
