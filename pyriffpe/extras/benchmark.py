import random
import sys
import time

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
    import os, sys
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


def benchmark_riffpe(dataset, n, l, label, native=False):
    if native and not have_native:
        print("--- native benchmark skipped ---")
        return
    if native:
        fpe = riffpe._native.Riffpe(n, l, BENCHMARK_KEY, BENCHMARK_TAG)
    else:
        fpe = riffpe._fallback.Riffpe(n, l, BENCHMARK_KEY, BENCHMARK_TAG)

    descr = f"Riffpe({n}, {l}) {'[native]' if native else '[Python]'}"
    _benchmark_common(dataset, label, descr,
                      (lambda entry: riffpe.int_to_digits(entry, l, n)),
                      fpe.encrypt, fpe.decrypt)


def benchmark_riffpex(dataset, ns, label, native=False):
    if native and not have_native:
        print("--- native benchmark skipped ---")
        return
    if native:
        fpe = riffpe._native.RiffpeX(ns, BENCHMARK_KEY, BENCHMARK_TAG)
    else:
        fpe = riffpe._fallback.RiffpeX(ns, BENCHMARK_KEY, BENCHMARK_TAG)

    descr = f"RiffpeX{tuple(ns)!r} {'[native]' if native else '[Python]'}"
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
        print(f"--- go ff1 (binding) benchmark skipped ---")
        return
    fpe = gofpe.ff1.NewCipher(10, len(BENCHMARK_TAG), gofpe.go.Slice_byte(BENCHMARK_KEY), gofpe.go.Slice_byte(BENCHMARK_TAG))

    _benchmark_common(dataset, label, f"FF1 [Go]",
                      (lambda entry: format(entry, f'0{ndigits}d')),
                      fpe.Encrypt, fpe.Decrypt)


def benchmark_go_ff3(dataset, ndigits, label):
    if not have_gofpe:
        print(f"--- go ff3 (binding) benchmark skipped ---")
        return
    fpe = gofpe.ff3.NewCipher(10, gofpe.go.Slice_byte(BENCHMARK_KEY), gofpe.go.Slice_byte(BENCHMARK_TAG))

    _benchmark_common(dataset, label, f"FF3 [Go]",
                      (lambda entry: format(entry, f'0{ndigits}d')),
                      fpe.Encrypt, fpe.Decrypt)


# Benchmark dataset 1: full credit card numbers [16-digit base10 integers]
# Riffpe configurations under test:
#  * n=10, l=16 (potentially insecure)
#  * n=100, l=8
#  * n=10000, l=4

BENCHMARK_DATASET_1_LENGTH = 10_000

BENCHMARK_DATASET_1 = [
    random.randrange(10000_0000_0000_0000)
    for _ in range(BENCHMARK_DATASET_1_LENGTH)
]


benchmark_pyffx(BENCHMARK_DATASET_1, 16, "[16-digit base10 integers]")
benchmark_ff3(BENCHMARK_DATASET_1, 16, "[16-digit base10 integers]")
benchmark_riffpe(BENCHMARK_DATASET_1, 10,    16, "[16-digit base10 integers]", False)
benchmark_riffpe(BENCHMARK_DATASET_1, 100,   8,  "[16-digit base10 integers]", False)
benchmark_riffpe(BENCHMARK_DATASET_1, 10000, 4,  "[16-digit base10 integers]", False)
benchmark_go_ff1(BENCHMARK_DATASET_1, 16, "[16-digit base10 integers]")
benchmark_go_ff3(BENCHMARK_DATASET_1, 16, "[16-digit base10 integers]")
benchmark_riffpe(BENCHMARK_DATASET_1, 10,    16, "[16-digit base10 integers]", True)
benchmark_riffpe(BENCHMARK_DATASET_1, 100,   8,  "[16-digit base10 integers]", True)
benchmark_riffpe(BENCHMARK_DATASET_1, 10000, 4,  "[16-digit base10 integers]", True)


# Benchmark dataset 2: inner 6 credit card digits [6-digit base10 integers]
# Riffpe configurations under test:
#  * n=10, l=6 (potentially insecure)
#  * n=100, l=3
#  * n=1000, l=2

