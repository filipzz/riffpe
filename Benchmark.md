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
pyffx                             | 23.986675 us                 | 25.922250 us                 | 30.177591 us
FF3 [Python]                      | 23.328708 us                 | 27.125796 us                 | 35.627292 us
Riffpe(n=10, bits=128) [Python]   | 72.944278 us                 | 109.368088 us                | 193.670763 us
Riffpe(n=10, bits=256) [Python]   | 79.811570 us                 | 119.283939 us                | 213.779783 us
Riffpe(n=100, bits=128) [Python]  | 167.974206 us                | *N/A*                        | 438.232856 us
Riffpe(n=100, bits=256) [Python]  | 196.889231 us                | *N/A*                        | 521.886724 us
Riffpe(n=1000, bits=128) [Python] | 1223.411313 us (1.223411 ms) | 1833.370415 us (1.833370 ms) | *N/A*
Riffpe(n=1000, bits=256) [Python] | 1429.298053 us (1.429298 ms) | 2147.437106 us (2.147437 ms) | *N/A*
RiffpeX(n>=16) [Python]           | (same as n>=25)              | (same as n>=25)              | 198.315712 us
RiffpeX(n>=25) [Python]           | 87.530259 us                 | 128.921013 us                | 217.632803 us
RiffpeX(n>=50) [Python]           | 162.500604 us                | 186.222248 us                | 317.529287 us
FF1 [Go]                          | 2.255994 us                  | 2.467973 us                  | 2.486744 us
FF3 [Go]                          | 3.700888 us                  | 3.859843 us                  | 4.265790 us
Riffpe(n=10, bits=128) [native]   | 2.005893 us                  | 2.862563 us                  | 5.189446 us
Riffpe(n=10, bits=256) [native]   | 2.990992 us                  | 4.345100 us                  | 7.767793 us
Riffpe(n=100, bits=128) [native]  | 7.622132 us                  | *N/A*                        | 19.831987 us
Riffpe(n=100, bits=256) [native]  | 13.005485 us                 | *N/A*                        | 34.195808 us
Riffpe(n=1000, bits=128) [native] | 46.915452 us                 | 69.878372 us                 | *N/A*
Riffpe(n=1000, bits=256) [native] | 82.968575 us                 | 123.566494 us                | *N/A*
RiffpeX(n>=16) [native]           | (same as n>=25)              | (same as n>=25)              | 6.471367 us
RiffpeX(n>=25) [native]           | 3.304088 us                  | 4.778295 us                  | 7.722564 us
RiffpeX(n>=50) [native]           | 6.919603 us                  | 7.691419 us                  | 12.814129 us

#### Decryption time

Implementation                    | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
----------------------------------|------------------------------|------------------------------|---------------------------
pyffx                             | 24.069491 us                 | 25.936587 us                 | 30.316469 us
FF3 [Python]                      | 23.472538 us                 | 27.130119 us                 | 35.626886 us
Riffpe(n=10, bits=128) [Python]   | 73.290750 us                 | 109.536324 us                | 194.189477 us
Riffpe(n=10, bits=256) [Python]   | 80.067122 us                 | 119.730503 us                | 214.411119 us
Riffpe(n=100, bits=128) [Python]  | 139.801279 us                | *N/A*                        | 370.253044 us
Riffpe(n=100, bits=256) [Python]  | 171.481979 us                | *N/A*                        | 454.146775 us
Riffpe(n=1000, bits=128) [Python] | 816.978203 us                | 1225.713086 us (1.225713 ms) | *N/A*
Riffpe(n=1000, bits=256) [Python] | 1022.046901 us (1.022047 ms) | 1534.294882 us (1.534295 ms) | *N/A*
RiffpeX(n>=16) [Python]           | (same as n>=25)              | (same as n>=25)              | 192.244599 us
RiffpeX(n>=25) [Python]           | 81.672979 us                 | 121.497848 us                | 206.473740 us
RiffpeX(n>=50) [Python]           | 136.704060 us                | 163.877664 us                | 280.384673 us
FF1 [Go]                          | 2.357159 us                  | 2.353173 us                  | 2.499110 us
FF3 [Go]                          | 3.765311 us                  | 3.977038 us                  | 4.323057 us
Riffpe(n=10, bits=128) [native]   | 2.170045 us                  | 3.138200 us                  | 5.646081 us
Riffpe(n=10, bits=256) [native]   | 3.376339 us                  | 4.906957 us                  | 8.818825 us
Riffpe(n=100, bits=128) [native]  | 7.830081 us                  | *N/A*                        | 20.407423 us
Riffpe(n=100, bits=256) [native]  | 13.249540 us                 | *N/A*                        | 34.820909 us
Riffpe(n=1000, bits=128) [native] | 52.783291 us                 | 79.008595 us                 | *N/A*
Riffpe(n=1000, bits=256) [native] | 88.560567 us                 | 132.544293 us                | *N/A*
RiffpeX(n>=16) [native]           | (same as n>=25)              | (same as n>=25)              | 6.653816 us
RiffpeX(n>=25) [native]           | 3.420754 us                  | 4.887298 us                  | 7.914811 us
RiffpeX(n>=50) [native]           | 7.151066 us                  | 7.877444 us                  | 13.172881 us

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

#### Encryption time

