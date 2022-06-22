#include <immintrin.h>
#include <cstdio>
#include <cstdint>

int main(int argc, const char *argv[])
{
  uint64_t test_var_0 = 123;
  __m128i test_var_1 = _mm_loadu_si64(const_cast<const uint64_t*>(&test_var_0));
  int test_var_2 = _mm_extract_epi8 (test_var_1, 0);
  std::printf("%08x\n", test_var_1);
  return 0;
}
