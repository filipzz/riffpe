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
$ sudo apt install python3-venv python3-dev golang cmake
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
Implementation          | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
------------------------|------------------------------|------------------------------|---------------------------
pyffx                   | 26.848726 us                 | 28.587382 us                 | 31.862288 us              
FF3 [Python]            | 20.319668 us                 | 23.304721 us                 | 30.952352 us              
Riffpe(n=10) [Python]   | 66.859381 us                 | 99.491692 us                 | 176.838924 us             
Riffpe(n=100) [Python]  | 154.331029 us                | *N/A*                        | 400.525435 us             
Riffpe(n=1000) [Python] | 1132.698363 us (1.132698 ms) | 1700.581762 us (1.700582 ms) | *N/A*                     
RiffpeX(n>=16) [Python] | *(same as n>=25)*            | *(same as n>=25)*            | 185.277786 us             
RiffpeX(n>=25) [Python] | 80.775718 us                 | 120.579996 us                | 203.432076 us             
RiffpeX(n>=50) [Python] | 151.496939 us                | 173.996147 us                | 296.246003 us             
FF1 [Go]                | 2.350532 us                  | 2.351495 us                  | 2.475475 us               
FF3 [Go]                | 3.824839 us                  | 4.105199 us                  | 4.465162 us               
Riffpe(n=10) [native]   | 2.215088 us                  | 3.106199 us                  | 5.231824 us               
Riffpe(n=100) [native]  | 20.123835 us                 | *N/A*                        | 53.603099 us              
Riffpe(n=1000) [native] | 207.510464 us                | 311.018867 us                | *N/A*    
RiffpeX(n>=16) [native] | *(same as n>=25)*            | *(same as n>=25)*            | 12.059439 us              
RiffpeX(n>=25) [native] | 7.246032 us                  | 10.701991 us                 | 16.696930 us              
RiffpeX(n>=50) [native] | 20.178766 us                 | 20.583378 us                 | 34.328756 us              

**Decryption time**
Implementation          | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
------------------------|------------------------------|------------------------------|---------------------------
pyffx                   | 26.955693 us                 | 28.722135 us                 | 31.982681 us              
FF3 [Python]            | 20.472033 us                 | 23.286966 us                 | 30.927852 us              
Riffpe(n=10) [Python]   | 69.387709 us                 | 103.255261 us                | 183.840928 us             
Riffpe(n=100) [Python]  | 159.184281 us                | *N/A*                        | 415.955270 us             
Riffpe(n=1000) [Python] | 1174.723789 us (1.174724 ms) | 1768.678350 us (1.768678 ms) | *N/A*                     
RiffpeX(n>=16) [Python] | *(same as n>=25)*            | *(same as n>=25)*            | 192.793216 us             
RiffpeX(n>=25) [Python] | 83.978545 us                 | 125.362241 us                | 211.764913 us             
RiffpeX(n>=50) [Python] | 156.975792 us                | 180.895637 us                | 308.207046 us             
FF1 [Go]                | 2.420522 us                  | 2.414628 us                  | 2.561597 us               
FF3 [Go]                | 3.939182 us                  | 4.237299 us                  | 4.568294 us               
Riffpe(n=10) [native]   | 2.101799 us                  | 2.946795 us                  | 4.976009 us               
Riffpe(n=100) [native]  | 13.925014 us                 | *N/A*                        | 42.608957 us              
Riffpe(n=1000) [native] | 196.780415 us                | 299.359738 us                | *N/A*          
RiffpeX(n>=16) [native] | *(same as n>=25)*            | *(same as n>=25)*            | 9.655402 us               
RiffpeX(n>=25) [native] | 5.213448 us                  | 7.782824 us                  | 12.473303 us              
RiffpeX(n>=50) [native] | 13.981167 us                 | 14.594120 us                 | 25.834916 us              


## Test platform 5

```
Apple MacBook Pro M3 
CPU: Apple Silicon M3
RAM: 36GB
```


