include (CheckCXXCompilerFlag)
include (CheckCXXSourceCompiles)

if (NOT MSVC)
  check_cxx_compiler_flag (-march=native RIFFPE_CXX_FLAG_MARCH_NATIVE_AVAILABLE)
  check_cxx_compiler_flag (-mtune=native RIFFPE_CXX_FLAG_MTUNE_NATIVE_AVAILABLE)
  check_cxx_compiler_flag (-maes         RIFFPE_CXX_FLAG_MAES_AVAILABLE)
endif()


# Set CMAKE_REQUIRED_FLAGS for feature detection
set (ORIG_CMAKE_REQUIRED_FLAGS ${CMAKE_REQUIRED_FLAGS})
if (RIFFPE_CXX_FLAG_MAES_AVAILABLE)
  set (CMAKE_REQUIRED_FLAGS "${CMAKE_REQUIRED_FLAGS} -maes")
endif()

# Detect instruction support in intrinsics
check_cxx_source_compiles("#include \"${CMAKE_CURRENT_LIST_DIR}/test_sources/detect_x86_aesni.cpp\" "         RIFFPE_CXX_EXT_AESNI_AVAILABLE)
check_cxx_source_compiles("#include \"${CMAKE_CURRENT_LIST_DIR}/test_sources/detect_x86_cpuid.cpp\" "         RIFFPE_CXX_EXT_CPUID_AVAILABLE)
check_cxx_source_compiles("#include \"${CMAKE_CURRENT_LIST_DIR}/test_sources/detect_x86_get_cpuid.cpp\" "     RIFFPE_CXX_EXT_GET_CPUID_AVAILABLE)
check_cxx_source_compiles("#include \"${CMAKE_CURRENT_LIST_DIR}/test_sources/detect_x86_mm_loadu_si64.cpp\" " RIFFPE_CXX_EXT_MM_LOADU_SI64_AVAILABLE)

check_cxx_source_compiles("#include \"${CMAKE_CURRENT_LIST_DIR}/test_sources/detect_arm64_aesneon.cpp\" "     RIFFPE_CXX_EXT_AESNEON_AVAILABLE)

# Unset CMAKE_REQUIRED_FLAGS
set (CMAKE_REQUIRED_FLAGS ${ORIG_CMAKE_REQUIRED_FLAGS})

# Default to -march=native if available
if (RIFFPE_CXX_FLAG_MARCH_NATIVE_AVAILABLE)
  list (APPEND RIFFPE_OPT_FLAGS "-march=native")
endif ()

# Default to -mtune=native if available
if (RIFFPE_CXX_FLAG_MTUNE_NATIVE_AVAILABLE)
  list (APPEND RIFFPE_OPT_FLAGS "-mtune=native")
endif ()
