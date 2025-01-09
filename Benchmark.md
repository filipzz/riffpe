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

** Notes on tests and targets **
 * We always measure the full time of the Python interface call,
   which means it includes binding overheads for "native" targets.
 * Some Riffpe comfigurations are marked as *N/A*, when it's impossible
   to construct a Riffpe instance with given parameters, e.g. it's
   impossible to describe $Z_{10^{16}}$ as a product of $Z_{1000}$.


## Test platform 1
```
CPU: Intel(R) Core(TM) i7-6700K CPU @ 4.00GHz
RAM: 64GB DDR4-2132 (1066 MHz)
```

Times averaged for a series of 100'000 random samples.


**Encryption time**

Implementation           | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
-------------------------|------------------------------|------------------------------|-------------------------------
pyffx                    | 51.914421 us                 | 56.121582 us                 | 73.006489 us
FF3 [Python]             | 54.579224 us                 | 63.967130 us                 | 96.836365 us
Riffpe(n=10) [Python]    | 127.865262 us                | 188.436328 us                | 390.087841 us
Riffpe(n=100) [Python]   | 225.471571 us                | *N/A*                        | 664.141735 us
Riffpe(n=1000) [Python]  | 1502.005000 us (1.502005 ms) | 2269.606008 us (2.269606 ms) | *N/A*
Riffpe(n=10000) [Python] | *N/A*                        | *N/A*                        | 42792.583647 us (42.792584 ms)
RiffpeX(n>=16) [Python]  | *(same as n>=25)*            | *(same as n>=25)*            | 321.956598 us
RiffpeX(n>=25) [Python]  | 137.044271 us                | 199.421127 us                | 338.039730 us
RiffpeX(n>=50) [Python]  | 225.091456 us                | 267.333926 us                | 453.031938 us
FF1 [Go]                 | 23.282516 us                 | 23.204177 us                 | 23.299040 us
FF3 [Go]                 | 25.733069 us                 | 26.076130 us                 | 26.684856 us
Riffpe(n=10) [native]    | 4.763138 us                  | 6.251231 us                  | 9.710452 us
Riffpe(n=100) [native]   | 27.972556 us                 | *N/A*                        | 71.189431 us
Riffpe(n=1000) [native]  | 271.570495 us                | 405.294185 us                | *N/A*
Riffpe(n=10000) [native] | *N/A*                        | *N/A*                        | 7420.863365 us (7.420863 ms)
RiffpeX(n>=16) [native]  | *(same as n>=25)*            | *(same as n>=25)*            | 19.137082 us
RiffpeX(n>=25) [native]  | 11.267393 us                 | 16.103899 us                 | 24.504501 us
RiffpeX(n>=50) [native]  | 28.578337 us                 | 29.570684 us                 | 48.447074 us


**Decryption time**

Implementation           | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
-------------------------|------------------------------|------------------------------|-------------------------------
pyffx                    | 52.055904 us                 | 56.111480 us                 | 73.487428 us
FF3 [Python]             | 54.700687 us                 | 63.954190 us                 | 97.145989 us
Riffpe(n=10) [Python]    | 132.180393 us                | 195.109248 us                | 405.967888 us
Riffpe(n=100) [Python]   | 235.247120 us                | *N/A*                        | 701.644082 us
Riffpe(n=1000) [Python]  | 1586.106363 us (1.586106 ms) | 2402.143434 us (2.402143 ms) | *N/A*
Riffpe(n=10000) [Python] | *N/A*                        | *N/A*                        | 44878.310603 us (44.878311 ms)
RiffpeX(n>=16) [Python]  | *(same as n>=25)*            | *(same as n>=25)*            | 335.044034 us
RiffpeX(n>=25) [Python]  | 142.399189 us                | 208.563338 us                | 353.481355 us
RiffpeX(n>=50) [Python]  | 234.777840 us                | 281.337611 us                | 477.145213 us
FF1 [Go]                 | 23.050744 us                 | 23.068145 us                 | 23.129191 us
FF3 [Go]                 | 25.705141 us                 | 26.107421 us                 | 26.680538 us
Riffpe(n=10) [native]    | 4.423520 us                  | 5.822869 us                  | 9.154686 us
Riffpe(n=100) [native]   | 24.619363 us                 | *N/A*                        | 67.043440 us
Riffpe(n=1000) [native]  | 271.400563 us                | 406.169651 us                | *N/A*
Riffpe(n=10000) [native] | *N/A*                        | *N/A*                        | 7465.919277 us (7.465919 ms)
RiffpeX(n>=16) [native]  | *(same as n>=25)*            | *(same as n>=25)*            | 16.872021 us
RiffpeX(n>=25) [native]  | 9.433573 us                  | 13.725166 us                 | 21.744010 us
RiffpeX(n>=50) [native]  | 25.138765 us                 | 26.219696 us                 | 44.787958 us


