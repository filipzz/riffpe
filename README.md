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
pip install -e .
```

This should pull all required build dependencies.

## Usage

As a standalone module:

Message encryption:

```bash
$ python -m riffpe.encrypt -k 00112233445566778899aabbccddeeff -n 100 -l 8 1234123456785678
0914050408195228
```

Message decryption:

```bash
$ python -m riffpe.decrypt -k 00112233445566778899aabbccddeeff -n 100 -l 8 0914050408195228
1234123456785678
```

The input messages are treated as integers and sliced in a little-endian order; big-endian order
may be requested by providing `-B` switch:

```bash
$ python -m riffpe.encrypt -k 00112233445566778899aabbccddeeff -n 100 -l 8 1234123456785678
0914050408195228

$ python -m riffpe.encrypt -k 00112233445566778899aabbccddeeff -n 100 -l 8 7856785634123412 -B
2852190804051409
```

**Note**: `2852190804051409` is `0914050408195228` in reverse (in chunks of 2 digits, since $n=100$), just as `7856785634123412` is `1234123456785678`.

```bash
$ python -m riffpe.encrypt -k 00112233445566778899aabbccddeeff -n 100 -l 8 7766554433221100 -t 416C696365
6396218874103160
```

Currently tag (`-T`) must be passed as a hex string.
In future, possibly another option will allow ASCII or UTF-8 encoding.
In the example above, tag `416C696365` corresponds to an ASCII string `"Alice"`.


As a Python module:

```python
from riffpe import Riffpe

#            n    l  key                                                tag
fpe = Riffpe(100, 8, bytes.fromhex("00112233445566778899aabbccddeeff"), b'')

ptx = [78, 56, 78, 56, 34, 12, 34, 12]

ctx = fpe.enc(ptx)
print("ctx:", ctx)

ptx = fpe.dec(ctx)
print("ptx:", ptx)
```

Output:
```
ctx: [28, 52, 19, 8, 4, 5, 14, 9]
ptx: [78, 56, 78, 56, 34, 12, 34, 12]
```

## Testing

[TBD]

## Performance

Benchmarks and comparison to other FPE are available [here](Benchmark.md).
