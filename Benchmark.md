# Performance benchmark

Based on [pyriffpe/extras/benchmark.py](pyriffpe/extras/benchmark.py).

To get the full benchmark experience, the following extras are needed:

* Python FF3 implementation (package `ff3`)
* Python pyffx implementation (package `pyffx`)
* Go >= 1.15 for native ff1/ff3 implementations
* `pybindgen` Python package for ff1/ff3 `gopy` bindings
* `tqdm` (fully optional) for progress bars.

For benchmark and development, a Python virtual environment is recommended.
On Ubuntu (latest version tested is 20.04.x) the following steps can be executed
to reproduce our benchmark environment.

```bash
$ sudo add-apt-repository ppa:longsleep/golang-backports
$ sudo apt install python3-venv python3-dev golang cmake
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install pyffx ff3 tqdm pybindgen
(venv) $ pip install -e .
(venv) $ python pyriffpe/extras/make_fpe_bindings.py
```

Running a benchmark should be as easy as
```bash
(venv) $ python pyriffpe/extras/benchmark.py > benchmark.log
```

** Notes on tests and targets **
 * We always measure the full time of the Python interface call,
   which means it includes binding overheads for "native" targets.
 * Some Riffpe comfigurations are marked as *N/A*, when it's impossible
   to construct a Riffpe instance with given parameters, e.g. it's
   impossible to describe $Z_{10^{16}}$ as a product of $Z_{1000}$.

## Test platform 1

```
Apple MacBook Pro M2
CPU: Apple Silicon M2
RAM: 16GB
```

Times averaged for a series of 100'000 random samples.

#### Encryption time

Implementation                    | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
----------------------------------|------------------------------|------------------------------|---------------------------
pyffx                             | 23.771287 us                 | 26.151259 us                 | 30.365206 us
FF3 [Python]                      | 23.343398 us                 | 27.117016 us                 | 35.983204 us
Riffpe(n=10, bits=128) [Python]   | 72.781813 us                 | 108.593015 us                | 192.667101 us
Riffpe(n=10, bits=256) [Python]   | 79.697211 us                 | 119.061928 us                | 212.880398 us
Riffpe(n=100, bits=128) [Python]  | 164.678396 us                | *N/A*                        | 438.122885 us
Riffpe(n=100, bits=256) [Python]  | 196.128428 us                | *N/A*                        | 521.106696 us
RiffpeX(n>=16) [Python]           | *N/A*                        | *N/A*                        | 198.854048 us
RiffpeX(n>=25) [Python]           | 86.193679 us                 | 129.244296 us                | 217.392248 us
RiffpeX(n>=50) [Python]           | 160.550257 us                | 185.871242 us                | 316.071817 us
FF1 [Go]                          | 2.374235 us                  | 2.367646 us                  | 2.419654 us
FF3 [Go]                          | 3.674403 us                  | 3.893985 us                  | 4.243578 us
Riffpe(n=10, bits=128) [native]   | 2.370180 us                  | 3.386118 us                  | 6.054985 us
Riffpe(n=10, bits=256) [native]   | 3.419886 us                  | 4.956384 us                  | 8.892828 us
Riffpe(n=100, bits=128) [native]  | 20.142977 us                 | *N/A*                        | 52.849849 us
Riffpe(n=100, bits=256) [native]  | 25.469943 us                 | *N/A*                        | 67.095638 us
RiffpeX(n>=16) [native]           | *N/A*                        | *N/A*                        | 11.854018 us
RiffpeX(n>=25) [native]           | 7.052613 us                  | 10.377493 us                 | 16.316434 us
RiffpeX(n>=50) [native]           | 19.574949 us                 | 20.044119 us                 | 33.239442 us
Riffpe(n=1000, bits=128) [Python] | 1220.692968 us (1.220693 ms) | 1830.479550 us (1.830480 ms) | *N/A*
Riffpe(n=1000, bits=256) [Python] | 1428.247391 us (1.428247 ms) | 2143.005533 us (2.143006 ms) | *N/A*
Riffpe(n=1000, bits=128) [native] | 206.767853 us                | 309.354795 us                | *N/A*
Riffpe(n=1000, bits=256) [native] | 242.419345 us                | 362.545974 us                | *N/A*

#### Decryption time