BENCHMARK_DATASET_2_LENGTH = 10_000

BENCHMARK_DATASET_2 = [
    random.randrange(1000_000)
    for _ in range(BENCHMARK_DATASET_2_LENGTH)
]


benchmark_pyffx(BENCHMARK_DATASET_2, 6, "[6-digit base10 integers]")
benchmark_ff3(BENCHMARK_DATASET_2, 6, "[6-digit base10 integers]")
benchmark_riffpe(BENCHMARK_DATASET_2, 10,   6, "[6-digit base10 integers]", False)
benchmark_riffpe(BENCHMARK_DATASET_2, 100,  3, "[6-digit base10 integers]", False)
benchmark_riffpe(BENCHMARK_DATASET_2, 1000, 2, "[6-digit base10 integers]", False)
benchmark_go_ff1(BENCHMARK_DATASET_2, 6, "[6-digit base10 integers]")
benchmark_go_ff3(BENCHMARK_DATASET_2, 6, "[6-digit base10 integers]")
benchmark_riffpe(BENCHMARK_DATASET_2, 10,   6, "[6-digit base10 integers]", True)
benchmark_riffpe(BENCHMARK_DATASET_2, 100,  3, "[6-digit base10 integers]", True)
benchmark_riffpe(BENCHMARK_DATASET_2, 1000, 2, "[6-digit base10 integers]", True)


# Benchmark dataset 3: inner 9 credit card digits [9-digit base10 integers]
# Riffpe configurations under test:
#  * n=10, l=9 (potentially insecure)
#  * n=1000, l=3
# RiffpeX configurations under test:
#  * (100, 100, 100, 1000)
#  * (50, 50, 40, 100, 100)
#  * (50, 50, 50, 80, 100)

BENCHMARK_DATASET_3_LENGTH = 10_000

BENCHMARK_DATASET_3 = [
    random.randrange(1000_000_000)
    for _ in range(BENCHMARK_DATASET_3_LENGTH)
]


benchmark_pyffx(BENCHMARK_DATASET_3, 9, "[9-digit base10 integers]")
benchmark_ff3(BENCHMARK_DATASET_3, 9, "[9-digit base10 integers]")
benchmark_riffpe(BENCHMARK_DATASET_3, 10,   9, "[9-digit base10 integers]", False)
benchmark_riffpe(BENCHMARK_DATASET_3, 1000, 3, "[9-digit base10 integers]", False)
benchmark_riffpex(BENCHMARK_DATASET_3, (100, 100, 100, 1000),  "[9-digit base10 integers]", False)
benchmark_riffpex(BENCHMARK_DATASET_3, (50, 50, 40, 100, 100), "[9-digit base10 integers]", False)
benchmark_riffpex(BENCHMARK_DATASET_3, (50, 50, 50, 80, 100),  "[9-digit base10 integers]", False)
benchmark_riffpex(BENCHMARK_DATASET_3, (25, 25, 25, 25, 40, 64),  "[9-digit base10 integers]", False)
benchmark_go_ff1(BENCHMARK_DATASET_3, 6, "[9-digit base10 integers]")
benchmark_go_ff3(BENCHMARK_DATASET_3, 6, "[9-digit base10 integers]")
benchmark_riffpe(BENCHMARK_DATASET_3, 10,   9, "[9-digit base10 integers]", True)
benchmark_riffpe(BENCHMARK_DATASET_3, 1000, 3, "[9-digit base10 integers]", True)
benchmark_riffpex(BENCHMARK_DATASET_3, (100, 100, 100, 1000),  "[9-digit base10 integers]", True)
benchmark_riffpex(BENCHMARK_DATASET_3, (50, 50, 40, 100, 100), "[9-digit base10 integers]", True)
benchmark_riffpex(BENCHMARK_DATASET_3, (50, 50, 50, 80, 100),  "[9-digit base10 integers]", True)
benchmark_riffpex(BENCHMARK_DATASET_3, (25, 25, 25, 25, 40, 64),  "[9-digit base10 integers]", True)
