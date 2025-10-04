import math
import random
import sys
import time

from typing import List

import riffpe
import riffpe._fallback

try:
    import riffpe._native
    have_native = True
except ImportError:
    print("riffpe._native not found, skipping")
    have_native = False

try:
    import ff3
    have_ff3 = True
except ImportError:
    print("ff3 not found, skipping")
    have_ff3 = False

try:
    import pyffx
    have_pyffx = True
except ImportError:
    print("pyffx not found, skipping")
    have_pyffx = False


# Run make_fpe_bindings.py to generate Python bindings for these targets
try:
    import os
    import sys
    _bench_ws_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.bench_ws'))
    sys.path.append(_bench_ws_path)

    import gofpe.go
    import gofpe.ff1
    import gofpe.ff3

    have_gofpe = True
except ImportError:
    print("gofpe not found, skipping")
    have_gofpe = False


try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x: x


BENCHMARK_PYTHON = False
BENCHMARK_NATIVE = True

BENCHMARK_TAG = bytes.fromhex("0011223344556677")
BENCHMARK_KEY = bytes.fromhex("0123456789abcdef0123456789abcdef")


def _benchmark_common(dataset, label: str, descr: str, encode, encrypt, decrypt):
    print("Dataset", label, descr)
    total_encrypt_time = 0
    total_decrypt_time = 0
    for entry in tqdm(dataset):
        input = encode(entry)
        ts_a = time.perf_counter_ns()
        ctx = encrypt(input)
        ts_b = time.perf_counter_ns()
        ptx = decrypt(ctx)
        ts_c = time.perf_counter_ns()
        assert input == ptx, f"{input} != {ptx}"
        total_encrypt_time += (ts_b - ts_a)
        total_decrypt_time += (ts_c - ts_b)
    
    print(f"total encrypt time: {total_encrypt_time}ns ({total_encrypt_time/1e9}s)")
    print(f"total decrypt time: {total_decrypt_time}ns ({total_decrypt_time/1e9}s)")
    print(f"average encrypt time: {total_encrypt_time/len(dataset)}ns")
    print(f"average decrypt time: {total_decrypt_time/len(dataset)}ns")
    sys.stdout.flush()


bpvs = {
    (128, 10): 144//8, # 137 bits
    (128, 100): 144//8, # 144 bits
    (128, 1000): 152//8, # 152 bits
    (128, 10000): 160//8, # 157 bits
    (256, 10): 272//8, # 265 bits
    (256, 100): 272//8, # 272 bits
    (256, 1000): 280//8, # 278 bits
    (256, 10000): 288//8, # 285 bits
}


def benchmark_riffpe(dataset, radix, digits, label, bits: int, native=False):
    if native and not have_native:
        print("--- native benchmark skipped ---")
        return
    bpv = bpvs[bits, radix]
    if native:
        fpe = riffpe._native.Riffpe(radix, digits, BENCHMARK_KEY, BENCHMARK_TAG, bpv)
    else:
        fpe = riffpe._fallback.Riffpe(radix, digits, BENCHMARK_KEY, BENCHMARK_TAG, bpv)

    descr = f"Riffpe({radix}, {digits}, {bits}-bits) {'[native]' if native else '[Python]'}"
    _benchmark_common(dataset, label, descr,
                      (lambda entry: riffpe.int_to_digits(entry, digits, radix)),
                      fpe.encrypt, fpe.decrypt)


def benchmark_riffpex(dataset, ndigits, th, label, native=False):
    if native and not have_native:
        print("--- native benchmark skipped ---")
        return
    ns = riffpe.find_best_bases(xfactors={2: ndigits, 5: ndigits}, threshold=th)
    print(f"--- best bases for (digits={ndigits}, th={th}) -> {ns!r}")
    if native:
        fpe = riffpe._native.RiffpeX(ns, BENCHMARK_KEY, BENCHMARK_TAG)
    else:
        fpe = riffpe._fallback.RiffpeX(ns, BENCHMARK_KEY, BENCHMARK_TAG)

    descr = f"RiffpeX(n>={th}) {'[native]' if native else '[Python]'}"
    _benchmark_common(dataset, label, descr,
                      (lambda entry: riffpe.int_to_bases(entry, ns)),
                      fpe.encrypt, fpe.decrypt)


def benchmark_ff3(dataset, ndigits, label):
    if not have_ff3:
        print("--- ff3 benchmark skipped ---")
        return
    fpe = ff3.FF3Cipher(BENCHMARK_KEY.hex(), BENCHMARK_TAG.hex())

    _benchmark_common(dataset, label, "FF3 [Python]",
                      (lambda entry: format(entry, f'0{ndigits}d')),
                      fpe.encrypt, fpe.decrypt)


def benchmark_pyffx(dataset, ndigits, label):
    if not have_pyffx:
        print("--- pyffx benchmark skipped ---")
        return
    fpe = pyffx.Integer(BENCHMARK_KEY, ndigits)

    _benchmark_common(dataset, label, "pyffx",
                      (lambda entry: entry),
                      fpe.encrypt, fpe.decrypt)