Implementation                    | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
----------------------------------|------------------------------|------------------------------|---------------------------
pyffx                             | 23.817708 us                 | 26.171775 us                 | 30.445322 us
FF3 [Python]                      | 23.486135 us                 | 27.114400 us                 | 36.023587 us
Riffpe(n=10, bits=128) [Python]   | 73.260253 us                 | 109.346817 us                | 193.956006 us
Riffpe(n=10, bits=256) [Python]   | 80.202644 us                 | 120.031337 us                | 214.332410 us
Riffpe(n=100, bits=128) [Python]  | 140.006663 us                | *N/A*                        | 371.840534 us
Riffpe(n=100, bits=256) [Python]  | 171.200837 us                | *N/A*                        | 454.401572 us
RiffpeX(n>=16) [Python]           | *N/A*                        | *N/A*                        | 193.321630 us
RiffpeX(n>=25) [Python]           | 81.269123 us                 | 122.086123 us                | 206.633959 us
RiffpeX(n>=50) [Python]           | 135.792249 us                | 163.853049 us                | 279.970152 us
FF1 [Go]                          | 2.326717 us                  | 2.368340 us                  | 2.582242 us
FF3 [Go]                          | 3.769861 us                  | 3.975852 us                  | 4.336212 us
Riffpe(n=10, bits=128) [native]   | 2.158384 us                  | 3.100619 us                  | 5.563383 us
Riffpe(n=10, bits=256) [native]   | 3.217256 us                  | 4.677618 us                  | 8.396580 us
Riffpe(n=100, bits=128) [native]  | 13.887905 us                 | *N/A*                        | 40.397209 us
Riffpe(n=100, bits=256) [native]  | 19.203044 us                 | *N/A*                        | 54.641152 us
RiffpeX(n>=16) [native]           | *N/A*                        | *N/A*                        | 9.589786 us
RiffpeX(n>=25) [native]           | 5.087622 us                  | 7.587563 us                  | 12.272060 us
RiffpeX(n>=50) [native]           | 13.327268 us                 | 14.026538 us                 | 24.413812 us
Riffpe(n=1000, bits=128) [Python] | 815.231090 us                | 1222.838569 us (1.222839 ms) | *N/A*
Riffpe(n=1000, bits=256) [Python] | 1019.908595 us (1.019909 ms) | 1530.111879 us (1.530112 ms) | *N/A*
Riffpe(n=1000, bits=128) [native] | 195.454592 us                | 297.013788 us                | *N/A*
Riffpe(n=1000, bits=256) [native] | 231.019623 us                | 349.986654 us                | *N/A*

## Test platform 2

```
Apple MacBook Pro M3 
CPU: Apple Silicon M3
RAM: 36GB
```

TODO: FILL THIS SECTION (@Filip)

## Test platform 3

```
CPU: Intel(R) Xeon(R) CPU E3-1245 v5 @ 3.50GHz
RAM: 32GB RDIMM 2133 MHz
```

TODO: FILL THIS SECTION (@Marcin)

## Test platform 4

```
CPU: AMD Ryzen 9 8945HS
RAM: 96GB (2x48GB) DDR5 SODIMM (5600MT/s)
```

#### Encryption time

Implementation                    | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
----------------------------------|------------------------------|------------------------------|---------------------------
pyffx                             | 23.105714 us                 | 24.725058 us                 | 28.485387 us
FF3 [Python]                      | 22.505705 us                 | 26.369326 us                 | 34.442826 us
Riffpe(n=10, bits=128) [Python]   | 67.663375 us                 | 101.166630 us                | 181.045087 us
Riffpe(n=10, bits=256) [Python]   | 71.827372 us                 | 107.848894 us                | 197.102988 us
Riffpe(n=100, bits=128) [Python]  | 136.817155 us                | *N/A*                        | 368.674417 us
Riffpe(n=100, bits=256) [Python]  | 149.638760 us                | *N/A*                        | 409.989407 us
Riffpe(n=1000, bits=128) [Python] | 1046.226900 us (1.046227 ms) | 1563.597420 us (1.563597 ms) | *N/A*
Riffpe(n=1000, bits=256) [Python] | 1124.991937 us (1.124992 ms) | 1671.670677 us (1.671671 ms) | *N/A*
RiffpeX(n>=16) [Python]           | (same as n>=25)              | (same as n>=25)              | 181.986290 us
RiffpeX(n>=25) [Python]           | 76.065121 us                 | 112.213474 us                | 196.172222 us
RiffpeX(n>=50) [Python]           | 135.159190 us                | 157.331450 us                | 266.585100 us
FF1 [Go]                          | 2.123694 us                  | 2.134087 us                  | 2.207434 us
FF3 [Go]                          | 3.402187 us                  | 3.458394 us                  | 3.802456 us
Riffpe(n=10, bits=128) [native]   | 3.015068 us                  | 4.298574 us                  | 7.613413 us
Riffpe(n=10, bits=256) [native]   | 4.010009 us                  | 5.706375 us                  | 10.158612 us
Riffpe(n=100, bits=128) [native]  | 22.379749 us                 | *N/A*                        | 58.742591 us
Riffpe(n=100, bits=256) [native]  | 27.096927 us                 | *N/A*                        | 71.386285 us
Riffpe(n=1000, bits=128) [native] | 224.904350 us                | 338.503995 us                | *N/A*
Riffpe(n=1000, bits=256) [native] | 260.870285 us                | 398.683427 us                | *N/A*
RiffpeX(n>=16) [native]           | (same as n>=25)              | (same as n>=25)              | 14.433037 us
RiffpeX(n>=25) [native]           | 7.975489 us                  | 12.011093 us                 | 18.721568 us
RiffpeX(n>=50) [native]           | 21.834912 us                 | 22.804209 us                 | 37.493107 us

