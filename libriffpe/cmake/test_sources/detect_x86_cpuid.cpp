#include <intrin.h>
#include <cstdio>

// MSVC uses __cpuid, GCC uses __get_cpuid; this source detects if __cpuid is available

int main(int argc, const char *argv[])
{
  int cpuid[4];
  __cpuid(cpuid, 0);
  std::printf("%08x\n", cpuid[2]);
  return 0;
}
