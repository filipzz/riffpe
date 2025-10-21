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

TODO: FILL THIS SECTION (@Marcin)

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


## Test platform 4

```
CPU: INTEL(R) XEON(R) GOLD 6548Y+
RAM: 1TB
```

#### Encryption time
Implementation                    | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
----------------------------------|------------------------------|------------------------------|---------------------------
pyffx                             | 26.478382 us                 | 28.600857 us                 | 39.176199 us              
FF3 [Python]                      | 24.831804 us                 | 29.217218 us                 | 40.095383 us              
Riffpe(n=10, bits=128) [Python]   | 71.823785 us                 | 107.655898 us                | 188.132250 us             
Riffpe(n=10, bits=256) [Python]   | 74.456805 us                 | 111.093605 us                | 196.268914 us             
Riffpe(n=100, bits=128) [Python]  | 145.212553 us                | *N/A*                        | 383.684576 us             
Riffpe(n=100, bits=256) [Python]  | 154.461201 us                | *N/A*                        | 411.301654 us             
RiffpeX(n>=16) [Python]           | *N/A*                        | *N/A*                        | 190.833926 us             
RiffpeX(n>=25) [Python]           | 81.878578 us                 | 122.950456 us                | 208.294153 us             
RiffpeX(n>=50) [Python]           | 143.984033 us                | 169.215109 us                | 289.362936 us             
FF1 [Go]                          | 2.796187 us                  | 4.543075 us                  | 2.991075 us               
FF3 [Go]                          | 4.833251 us                  | 7.909179 us                  | 5.515112 us               
Riffpe(n=10, bits=128) [native]   | 3.315505 us                  | 7.717045 us                  | 8.412343 us               
Riffpe(n=10, bits=256) [native]   | 4.302174 us                  | 7.349120 us                  | 11.039188 us              
Riffpe(n=100, bits=128) [native]  | 26.838601 us                 | *N/A*                        | 69.179410 us              
Riffpe(n=100, bits=256) [native]  | 31.739854 us                 | *N/A*                        | 82.231671 us              
RiffpeX(n>=16) [native]           | *N/A*                        | *N/A*                        | 17.198508 us              
RiffpeX(n>=25) [native]           | 9.825331 us                  | 14.279600 us                 | 22.305598 us              
RiffpeX(n>=50) [native]           | 26.522209 us                 | 27.045195 us                 | 44.636597 us              
Riffpe(n=1000, bits=128) [Python] | 1072.015620 us (1.072016 ms) | 1607.471896 us (1.607472 ms) | *N/A*                     
Riffpe(n=1000, bits=256) [Python] | 1137.794407 us (1.137794 ms) | 1711.760555 us (1.711761 ms) | *N/A*                     
Riffpe(n=1000, bits=128) [native] | 266.763668 us                | 401.517187 us                | *N/A*                     
Riffpe(n=1000, bits=256) [native] | 301.613338 us                | 451.312203 us                | *N/A*  


#### Decryption time
Implementation                    | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
----------------------------------|------------------------------|------------------------------|---------------------------
pyffx                             | 26.491399 us                 | 28.898710 us                 | 39.548984 us              
FF3 [Python]                      | 24.907453 us                 | 28.942596 us                 | 39.537928 us              
Riffpe(n=10, bits=128) [Python]   | 72.787314 us                 | 108.958803 us                | 191.121964 us             
Riffpe(n=10, bits=256) [Python]   | 76.651766 us                 | 114.567980 us                | 203.506200 us             
Riffpe(n=100, bits=128) [Python]  | 147.166255 us                | *N/A*                        | 393.931483 us             
Riffpe(n=100, bits=256) [Python]  | 156.239330 us                | *N/A*                        | 421.916715 us             
RiffpeX(n>=16) [Python]           | *N/A*                        | *N/A*                        | 197.257581 us             
RiffpeX(n>=25) [Python]           | 83.335609 us                 | 125.613729 us                | 215.237159 us             
RiffpeX(n>=50) [Python]           | 146.214167 us                | 173.196948 us                | 297.818082 us             
FF1 [Go]                          | 2.885318 us                  | 4.638932 us                  | 3.129520 us               
FF3 [Go]                          | 4.877182 us                  | 8.029456 us                  | 5.466896 us               
Riffpe(n=10, bits=128) [native]   | 3.259471 us                  | 7.609884 us                  | 8.365069 us               
Riffpe(n=10, bits=256) [native]   | 4.265693 us                  | 7.284247 us                  | 10.991648 us              
Riffpe(n=100, bits=128) [native]  | 23.240337 us                 | *N/A*                        | 64.428312 us              
Riffpe(n=100, bits=256) [native]  | 28.145284 us                 | *N/A*                        | 77.442788 us              
RiffpeX(n>=16) [native]           | *N/A*                        | *N/A*                        | 15.766533 us              
RiffpeX(n>=25) [native]           | 8.332429 us                  | 12.503286 us                 | 20.457415 us              
RiffpeX(n>=50) [native]           | 22.814811 us                 | 23.867226 us                 | 40.880301 us              
Riffpe(n=1000, bits=128) [Python] | 1116.389468 us (1.116389 ms) | 1674.069057 us (1.674069 ms) | *N/A*                     
Riffpe(n=1000, bits=256) [Python] | 1182.374738 us (1.182375 ms) | 1778.494243 us (1.778494 ms) | *N/A*                     
Riffpe(n=1000, bits=128) [native] | 261.092573 us                | 395.415301 us                | *N/A*                     
Riffpe(n=1000, bits=256) [native] | 296.164701 us                | 445.294767 us                | *N/A*                     
