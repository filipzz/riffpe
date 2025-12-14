#pragma once

#include <cstdint>


#ifdef __x86_64__
#include <immintrin.h>

static inline uint64_t ts() {
    return __rdtsc();
}


#else
#  error unsupported platform
#endif