## Test platform 2
```
CPU: AMD EPYC 7443P
RAM: 8x32GB RDIMM 3200Mhz
```

Times averaged for a series of 100'000 random samples.

**Encryption time**

Implementation           | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
-------------------------|------------------------------|------------------------------|-------------------------------
pyffx                    | 61.628685 us                 | 67.412416 us                 | 76.585629 us
FF3 [Python]             | 63.780029 us                 | 76.410560 us                 | 107.523396 us
Riffpe(n=10) [Python]    | 162.362833 us                | 243.874946 us                | 428.627924 us
Riffpe(n=100) [Python]   | 277.746892 us                | *N/A*                        | 731.346019 us
Riffpe(n=1000) [Python]  | 1809.771448 us (1.809771 ms) | 2727.124703 us (2.727125 ms) | *N/A*
Riffpe(n=10000) [Python] | *N/A*                        | *N/A*                        | 47411.452306 us (47.411452 ms)
RiffpeX(n>=16) [Python]  | *(same as n>=25)*            | *(same as n>=25)*            | 423.106058 us
RiffpeX(n>=25) [Python]  | 171.904044 us                | 255.220306 us                | 440.678673 us
RiffpeX(n>=50) [Python]  | 282.371957 us                | 335.734812 us                | 580.937853 us
FF1 [Go]                 | 4.455967 us                  | 4.488138 us                  | 4.584481 us
FF3 [Go]                 | 6.476551 us                  | 6.724977 us                  | 7.290570 us
Riffpe(n=10) [native]    | 3.935099 us                  | 5.633881 us                  | 9.579354 us
Riffpe(n=100) [native]   | 28.766100 us                 | *N/A*                        | 75.430362 us
Riffpe(n=1000) [native]  | 277.894767 us                | 415.899055 us                | *N/A*
Riffpe(n=10000) [native] | *N/A*                        | *N/A*                        | 7454.046430 us (7.454046 ms)
RiffpeX(n>=16) [native]  | *(same as n>=25)*            | *(same as n>=25)*            | 19.193291 us
RiffpeX(n>=25) [native]  | 10.693665 us                 | 15.772357 us                 | 24.893275 us
RiffpeX(n>=50) [native]  | 28.911360 us                 | 29.843480 us                 | 49.643867 us


**Decryption time**

Implementation           | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
-------------------------|------------------------------|------------------------------|-------------------------------
pyffx                    | 61.773913 us                 | 67.651665 us                 | 76.926448 us
FF3 [Python]             | 63.882326 us                 | 76.460891 us                 | 107.445545 us
Riffpe(n=10) [Python]    | 168.224551 us                | 252.712601 us                | 445.224184 us
Riffpe(n=100) [Python]   | 293.218036 us                | *N/A*                        | 781.402783 us
Riffpe(n=1000) [Python]  | 1953.736556 us (1.953737 ms) | 2955.537983 us (2.955538 ms) | *N/A*
Riffpe(n=10000) [Python] | *N/A*                        | *N/A*                        | 50609.614716 us (50.609615 ms)
RiffpeX(n>=16) [Python]  | *(same as n>=25)*            | *(same as n>=25)*            | 442.164315 us
RiffpeX(n>=25) [Python]  | 179.773033 us                | 267.005852 us                | 462.167980 us
RiffpeX(n>=50) [Python]  | 297.835350 us                | 355.148217 us                | 616.636944 us
FF1 [Go]                 | 4.607206 us                  | 4.605465 us                  | 4.653842 us
FF3 [Go]                 | 6.617545 us                  | 6.876247 us                  | 7.435471 us
Riffpe(n=10) [native]    | 3.501333 us                  | 5.020076 us                  | 8.647531 us
Riffpe(n=100) [native]   | 18.585572 us                 | *N/A*                        | 56.490244 us
Riffpe(n=1000) [native]  | 253.467517 us                | 388.474900 us                | *N/A*
Riffpe(n=10000) [native] | *N/A*                        | *N/A*                        | 7478.777543 us (7.478778 ms)
RiffpeX(n>=16) [native]  | *(same as n>=25)*            | *(same as n>=25)*            | 14.044340 us
RiffpeX(n>=25) [native]  | 7.107522 us                  | 10.666674 us                 | 17.523602 us
RiffpeX(n>=50) [native]  | 18.701114 us                 | 19.872807 us                 | 35.125438 us


