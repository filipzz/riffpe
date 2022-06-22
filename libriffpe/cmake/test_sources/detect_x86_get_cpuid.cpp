#include <cpuid.h>
#include <cstdio>

// MSVC uses __cpuid, GCC uses __get_cpuid; this source detects if __get_cpuid is available

int main(int argc, const char *argv[])
{
  unsigned cpuid[4];
  __get_cpuid(0, &cpuid[0], &cpuid[1], &cpuid[2], &cpuid[3]);
  std::printf("%08x\n", cpuid[2]);
  return 0;
}
