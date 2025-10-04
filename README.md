# Riffpe - a Riffle-Shuffle-based Format Preserving Encryption

[![Wheels](https://github.com/filipzz/riffpe/actions/workflows/wheels.yml/badge.svg)](https://github.com/filipzz/riffpe/actions/workflows/wheels.yml)

This repository contains the following:
 * an optimized C++17 implementation of Riffpe in form of a simple library (libriffpe)
 * a pure Python implementation of riffpe (pyriffpe/riffpe/_fallback)
 * Python bindings to libriffpe (pyriffpe/riffpe/_native)
 * Python-based CLI for Riffpe (using either libriffpe bindings or fallback implementation)


## Requirements

 * For the C++ code, all you need is CMake (at least 3.18), C++ compiler supporting at least C++17, and a supported build system (e.g. Ninja, GNU Make, MSBuild)
 * For Python bindings, C++ compiler ought to be enough, as CMake and Ninja are being pulled in by setuptools during package build and thus do not need to be present in the system. At least Python 3.7 is required.
 * For pure Python implementation, PyCryptodome package is required (will be pulled automatically with `pip install`).

## Installation

[TBD]

To install full developement version from source issue:

```bash
pip install -e .[tests,benchmark]
```

This should pull all required build dependencies.

## Usage

As a standalone module:

Message encryption:

```bash
$ python -m riffpe.encrypt -k 00112233445566778899aabbccddeeff -n 100 -l 8 1234123456785678
3123769254898119
```

Message decryption:

```bash
$ python -m riffpe.decrypt -k 00112233445566778899aabbccddeeff -n 100 -l 8 3123769254898119
1234123456785678
```

The input messages are treated as integers and sliced in a little-endian order; big-endian order
may be requested by providing `-B` switch:

```bash
$ python -m riffpe.encrypt -k 00112233445566778899aabbccddeeff -n 100 -l 8 1234123456785678
3123769254898119

$ python -m riffpe.encrypt -k 00112233445566778899aabbccddeeff -n 100 -l 8 7856785634123412 -B
1981895492762331
```

**Note**: `3594761421525475` is `7554522114769435` in reverse (in chunks of 2 digits, since $n=100$), just as `7856785634123412` is `1234123456785678`.

```bash
$ python -m riffpe.encrypt -k 00112233445566778899aabbccddeeff -n 100 -l 8 7766554433221100 -t 416C696365
2601183984852660
```

Currently tag (`-t`) must be passed as a hex string.
In future, possibly another option will allow ASCII or UTF-8 encoding.
In the example above, tag `416C696365` corresponds to an ASCII string `"Alice"`.

As a Python module:

```python
from riffpe import Riffpe

fpe = Riffpe(
    radix=100, 
    digits=8, 
    key=bytes.fromhex("00112233445566778899aabbccddeeff"),
    tweak=b'',
)

ptx = [78, 56, 78, 56, 34, 12, 34, 12]

ctx = fpe.encrypt(ptx)
print("ctx:", ctx)

ptx = fpe.decrypt(ctx)
print("ptx:", ptx)
```

Output:

```python
ctx: [19, 81, 89, 54, 92, 76, 23, 31]
ptx: [78, 56, 78, 56, 34, 12, 34, 12]
```

## Testing

```bash
pytest pyriffpe/tests
```

## Performance

Benchmarks and comparison to other FPEs are available [here](Benchmark.md).
