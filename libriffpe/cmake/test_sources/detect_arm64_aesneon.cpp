#include <cstdio>
#include <arm_neon.h>
#include <arm_acle.h>

int main(int argc, const char *argv[])
{
  uint8x16_t test_var_0 = vdupq_n_u8(0);
  uint8x16_t test_var_1 = vdupq_n_u8(1);
  uint8x16_t test_var_2 = vaeseq_u8 (test_var_0, test_var_1);
  uint8_t test_var_3[16];
  vst1q_u8(test_var_3, test_var_2);
  std::printf("%08x\n", test_var_3[0]);
  return 0;
}
