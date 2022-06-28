# Performance benchmark

Based on [pyriffpe/extras/benchmark.py](pyriffpe/extras/benchmark.py).

To get the full benchmark experience, the following extras are needed:

* Python FF3 implementation (package `ff3`)
* Python pyffx implementation (package `pyffx`)
* Go >= 1.15

For benchmark and development, a Python virtual environment is recommended.
On Ubuntu (latest version tested is 20.04.x) the following steps can be executed
to reproduce our benchmark environment.

```
$ sudo add-apt-repository ppa:longsleep/golang-backports
$ sudo apt install python3-venv golang
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install pyffx ff3 tqdm pybindgen
(venv) $ pip install -e .
(venv) $ python pyriffpe/extras/make_fpe_bindings.py
```

Running a benchmark should be as easy as
```
(venv) $ python pyriffpe/extras/benchmark.py > benchmark.log
```


## Test platform 1
```
CPU: Intel(R) Core(TM) i7-6700K CPU @ 4.00GHz
RAM: 64GB DDR4-2132 (1066 MHz)
```

Times averaged for a series of 100'000 random samples.

**Encryption time**

Implementation                           | [16-digit base10 integers]     | [9-digit base10 integers]    | [6-digit base10 integers]
-----------------------------------------|--------------------------------|------------------------------|-----------------------------
pyffx                                    | 62.301488 us                   | 56.444979 us                 | 53.430268 us
FF3 [Python]                             | 87.207420 us                   | 63.921682 us                 | 55.944852 us
Riffpe(n=10) [Python]                    | 332.825165 us                  | 187.357098 us                | 128.548088 us
Riffpe(n=100) [Python]                   | 584.446348 us                  | *N/A*                        | 223.974444 us
Riffpe(n=1000) [Python]                  | *N/A*                          | 2273.019131 us (2.273019 ms) | 1514.839518 us (1.514840 ms)
Riffpe(n=10000) [Python]                 | 43690.803584 us (43.690804 ms) | *N/A*                        | *N/A*
RiffpeX(100, 100, 100, 1000) [Python]    | *N/A*                          | 980.284731 us                | *N/A*
RiffpeX(50, 50, 40, 100, 100) [Python]   | *N/A*                          | 274.612539 us                | *N/A*
RiffpeX(50, 50, 50, 80, 100) [Python]    | *N/A*                          | 266.662054 us                | *N/A*
RiffpeX(25, 25, 25, 25, 40, 64) [Python] | *N/A*                          | 204.370561 us                | *N/A*
FF1 [Go]                                 | 24.707515 us                   | 25.225752 us                 | 24.275316 us
FF3 [Go]                                 | 29.257298 us                   | 28.522861 us                 | 29.219470 us
Riffpe(n=10) [native]                    | 9.893939 us                    | 6.264304 us                  | 4.763808 us
Riffpe(n=100) [native]                   | 72.041398 us                   | *N/A*                        | 28.422461 us
Riffpe(n=1000) [native]                  | *N/A*                          | 408.182716 us                | 272.896927 us
Riffpe(n=10000) [native]                 | 7509.478950 us (7.509479 ms)   | *N/A*                        | *N/A*
RiffpeX(100, 100, 100, 1000) [native]    | *N/A*                          | 166.522985 us                | *N/A*
RiffpeX(50, 50, 40, 100, 100) [native]   | *N/A*                          | 30.871058 us                 | *N/A*
RiffpeX(50, 50, 50, 80, 100) [native]    | *N/A*                          | 29.483050 us                 | *N/A*
RiffpeX(25, 25, 25, 25, 40, 64) [native] | *N/A*                          | 17.346733 us                 | *N/A*


**Decryption time**

Implementation                           | [16-digit base10 integers]     | [9-digit base10 integers]    | [6-digit base10 integers]
-----------------------------------------|--------------------------------|------------------------------|-----------------------------
pyffx                                    | 63.115158 us                   | 56.850320 us                 | 53.833200 us
FF3 [Python]                             | 87.236098 us                   | 63.887724 us                 | 56.071366 us
Riffpe(n=10) [Python]                    | 344.455869 us                  | 193.852680 us                | 133.184275 us
Riffpe(n=100) [Python]                   | 614.470735 us                  | *N/A*                        | 233.158090 us
Riffpe(n=1000) [Python]                  | *N/A*                          | 2391.248397 us (2.391248 ms) | 1595.207327 us (1.595207 ms)
Riffpe(n=10000) [Python]                 | 45731.408641 us (45.731409 ms) | *N/A*                        | *N/A*
RiffpeX(100, 100, 100, 1000) [Python]    | *N/A*                          | 1036.274205 us (1.036274 ms) | *N/A*
RiffpeX(50, 50, 40, 100, 100) [Python]   | *N/A*                          | 287.463731 us                | *N/A*
RiffpeX(50, 50, 50, 80, 100) [Python]    | *N/A*                          | 279.245971 us                | *N/A*
RiffpeX(25, 25, 25, 25, 40, 64) [Python] | *N/A*                          | 213.594211 us                | *N/A*
FF1 [Go]                                 | 24.478399 us                   | 25.090845 us                 | 24.080567 us
FF3 [Go]                                 | 29.181906 us                   | 28.399115 us                 | 28.541695 us
Riffpe(n=10) [native]                    | 9.283083 us                    | 5.843932 us                  | 4.412632 us
Riffpe(n=100) [native]                   | 67.908192 us                   | *N/A*                        | 24.992604 us
Riffpe(n=1000) [native]                  | *N/A*                          | 409.697968 us                | 273.128215 us
Riffpe(n=10000) [native]                 | 7546.507771 us (7.546508 ms)   | *N/A*                        | *N/A*
RiffpeX(100, 100, 100, 1000) [native]    | *N/A*                          | 165.743191 us                | *N/A*
RiffpeX(50, 50, 40, 100, 100) [native]   | *N/A*                          | 27.423131 us                 | *N/A*
RiffpeX(50, 50, 50, 80, 100) [native]    | *N/A*                          | 26.237416 us                 | *N/A*
RiffpeX(25, 25, 25, 25, 40, 64) [native] | *N/A*                          | 14.948972 us                 | *N/A*