## Test platform 3
```
CPU: 13th Gen Intel(R) Core(TM) i9-13900H
RAM: 32 GB LPDDR5 at 6000 MT/s	 
```

Times averaged for a series of 100'000 random samples.


**Encryption time**
Implementation          | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
------------------------|------------------------------|------------------------------|---------------------------
pyffx                   | 30.322117 us                 | 33.314879 us                 | 37.443454 us              
FF3 [Python]            | 27.472130 us                 | 32.222651 us                 | 43.259482 us              
Riffpe(n=10) [Python]   | 77.400890 us                 | 115.719747 us                | 205.258588 us             
Riffpe(n=100) [Python]  | 151.647837 us                | *N/A*                        | 402.286517 us             
Riffpe(n=1000) [Python] | 1127.369200 us (1.127369 ms) | 1694.292011 us (1.694292 ms) | *N/A*                     
RiffpeX(n>=16) [Python] | *(same as n>=25)*            | *(same as n>=25)*            | 207.590546 us             
RiffpeX(n>=25) [Python] | 86.992629 us                 | 131.246739 us                | 220.759898 us             
RiffpeX(n>=50) [Python] | 152.052292 us                | 180.681650 us                | 307.305501 us             
FF1 [Go]                | 124.658702 us                | 125.131409 us                | 122.620645 us             
FF3 [Go]                | 125.638573 us                | 127.159212 us                | 125.314994 us             
Riffpe(n=10) [native]   | 3.237855 us                  | 4.651957 us                  | 7.929434 us               
Riffpe(n=100) [native]  | 27.776879 us                 | *N/A*                        | 71.518406 us              
Riffpe(n=1000) [native] | 281.901827 us                | 421.978376 us                | *N/A*                   
RiffpeX(n>=16) [native] | *(same as n>=25)*            | *(same as n>=25)*            | 17.816019 us              
RiffpeX(n>=25) [native] | 10.101478 us                 | 14.893605 us                 | 23.182854 us              
RiffpeX(n>=50) [native] | 27.821081 us                 | 28.458595 us                 | 47.026929 us              


**Decryption time**

Implementation          | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
------------------------|------------------------------|------------------------------|---------------------------
pyffx                   | 30.432406 us                 | 33.566098 us                 | 37.964543 us              
FF3 [Python]            | 27.512236 us                 | 31.966303 us                 | 42.708198 us              
Riffpe(n=10) [Python]   | 79.975181 us                 | 119.841035 us                | 212.890599 us             
Riffpe(n=100) [Python]  | 153.913254 us                | *N/A*                        | 412.936613 us             
Riffpe(n=1000) [Python] | 1173.244937 us (1.173245 ms) | 1764.721269 us (1.764721 ms) | *N/A*                     
RiffpeX(n>=16) [Python] | *(same as n>=25)*            | *(same as n>=25)*            | 214.144613 us             
RiffpeX(n>=25) [Python] | 88.383418 us                 | 133.596291 us                | 227.753573 us             
RiffpeX(n>=50) [Python] | 154.225560 us                | 184.108121 us                | 315.727713 us             
FF1 [Go]                | 124.140600 us                | 124.710053 us                | 122.655457 us             
FF3 [Go]                | 126.313094 us                | 127.374749 us                | 125.388571 us             
Riffpe(n=10) [native]   | 3.055111 us                  | 4.437086 us                  | 7.607327 us               
Riffpe(n=100) [native]  | 19.804243 us                 | *N/A*                        | 60.257029 us              
Riffpe(n=1000) [native] | 275.530924 us                | 416.475785 us                | *N/A*    
RiffpeX(n>=16) [native] | *(same as n>=25)*            | *(same as n>=25)*            | 13.301078 us              
RiffpeX(n>=25) [native] | 6.535937 us                  | 10.099881 us                 | 17.422434 us              
RiffpeX(n>=50) [native] | 19.873371 us                 | 20.858023 us                 | 37.586854 us              


