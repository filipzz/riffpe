#pragma once

#include <wmmintrin.h>
#include <immintrin.h>
#include <emmintrin.h>

#if __has_include(<cpuid.h>)
#  include <cpuid.h>
#endif

namespace riffpe
{
  namespace crypto
  {
    constexpr __m128i BSWAP_EPI64
    //  = _mm_set_epi8(8, 9, 10, 11, 12, 13, 14, 15, 0, 1, 2, 3, 4, 5, 6, 7);
      = {0x0001020304050607, 0x08090a0b0c0d0e0f};
    constexpr  __m128i ONE
    //  = _mm_set_epi32(0, 1, 0, 0);
      = {0x0000000000000000, 0x0000000000000001};
    constexpr __m128i BSWAP_MASK
    //  = _mm_set_epi8(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15);
      = {0x08090a0b0c0d0e0f, 0x0001020304050607};

    /** This helper inline reinterprets and loads potentially unaligned __m128i
     *  locations */
    template<typename T>
    inline __m128i loadu_mm128i(const T* ptr)
    { return _mm_loadu_si128( reinterpret_cast<const __m128i*>(ptr) ); }

    /** This helper inline reinterprets and loads potentially unaligned __m128i
     *  locations - restricted to 64 bits only */
    template<typename T>
    inline __m128i loadu_mm64i(const T* ptr)
    {
      /* Workaround for missing _mm_loadu_si64 intrinsic in GCC */
#if !HAS_MM_LOADU_SI64
      return __m128i{ *reinterpret_cast<const int64_t*>(ptr), 0 };
#else
      return _mm_loadu_si64(ptr);
#endif
    }

    /** This helper inline reinterprets and stores __m128i to potentially unaligned
     *  locations */
    template<typename T>
    inline void storeu_mm128i(T* out, const __m128i& value)
    { _mm_storeu_si128( reinterpret_cast<__m128i*>(out), value ); }

    /** This helper inline queries CPU capabilites for AES-NI support */
    inline bool has_aesni()
    {
      int32_t cpuid[4];
      #if HAS_CPUID
      __cpuid(cpuid, 0);
      #else
      __get_cpuid(0, &cpuid[0], &cpuid[1], &cpuid[2], &cpuid[3]);
      #endif
      return (bool)(cpuid[2] /* ECX */ & (1 << 25) /* bit 25 */);
    }
  }
}
