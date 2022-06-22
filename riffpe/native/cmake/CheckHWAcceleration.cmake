include (CheckCXXCompilerFlag)
include (CheckCXXSourceCompiles)
include (CheckCXXSourceRuns)

if (NOT MSVC)
  check_cxx_compiler_flag (-march=native CXX_FLAG_MARCH_NATIVE_AVAILABLE)
  check_cxx_compiler_flag (-mtune=native CXX_FLAG_MTUNE_NATIVE_AVAILABLE)
  check_cxx_compiler_flag (-maes         CXX_FLAG_MAES_AVAILABLE)
endif()


# Detect instruction support in intrinsics
check_cxx_source_compiles("#include \"${CMAKE_CURRENT_LIST_DIR}/test_sources/detect_x86_mm_loadu_si64.cpp\" " HAS_MM_LOADU_SI64)
check_cxx_source_compiles("#include \"${CMAKE_CURRENT_LIST_DIR}/test_sources/detect_x86_cpuid.cpp\" " HAS_CPUID)

# TODO: Feature detection in cross-compiling scenario
if (CMAKE_CROSSCOMPILING)
  # TODO!
else ()

  if(MSVC OR CXX_FLAG_MAES_AVAILABLE)
    set (ORIG_CMAKE_REQUIRED_FLAGS ${CMAKE_REQUIRED_FLAGS})
    set (CMAKE_REQUIRED_FLAGS "${CMAKE_REQUIRED_FLAGS} -maes")
    CHECK_CXX_SOURCE_COMPILES("#include \"${CMAKE_CURRENT_LIST_DIR}/test_sources/detect_x86_aesni.cpp\" " HOST_AESNI_AVAILABLE)
    set (CMAKE_REQUIRED_FLAGS ${ORIG_CMAKE_REQUIRED_FLAGS})

    if (HOST_AESNI_AVAILABLE AND RIFFPE_USE_HW_ACCELERATION)
      set (RIFFPE_AESNI_AVAILABLE TRUE)
      macro (riffpe_enable_aesni_for_target Target)
        if(NOT MSVC)
          target_compile_options (${Target} PUBLIC "-maes")
        endif ()
      endmacro()
    endif ()

  endif ()

  # Default to -march=native if available
  if (CXX_FLAG_MARCH_NATIVE_AVAILABLE)
    list (APPEND RIFFPE_OPT_FLAGS "-march=native")
  endif ()

  # Default to -mtune=native if available
  if (CXX_FLAG_MTUNE_NATIVE_AVAILABLE)
    list (APPEND RIFFPE_OPT_FLAGS "-mtune=native")
  endif ()

endif ()
