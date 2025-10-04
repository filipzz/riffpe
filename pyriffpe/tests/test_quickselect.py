from dataclasses import dataclass
import pytest
from random import shuffle

from riffpe._fallback.Perm import _partition, _nth_element

@dataclass
class PartitionEntry:
    lst: list
    begin: int
    end: int
    pivot: int
    exp_lst: list

TEST_ENTRIES = [
    PartitionEntry([1, 2, 3], 0, 3, 2, [1, 2, 3]),
    PartitionEntry([3, 4, 5, 1, 2], 0, 5, 1, [1, 2, 5, 3, 4]),
    PartitionEntry([None, None, None, 1, 2, 3, 4, 5, None, None, None],
                   3, 8, 7,
                   [None, None, None, 1, 2, 3, 4, 5, None, None, None])
]

@pytest.mark.parametrize('test_entry', TEST_ENTRIES)
def test_partition(test_entry: PartitionEntry):
    tmplst = list(test_entry.lst)
    pivot = _partition(tmplst, test_entry.begin, test_entry.end)
    assert pivot == test_entry.pivot, f"{tmplst=}"
    assert tmplst == test_entry.exp_lst


@dataclass
class SelectEntry:
    lst: list[int]
    n: int
    exp: int
    shuffle: bool = False

TEST_ENTRIES_SELECT = [
    SelectEntry([1, 2, 3], 1, 2),
    SelectEntry([1, 3, 2], 1, 2),
    SelectEntry([5, 3, 1], 1, 3),
    SelectEntry([1, 10, 5, 4, 6, 11, 7, 3, 8, 14, 2, 13, 15, 12, 0, 9], 0, 0),
    SelectEntry([1, 10, 5, 4, 6, 11, 7, 3, 8, 14, 2, 13, 15, 12, 0, 9], 15, 15),

    *(SelectEntry(list(range(16)), i, i, True) for i in range(16))
]

@pytest.mark.parametrize('test_entry', TEST_ENTRIES_SELECT)
def test_nth_element(test_entry: SelectEntry):
    tmplst = list(test_entry.lst)
    if test_entry.shuffle:
        shuffle(tmplst)
        print(tmplst)
    elem = _nth_element(tmplst, test_entry.n)
    assert elem == test_entry.exp

