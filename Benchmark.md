# Performance benchmark

Based on [pyriffpe/extras/benchmark.py](pyriffpe/extras/benchmark.py).

## Test platform 1
```
CPU: Intel(R) Core(TM) i7-6700K CPU @ 4.00GHz
RAM: 64GB DDR4-2132 (1066 MHz)
```

Times averaged for a series of 10'000 random samples.

**Encryption time**

Implementation           | [16-digit base10 integers]     | [6-digit base10 integers]
-------------------------|--------------------------------|-----------------------------
FF3 [Python]             | 90.367700 us                   | 64.127110 us
pyffx                    | 67.643850 us                   | 54.155790 us
Riffpe(n=10) [Python]    | 549.762150 us                  | 161.267500 us
Riffpe(n=100) [Python]   | 681.253030 us                  | 253.850940 us
Riffpe(n=1000) [Python]  | *N/A*                          | 1658.702650 us (1.658703 ms)
Riffpe(n=10000) [Python] | 47062.520800 us (47.062521 ms) | *N/A*
Riffpe(n=10) [native]    | 12.623010 us                   | 6.445900 us
Riffpe(n=100) [native]   | 82.596880 us                   | 32.412870 us
Riffpe(n=1000) [native]  | *N/A*                          | 301.486250 us
Riffpe(n=10000) [native] | 10575.390540 us (10.575391 ms) | *N/A*

**Decryption time**

Implementation           | [16-digit base10 integers]     | [6-digit base10 integers]
-------------------------|--------------------------------|-----------------------------
FF3 [Python]             | 90.600350 us                   | 64.949270 us
pyffx                    | 69.823730 us                   | 54.481060 us
Riffpe(n=10) [Python]    | 560.230650 us                  | 165.239480 us
Riffpe(n=100) [Python]   | 715.503930 us                  | 267.344040 us
Riffpe(n=1000) [Python]  | *N/A*                          | 1746.314170 us (1.746314 ms)
Riffpe(n=10000) [Python] | 47949.220560 us (47.949221 ms) | *N/A*
Riffpe(n=10) [native]    | 12.336620 us                   | 5.917750 us
Riffpe(n=100) [native]   | 80.591830 us                   | 30.509740 us
Riffpe(n=1000) [native]  | *N/A*                          | 302.928070 us
Riffpe(n=10000) [native] | 10563.137610 us (10.563138 ms) | *N/A*