**Encryption time**
Implementation          | [6-digit base10 integers] | [9-digit base10 integers]    | [16-digit base10 integers]
------------------------|---------------------------|------------------------------|---------------------------
pyffx                   | 19.444915 us              | 21.172657 us                 | 23.122047 us              
FF3 [Python]            | 16.863991 us              | 19.621980 us                 | 25.738379 us              
Riffpe(n=10) [Python]   | 55.075674 us              | 82.509539 us                 | 145.577507 us             
Riffpe(n=100) [Python]  | 128.902214 us             | *N/A*                        | 343.145806 us             
Riffpe(n=1000) [Python] | 942.183500 us             | 1448.266519 us (1.448267 ms) | *N/A*                     
RiffpeX(n>=16) [Python] | *N/A*                     | *N/A*                        | 155.819945 us             
RiffpeX(n>=25) [Python] | 68.612205 us              | 102.555249 us                | 172.635678 us             
RiffpeX(n>=50) [Python] | 129.314760 us             | 150.042073 us                | 254.394272 us             
FF1 [Go]                | 1.850072 us               | 1.823908 us                  | 1.955441 us               
FF3 [Go]                | 3.097339 us               | 3.241303 us                  | 3.555541 us               
Riffpe(n=10) [native]   | 1.695244 us               | 2.403553 us                  | 4.037695 us               
Riffpe(n=100) [native]  | 16.677125 us              | *N/A*                        | 44.745565 us              
Riffpe(n=1000) [native] | 174.140379 us             | 268.708087 us                | *N/A*                     
RiffpeX(n>=16) [native] | *N/A*                     | *N/A*                        | 10.092650 us              
RiffpeX(n>=25) [native] | 5.861662 us               | 8.933298 us                  | 14.047371 us              
RiffpeX(n>=50) [native] | 16.509270 us              | 17.492825 us                 | 29.017033 us              


**Decryption time**

Implementation          | [6-digit base10 integers] | [9-digit base10 integers]    | [16-digit base10 integers]
------------------------|---------------------------|------------------------------|---------------------------
pyffx                   | 19.481547 us              | 21.243491 us                 | 23.203869 us              
FF3 [Python]            | 16.962539 us              | 19.580746 us                 | 25.682651 us              
Riffpe(n=10) [Python]   | 56.981769 us              | 85.491255 us                 | 151.389730 us             
Riffpe(n=100) [Python]  | 133.130482 us             | *N/A*                        | 355.040964 us             
Riffpe(n=1000) [Python] | 972.661738 us             | 1496.702079 us (1.496702 ms) | *N/A*                     
RiffpeX(n>=16) [Python] | *N/A*                     | *N/A*                        | 161.588549 us             
RiffpeX(n>=25) [Python] | 71.205992 us              | 106.337158 us                | 179.119136 us             
RiffpeX(n>=50) [Python] | 133.686178 us             | 155.678183 us                | 263.932461 us             
FF1 [Go]                | 1.920768 us               | 1.895865 us                  | 2.008697 us               
FF3 [Go]                | 3.222272 us               | 3.373040 us                  | 3.656863 us               
Riffpe(n=10) [native]   | 1.580319 us               | 2.248571 us                  | 3.806976 us               
Riffpe(n=100) [native]  | 10.145970 us              | *N/A*                        | 28.919716 us              
Riffpe(n=1000) [native] | 132.414228 us             | 214.683895 us                | *N/A*
RiffpeX(n>=16) [native] | *N/A*                     | *N/A*                        | 7.734065 us               
RiffpeX(n>=25) [native] | 4.059833 us               | 6.193440 us                  | 9.927761 us               
RiffpeX(n>=50) [native] | 10.074040 us              | 11.106956 us                 | 18.926257 us              


## Test platform 6
```
CPU: Intel(R) Xeon(R) Gold 6342 CPU @ 2.80GHz
RAM: 64 GB
```

