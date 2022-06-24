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
pyffx                    | 61.408470 us                   | 51.239390 us
FF3 [Python]             | 88.058340 us                   | 55.256050 us
Riffpe(n=10) [Python]    | 504.753340 us                  | 151.468660 us
Riffpe(n=100) [Python]   | 629.292110 us                  | 229.061280 us
Riffpe(n=1000) [Python]  | *N/A*                          | 1511.271110 us (1.511271 ms)
Riffpe(n=10000) [Python] | 40336.441230 us (40.336441 ms) | *N/A*
FF1 [Go]                 | 23.430800 us                   | 23.118320 us
FF3 [Go]                 | 26.509180 us                   | 25.599320 us
Riffpe(n=10) [native]    | 10.442720 us                   | 4.926270 us
Riffpe(n=100) [native]   | 77.466980 us                   | 30.020990 us
Riffpe(n=1000) [native]  | *N/A*                          | 281.163130 us
Riffpe(n=10000) [native] | 7662.221550 us (7.662222 ms)   | *N/A*

**Decryption time**

Implementation           | [16-digit base10 integers]     | [6-digit base10 integers]
-------------------------|--------------------------------|-----------------------------
pyffx                    | 61.886340 us                   | 51.527610 us
FF3 [Python]             | 87.641110 us                   | 55.257010 us
Riffpe(n=10) [Python]    | 516.879950 us                  | 155.836860 us
Riffpe(n=100) [Python]   | 658.386430 us                  | 237.949840 us
Riffpe(n=1000) [Python]  | *N/A*                          | 1588.954800 us (1.588955 ms)
Riffpe(n=10000) [Python] | 42147.792200 us (42.147792 ms) | *N/A*
FF1 [Go]                 | 23.218540 us                   | 23.011220 us
FF3 [Go]                 | 26.438190 us                   | 25.396150 us
Riffpe(n=10) [native]    | 10.267440 us                   | 4.758810 us
Riffpe(n=100) [native]   | 75.578240 us                   | 28.437200 us
Riffpe(n=1000) [native]  | *N/A*                          | 282.840870 us
Riffpe(n=10000) [native] | 7744.897080 us (7.744897 ms)   | *N/A*