Implementation                    | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
----------------------------------|------------------------------|------------------------------|---------------------------
pyffx                             | 41.408022 us                 | 44.416960 us                 | 50.212452 us
FF3 [Python]                      | 40.999134 us                 | 46.024236 us                 | 61.027176 us
Riffpe(n=10, bits=128) [Python]   | 119.072819 us                | 175.451752 us                | 309.192943 us
Riffpe(n=10, bits=256) [Python]   | 124.599243 us                | 184.961407 us                | 327.026799 us
Riffpe(n=100, bits=128) [Python]  | 239.957794 us                | *N/A*                        | 623.778976 us
Riffpe(n=100, bits=256) [Python]  | 255.921758 us                | *N/A*                        | 666.933579 us
Riffpe(n=1000, bits=128) [Python] | 1742.561652 us (1.742562 ms) | 2604.598909 us (2.604599 ms) | *N/A*
Riffpe(n=1000, bits=256) [Python] | 1836.671421 us (1.836671 ms) | 2740.352766 us (2.740353 ms) | *N/A*
RiffpeX(n>=16) [Python]           | (same as n>=25)              | (same as n>=25)              | 312.961270 us
RiffpeX(n>=25) [Python]           | 136.587852 us                | 199.756237 us                | 336.345130 us
RiffpeX(n>=50) [Python]           | 237.998897 us                | 296.997175 us                | 485.008395 us
FF1 [Go]                          | 625.604180 us                | 620.845468 us                | 615.167518 us
FF3 [Go]                          | 619.071061 us                | 615.262235 us                | 611.513789 us
Riffpe(n=10, bits=128) [native]   | 3.495294 us                  | 4.935844 us                  | 9.186180 us
Riffpe(n=10, bits=256) [native]   | 4.846486 us                  | 7.186416 us                  | 12.325696 us
Riffpe(n=100, bits=128) [native]  | 10.805593 us                 | *N/A*                        | 27.933820 us
Riffpe(n=100, bits=256) [native]  | 17.509933 us                 | *N/A*                        | 45.898409 us
Riffpe(n=1000, bits=128) [native] | 71.659402 us                 | 108.736516 us                | *N/A*
Riffpe(n=1000, bits=256) [native] | 117.571950 us                | 176.544545 us                | *N/A*
RiffpeX(n>=16) [native]           | (same as n>=25)              | (same as n>=25)              | 10.410785 us
RiffpeX(n>=25) [native]           | 4.889667 us                  | 7.033049 us                  | 11.742551 us
RiffpeX(n>=50) [native]           | 10.282131 us                 | 11.217021 us                 | 19.549364 us

#### Decryption time

Implementation                    | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
----------------------------------|------------------------------|------------------------------|---------------------------
pyffx                             | 41.670416 us                 | 45.102544 us                 | 50.690603 us
FF3 [Python]                      | 40.842391 us                 | 45.913423 us                 | 60.716376 us
Riffpe(n=10, bits=128) [Python]   | 117.436505 us                | 173.554920 us                | 306.250726 us
Riffpe(n=10, bits=256) [Python]   | 123.151585 us                | 182.441704 us                | 324.746811 us
Riffpe(n=100, bits=128) [Python]  | 186.849073 us                | *N/A*                        | 482.556699 us
Riffpe(n=100, bits=256) [Python]  | 203.612707 us                | *N/A*                        | 525.881108 us
Riffpe(n=1000, bits=128) [Python] | 1026.767232 us (1.026767 ms) | 1522.273540 us (1.522274 ms) | *N/A*
Riffpe(n=1000, bits=256) [Python] | 1118.923542 us (1.118924 ms) | 1661.723999 us (1.661724 ms) | *N/A*
RiffpeX(n>=16) [Python]           | (same as n>=25)              | (same as n>=25)              | 294.143108 us
RiffpeX(n>=25) [Python]           | 123.558616 us                | 179.612331 us                | 306.274506 us
RiffpeX(n>=50) [Python]           | 184.945671 us                | 243.878089 us                | 400.208776 us
FF1 [Go]                          | 624.986998 us                | 619.530469 us                | 614.818892 us
FF3 [Go]                          | 619.771427 us                | 617.903084 us                | 611.810919 us
Riffpe(n=10, bits=128) [native]   | 3.223272 us                  | 4.526722 us                  | 7.989806 us
Riffpe(n=10, bits=256) [native]   | 4.825680 us                  | 7.150299 us                  | 12.353127 us
Riffpe(n=100, bits=128) [native]  | 11.338306 us                 | *N/A*                        | 29.729686 us
Riffpe(n=100, bits=256) [native]  | 18.619082 us                 | *N/A*                        | 49.084760 us
Riffpe(n=1000, bits=128) [native] | 73.943905 us                 | 110.797139 us                | *N/A*
Riffpe(n=1000, bits=256) [native] | 122.083227 us                | 181.808847 us                | *N/A*
RiffpeX(n>=16) [native]           | (same as n>=25)              | (same as n>=25)              | 10.179754 us
RiffpeX(n>=25) [native]           | 5.090384 us                  | 7.248719 us                  | 11.893546 us
RiffpeX(n>=50) [native]           | 10.436762 us                 | 11.641393 us                 | 19.650762 us

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


## Test platform 5

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