**Encryption time**
Implementation          | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
------------------------|------------------------------|------------------------------|---------------------------
pyffx                   | 63.079604 us                 | 69.128211 us                 | 75.370258 us              
FF3 [Python]            | 59.092358 us                 | 77.010549 us                 | 102.502928 us             
Riffpe(n=10) [Python]   | 141.527825 us                | 207.169373 us                | 374.259361 us             
Riffpe(n=100) [Python]  | 252.395804 us                | *N/A*                        | 673.564254 us             
Riffpe(n=1000) [Python] | 1764.100164 us (1.764100 ms) | 2635.966341 us (2.635966 ms) | *N/A*                     
RiffpeX(n>=16) [Python] | *(same as n>=25)*            | *(same as n>=25)*            | 357.159918 us             
RiffpeX(n>=25) [Python] | 154.538517 us                | 227.523714 us                | 374.987743 us             
RiffpeX(n>=50) [Python] | 256.704811 us                | 304.742725 us                | 512.999696 us             
FF1 [Go]                | 182.987567 us                | 185.747542 us                | 185.253188 us             
FF3 [Go]                | 188.510816 us                | 194.616387 us                | 190.866425 us             
Riffpe(n=10) [native]   | 4.380597 us                  | 5.709093 us                  | 9.684850 us               
Riffpe(n=100) [native]  | 33.376996 us                 | *N/A*                        | 87.756041 us              
Riffpe(n=1000) [native] | 345.858710 us                | 514.229154 us                | *N/A*       
RiffpeX(n>=16) [native] | *(same as n>=25)*            | *(same as n>=25)*            | 21.984783 us              
RiffpeX(n>=25) [native] | 12.534854 us                 | 17.867115 us                 | 27.843765 us              
RiffpeX(n>=50) [native] | 33.700590 us                 | 35.181096 us                 | 56.779438 us              

**Decryption time**
Implementation          | [6-digit base10 integers]    | [9-digit base10 integers]    | [16-digit base10 integers]
------------------------|------------------------------|------------------------------|---------------------------
pyffx                   | 63.415213 us                 | 69.505532 us                 | 76.200847 us              
FF3 [Python]            | 59.244110 us                 | 77.032560 us                 | 102.358268 us             
Riffpe(n=10) [Python]   | 145.248935 us                | 213.203979 us                | 386.628546 us             
Riffpe(n=100) [Python]  | 258.729112 us                | *N/A*                        | 702.057554 us             
Riffpe(n=1000) [Python] | 1851.131495 us (1.851131 ms) | 2767.896111 us (2.767896 ms) | *N/A*                     
RiffpeX(n>=16) [Python] | *(same as n>=25)*            | *(same as n>=25)*            | 368.534440 us             
RiffpeX(n>=25) [Python] | 156.805987 us                | 232.979660 us                | 387.087414 us             
RiffpeX(n>=50) [Python] | 262.892827 us                | 313.566597 us                | 532.343138 us             
FF1 [Go]                | 182.563033 us                | 185.246989 us                | 184.916030 us             
FF3 [Go]                | 188.189280 us                | 194.626107 us                | 190.740503 us             
Riffpe(n=10) [native]   | 4.263128 us                  | 5.560279 us                  | 9.482151 us               
Riffpe(n=100) [native]  | 24.747900 us                 | *N/A*                        | 74.804452 us              
Riffpe(n=1000) [native] | 334.161353 us                | 503.455280 us                | *N/A* 
RiffpeX(n>=16) [native] | *(same as n>=25)*            | *(same as n>=25)*            | 17.326193 us              
RiffpeX(n>=25) [native] | 8.868536 us                  | 13.122316 us                 | 21.796283 us              
RiffpeX(n>=50) [native] | 24.976424 us                 | 26.701513 us                 | 45.999327 us              


## Test platform 7
```
CPU: Intel(R) Xeon(R) CPU E3-1245 v5 @ 3.50GHz
RAM: 32GB RDIMM 2133 MHz
```