def benchmark_go_ff1(dataset, ndigits, label):
    if not have_gofpe:
        print("--- go ff1 (binding) benchmark skipped ---")
        return
    fpe = gofpe.ff1.NewCipher(10, len(BENCHMARK_TAG), gofpe.go.Slice_byte(BENCHMARK_KEY), gofpe.go.Slice_byte(BENCHMARK_TAG))

    _benchmark_common(dataset, label, "FF1 [Go]",
                      (lambda entry: format(entry, f'0{ndigits}d')),
                      fpe.Encrypt, fpe.Decrypt)


def benchmark_go_ff3(dataset, ndigits, label):
    if not have_gofpe:
        print("--- go ff3 (binding) benchmark skipped ---")
        return
    fpe = gofpe.ff3.NewCipher(10, gofpe.go.Slice_byte(BENCHMARK_KEY), gofpe.go.Slice_byte(BENCHMARK_TAG))

    _benchmark_common(dataset, label, "FF3 [Go]",
                      (lambda entry: format(entry, f'0{ndigits}d')),
                      fpe.Encrypt, fpe.Decrypt)


def all_benchmarks_for_dataset(dataset, label, ndigits, fbb_ths: List[int], ns: List[int]):
    # Python impls
    benchmark_pyffx(dataset, ndigits, label)
    benchmark_ff3(dataset, ndigits, label)
    if BENCHMARK_PYTHON:
        for radix in ns:
            log10n = int(math.log10(radix))
            if ndigits % log10n != 0:
                print(f"--- riffpe radix = {radix} skipped (domain not divisible) ---")
            digits = ndigits // log10n
            benchmark_riffpe(dataset, radix, digits, label, 128, False)
            benchmark_riffpe(dataset, radix, digits, label, 256, False)
        for th in fbb_ths:
            benchmark_riffpex(dataset, ndigits, th, label, False)

    # Native impls
    benchmark_go_ff1(dataset, ndigits, label)
    benchmark_go_ff3(dataset, ndigits, label)
    if BENCHMARK_NATIVE:
        for radix in ns:
            log10n = int(math.log10(radix))
            if ndigits % log10n != 0:
                print(f"--- riffpe radix = {radix} skipped (domain not divisible) ---")
            digits = ndigits // log10n
            benchmark_riffpe(dataset, radix, digits, label, 128, True)
            benchmark_riffpe(dataset, radix, digits, label, 256, True)
        for th in fbb_ths:
            benchmark_riffpex(dataset, ndigits, th, label, True)


# Benchmark dataset 1: full credit card numbers [16-digit base10 integers]
# Riffpe configurations under test:
#  * n=10, l=16 (potentially insecure)
#  * n=100, l=8
#  * n=10000, l=4 (skipped for now)
# RiffpeX configurations under test:
#  * n >= 16 (20, 20, 20, 20, 20, 20, 20, 20, 25, 25, 25, 25)
#  * n >= 25 (25, 25, 25, 25, 25, 25, 25, 32, 32, 40, 40)
#  * n >= 32 (50, 50, 50, 50, 50, 50, 80, 80, 100)
#  * n >= 50 (50, 50, 50, 50, 50, 50, 80, 80, 100)

BENCHMARK_DATASET_1_LENGTH = 100_000

BENCHMARK_DATASET_1 = [
    random.randrange(10000_0000_0000_0000)
    for _ in range(BENCHMARK_DATASET_1_LENGTH)
]

all_benchmarks_for_dataset(BENCHMARK_DATASET_1, "[16-digit base10 integers]", 16, (16, 25, 50), (10, 100)) # 10000


# Benchmark dataset 2: inner 6 credit card digits [6-digit base10 integers]
# Riffpe configurations under test:
#  * n=10, l=6 (potentially insecure)
#  * n=100, l=3
#  * n=1000, l=2
# RiffpeX configurations under test:
#  * n >= 16 (25, 25, 40, 40)
#  * n >= 25 (25, 25, 40, 40)
#  * n >= 32 (100, 100, 100)
#  * n >= 50 (100, 100, 100)

BENCHMARK_DATASET_2_LENGTH = 100_000

BENCHMARK_DATASET_2 = [
    random.randrange(1000_000)
    for _ in range(BENCHMARK_DATASET_2_LENGTH)
]

all_benchmarks_for_dataset(BENCHMARK_DATASET_2, "[6-digit base10 integers]", 6, (25, 50), (10, 100, 1000))


# Benchmark dataset 3: inner 9 credit card digits [9-digit base10 integers]
# Riffpe configurations under test:
#  * n=10, l=9 (potentially insecure)
#  * n=1000, l=3
# RiffpeX configurations under test:
#  * n >= 16 (25, 25, 25, 40, 40, 40)
#  * n >= 25 (25, 25, 25, 40, 40, 40)
#  * n >= 32 (50, 50, 50, 80, 100)
#  * n >= 50 (50, 50, 50, 80, 100)

BENCHMARK_DATASET_3_LENGTH = 100_000

BENCHMARK_DATASET_3 = [
    random.randrange(1000_000_000)
    for _ in range(BENCHMARK_DATASET_3_LENGTH)
]

all_benchmarks_for_dataset(BENCHMARK_DATASET_3, "[9-digit base10 integers]", 9, (25, 50), (10, 1000))