#### Decryption time

Implementation                    | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
----------------------------------|------------------------------|------------------------------|---------------------------
pyffx                             | 23.258079 us                 | 25.098495 us                 | 28.988131 us
FF3 [Python]                      | 22.702456 us                 | 26.402971 us                 | 34.313995 us
Riffpe(n=10, bits=128) [Python]   | 69.160220 us                 | 103.394348 us                | 185.091978 us
Riffpe(n=10, bits=256) [Python]   | 73.258916 us                 | 109.842794 us                | 201.012372 us
Riffpe(n=100, bits=128) [Python]  | 133.452143 us                | *N/A*                        | 368.132590 us
Riffpe(n=100, bits=256) [Python]  | 146.894381 us                | *N/A*                        | 410.065659 us
Riffpe(n=1000, bits=128) [Python] | 1087.940004 us (1.087940 ms) | 1631.797280 us (1.631797 ms) | *N/A*
Riffpe(n=1000, bits=256) [Python] | 1167.228261 us (1.167228 ms) | 1738.814028 us (1.738814 ms) | *N/A*
RiffpeX(n>=16) [Python]           | (same as n>=25)              | (same as n>=25)              | 183.651342 us
RiffpeX(n>=25) [Python]           | 75.494382 us                 | 111.680933 us                | 196.438942 us
RiffpeX(n>=50) [Python]           | 131.685622 us                | 154.882366 us                | 264.984849 us
FF1 [Go]                          | 2.151855 us                  | 2.171542 us                  | 2.277153 us
FF3 [Go]                          | 3.567974 us                  | 3.630301 us                  | 3.982222 us
Riffpe(n=10, bits=128) [native]   | 2.657507 us                  | 3.811840 us                  | 6.873059 us
Riffpe(n=10, bits=256) [native]   | 3.699591 us                  | 5.288134 us                  | 9.460515 us
Riffpe(n=100, bits=128) [native]  | 17.814810 us                 | *N/A*                        | 48.949597 us
Riffpe(n=100, bits=256) [native]  | 22.501884 us                 | *N/A*                        | 61.721819 us
Riffpe(n=1000, bits=128) [native] | 204.758564 us                | 318.007250 us                | *N/A*
Riffpe(n=1000, bits=256) [native] | 240.200814 us                | 377.797873 us                | *N/A*
RiffpeX(n>=16) [native]           | (same as n>=25)              | (same as n>=25)              | 11.922651 us
RiffpeX(n>=25) [native]           | 6.439258 us                  | 9.757706 us                  | 15.439215 us
RiffpeX(n>=50) [native]           | 17.153353 us                 | 18.174779 us                 | 30.546182 us

---

### Optimizations

* **native**: Reimplemented permutation with `std::nth_element` (QuickSelect) and a simple rank algorithm (linear sum of smaller elements)
* **Python**: Implemented simple rank algorithm. Manual QuickSelect seems to be slower than a naiive sort-and-select. To be investigated.

#### Encryption time