**Encryption time**
Implementation          | [9-digit base10 integers]    | [6-digit base10 integers]    | [16-digit base10 integers]
------------------------|------------------------------|------------------------------|---------------------------
pyffx                   | 45.515348 us                 | 42.530219 us                 | 52.224843 us              
FF3 [Python]            | 46.565617 us                 | 40.782846 us                 | 63.333349 us              
Riffpe(n=10) [Python]   | 177.102394 us                | 117.560690 us                | 320.106154 us             
Riffpe(n=100) [Python]  | *N/A*                        | 243.436109 us                | 640.831035 us             
Riffpe(n=1000) [Python] | 2724.619217 us (2.724619 ms) | 1787.530842 us (1.787531 ms) | *N/A*                     
RiffpeX(n>=16) [Python] | *(same as n>=25)*            | *(same as n>=25)*            | 317.390873 us             
RiffpeX(n>=25) [Python] | 204.606406 us                | 137.335654 us                | 346.109021 us             
RiffpeX(n>=50) [Python] | 287.188151 us                | 247.084017 us                | 483.349273 us             
FF1 [Go]                | 364.814141 us                | 365.630803 us                | 363.252412 us             
FF3 [Go]                | 365.128117 us                | 364.066322 us                | 365.215932 us             
Riffpe(n=10) [native]   | 5.891309 us                  | 4.152429 us                  | 9.928108 us               
Riffpe(n=100) [native]  | *N/A*                        | 29.771851 us                 | 77.998309 us              
Riffpe(n=1000) [native] | 438.826174 us                | 294.029697 us                | *N/A*                     
RiffpeX(n>=16) [native] | *(same as n>=25)*            | *(same as n>=25)*            | 20.522432 us              
RiffpeX(n>=25) [native] | 16.859346 us                 | 11.415984 us                 | 26.373298 us              
RiffpeX(n>=50) [native] | 31.371450 us                 | 30.203969 us                 | 52.393054 us              

**Decryption time**
Implementation          | [9-digit base10 integers]    | [6-digit base10 integers]    | [16-digit base10 integers]
------------------------|------------------------------|------------------------------|---------------------------
pyffx                   | 45.713602 us                 | 42.485339 us                 | 52.639968 us              
FF3 [Python]            | 46.421090 us                 | 40.894890 us                 | 63.589119 us              
Riffpe(n=10) [Python]   | 183.219916 us                | 121.514537 us                | 330.961792 us             
Riffpe(n=100) [Python]  | *N/A*                        | 251.848214 us                | 666.015033 us             
Riffpe(n=1000) [Python] | 2864.102350 us (2.864102 ms) | 1874.644653 us (1.874645 ms) | *N/A*                     
RiffpeX(n>=16) [Python] | *(same as n>=25)*            | *(same as n>=25)*            | 329.188894 us             
RiffpeX(n>=25) [Python] | 211.687855 us                | 141.718431 us                | 358.260772 us             
RiffpeX(n>=50) [Python] | 298.083281 us                | 255.223019 us                | 502.147847 us             
FF1 [Go]                | 363.642149 us                | 364.457707 us                | 361.982266 us             
FF3 [Go]                | 365.336358 us                | 365.161632 us                | 364.504476 us             
Riffpe(n=10) [native]   | 5.398939 us                  | 3.776316 us                  | 9.225774 us               
Riffpe(n=100) [native]  | *N/A*                        | 25.931678 us                 | 73.541688 us              
Riffpe(n=1000) [native] | 439.485915 us                | 293.849690 us                | *N/A* 
RiffpeX(n>=16) [native] | *(same as n>=25)*            | *(same as n>=25)*            | 17.643518 us              
RiffpeX(n>=25) [native] | 14.024088 us                 | 9.206854 us                  | 22.881217 us              
RiffpeX(n>=50) [native] | 27.503673 us                 | 26.247257 us                 | 48.059035 us              

