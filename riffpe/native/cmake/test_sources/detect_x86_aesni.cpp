#include <immintrin.h>
#include <wmmintrin.h>
#include <cstdio>

int main(int argc, const char *argv[])
{
  volatile __m128i test_var_0 = _mm_set_epi8(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15);
  volatile __m128i test_var_1 = _mm_set_epi8(16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31);
  volatile __m128i test_var_2 = _mm_aesenc_si128 (test_var_0, test_var_1);
  int test_var_3 = _mm_extract_epi8 (test_var_2, 0);
  std::printf("%08x\n", test_var_3);
  return 0;
}