## Test platform 4
```
Apple MacBook Pro M2 (No hardware acceleration for AES (yet))
CPU: Apple Silicon M2
RAM: 16GB
```

Times averaged for a series of 100'000 random samples.



**Encryption time**
Implementation          | [9-digit base10 integers]    | [6-digit base10 integers]    | [16-digit base10 integers]
------------------------|------------------------------|------------------------------|---------------------------
pyffx                   | 28.666813 us                 | 26.617759 us                 | 32.321983 us              
FF3 [Python]            | 23.373233 us                 | 19.991472 us                 | 30.379130 us              
Riffpe(n=10) [Python]   | 99.297348 us                 | 66.333966 us                 | 172.860899 us             
Riffpe(n=100) [Python]  | *N/A*                        | 148.367700 us                | 386.731620 us             
Riffpe(n=1000) [Python] | 1690.558570 us (1.690559 ms) | 1128.110936 us (1.128111 ms) | *N/A*                     
RiffpeX(n>=16) [Python] | *(same as n>=25)*            | *(same as n>=25)*            | 180.425843 us             
RiffpeX(n>=25) [Python] | 120.202711 us                | 80.953237 us                 | 199.179633 us             
RiffpeX(n>=50) [Python] | 173.838994 us                | 150.877737 us                | 292.212286 us             
FF1 [Go]                | 2.421455 us                  | 2.382380 us                  | 2.488242 us               
FF3 [Go]                | 4.064299 us                  | 3.911251 us                  | 4.406615 us               
Riffpe(n=10) [native]   | 10.812630 us                 | 7.301113 us                  | 18.484012 us              
Riffpe(n=100) [native]  | *N/A*                        | 40.409625 us                 | 105.503877 us             
Riffpe(n=1000) [native] | 510.369217 us                | 345.124989 us                | *N/A*         
RiffpeX(n>=16) [native] | *(same as n>=25)*            | *(same as n>=25)*            | 31.034969 us              
RiffpeX(n>=25) [native] | 24.316769 us                 | 16.374201 us                 | 38.864875 us              
RiffpeX(n>=50) [native] | 43.079022 us                 | 40.796614 us                 | 71.559904 us              

**Decryption time**
Implementation          | [9-digit base10 integers]    | [6-digit base10 integers]    | [16-digit base10 integers]
------------------------|------------------------------|------------------------------|---------------------------
pyffx                   | 28.793989 us                 | 26.674161 us                 | 32.382288 us              
FF3 [Python]            | 23.278291 us                 | 20.091795 us                 | 30.309779 us              
Riffpe(n=10) [Python]   | 103.064300 us                | 68.838388 us                 | 179.522438 us             
Riffpe(n=100) [Python]  | *N/A*                        | 153.956922 us                | 401.616789 us             
Riffpe(n=1000) [Python] | 1758.534715 us (1.758535 ms) | 1169.572134 us (1.169572 ms) | *N/A*                     
RiffpeX(n>=16) [Python] | *(same as n>=25)*            | *(same as n>=25)*            | 187.644484 us             
RiffpeX(n>=25) [Python] | 124.941611 us                | 84.115673 us                 | 207.466635 us             
RiffpeX(n>=50) [Python] | 180.784502 us                | 156.332716 us                | 304.448996 us             
FF1 [Go]                | 2.486648 us                  | 2.468947 us                  | 2.543837 us               
FF3 [Go]                | 4.192245 us                  | 4.005510 us                  | 4.500464 us               
Riffpe(n=10) [native]   | 10.291026 us                 | 6.951989 us                  | 17.636422 us              
Riffpe(n=100) [native]  | *N/A*                        | 34.235035 us                 | 94.425913 us              
Riffpe(n=1000) [native] | 498.140683 us                | 334.273266 us                | *N/A* 
RiffpeX(n>=16) [native] | *(same as n>=25)*            | *(same as n>=25)*            | 28.556010 us              
RiffpeX(n>=25) [native] | 21.421437 us                 | 14.358682 us                 | 34.687414 us              
RiffpeX(n>=50) [native] | 37.094159 us                 | 34.628894 us                 | 63.182252 us              