Implementation                    | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
----------------------------------|------------------------------|------------------------------|---------------------------
pyffx                             | 23.139748 us                 | 24.394683 us                 | 27.835407 us
FF3 [Python]                      | 22.570189 us                 | 26.002940 us                 | 33.824476 us
Riffpe(n=10, bits=128) [Python]   | 69.597180 us                 | 104.588297 us                | 181.113943 us
Riffpe(n=10, bits=256) [Python]   | 72.944629 us                 | 110.532432 us                | 193.126503 us
Riffpe(n=100, bits=128) [Python]  | 139.789665 us                | *N/A*                        | 366.563611 us
Riffpe(n=100, bits=256) [Python]  | 155.044022 us                | *N/A*                        | 414.890974 us
Riffpe(n=1000, bits=128) [Python] | 1040.265357 us (1.040265 ms) | 1570.219933 us (1.570220 ms) | *N/A*
Riffpe(n=1000, bits=256) [Python] | 1130.949439 us (1.130949 ms) | 1707.850404 us (1.707850 ms) | *N/A*
RiffpeX(n>=16) [Python]           | (same as n>=25)              | (same as n>=25)              | 180.400996 us
RiffpeX(n>=25) [Python]           | 77.333545 us                 | 114.776140 us                | 194.357771 us
RiffpeX(n>=50) [Python]           | 139.850895 us                | 160.135945 us                | 271.529234 us
FF1 [Go]                          | 2.293371 us                  | 2.365901 us                  | 2.420372 us
FF3 [Go]                          | 3.725901 us                  | 3.762887 us                  | 3.880713 us
Riffpe(n=10, bits=128) [native]   | 2.983664 us                  | 4.322063 us                  | 7.554765 us
Riffpe(n=10, bits=256) [native]   | 3.986008 us                  | 5.718703 us                  | 10.353791 us
Riffpe(n=100, bits=128) [native]  | 12.446001 us                 | *N/A*                        | 32.938137 us
Riffpe(n=100, bits=256) [native]  | 17.526798 us                 | *N/A*                        | 46.144274 us
Riffpe(n=1000, bits=128) [native] | 78.643751 us                 | 119.729319 us                | *N/A*
Riffpe(n=1000, bits=256) [native] | 111.786687 us                | 168.464085 us                | *N/A*
RiffpeX(n>=16) [native]           | (same as n>=25)              | (same as n>=25)              | 11.998398 us
RiffpeX(n>=25) [native]           | 5.859920 us                  | 8.896056 us                  | 14.235193 us
RiffpeX(n>=50) [native]           | 11.933764 us                 | 13.779151 us                 | 22.783375 us

#### Decryption time

Implementation                    | [6-digit base10 integers] | [9-digit base10 integers]    | [16-digit base10 integers]
----------------------------------|---------------------------|------------------------------|---------------------------
pyffx                             | 23.346388 us              | 24.790187 us                 | 28.403810 us
FF3 [Python]                      | 22.793230 us              | 26.106201 us                 | 33.692771 us
Riffpe(n=10, bits=128) [Python]   | 69.485338 us              | 104.010607 us                | 180.160010 us
Riffpe(n=10, bits=256) [Python]   | 72.698797 us              | 110.219295 us                | 192.525166 us
Riffpe(n=100, bits=128) [Python]  | 112.047264 us             | *N/A*                        | 293.999904 us
Riffpe(n=100, bits=256) [Python]  | 125.056049 us             | *N/A*                        | 341.262352 us
Riffpe(n=1000, bits=128) [Python] | 638.081180 us             | 967.829657 us                | *N/A*
Riffpe(n=1000, bits=256) [Python] | 728.086686 us             | 1101.244089 us (1.101244 ms) | *N/A*
RiffpeX(n>=16) [Python]           | (same as n>=25)           | (same as n>=25)              | 172.849581 us
RiffpeX(n>=25) [Python]           | 71.349146 us              | 105.879938 us                | 181.293965 us
RiffpeX(n>=50) [Python]           | 109.375273 us             | 134.550654 us                | 230.387097 us
FF1 [Go]                          | 2.361293 us               | 2.476037 us                  | 2.360733 us
FF3 [Go]                          | 3.963232 us               | 3.930016 us                  | 4.064471 us
Riffpe(n=10, bits=128) [native]   | 2.189146 us               | 3.177668 us                  | 5.554533 us
Riffpe(n=10, bits=256) [native]   | 3.353297 us               | 4.956192 us                  | 8.812060 us
Riffpe(n=100, bits=128) [native]  | 7.985180 us               | *N/A*                        | 20.945183 us
Riffpe(n=100, bits=256) [native]  | 13.141864 us              | *N/A*                        | 34.360725 us
Riffpe(n=1000, bits=128) [native] | 53.245535 us              | 80.906444 us                 | *N/A*
Riffpe(n=1000, bits=256) [native] | 86.071989 us              | 129.779775 us                | *N/A*
RiffpeX(n>=16) [native]           | (same as n>=25)           | (same as n>=25)              | 7.612637 us
RiffpeX(n>=25) [native]           | 3.665733 us               | 5.549970 us                  | 8.935720 us
RiffpeX(n>=50) [native]           | 7.372530 us               | 8.531533 us                  | 14.040910 us

