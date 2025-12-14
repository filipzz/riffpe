cmake_minimum_required(VERSION 3.18 FATAL_ERROR)

# Public configure options
option(RIFFPE_DISABLE_ACCELERATION "Force generic AES implementation instead of hardware accelerated" OFF)


set(CMAKE_CXX_STANDARD 17)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_INTERPROCEDURAL_OPTIMIZATION ON)


project(libriffpe CXX)

set (CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})

include(CheckCompilerSupport)


add_library(riffpe
            STATIC
            src/AESEngine.cpp
            src/AESEngineGeneric.cpp
            $<$<BOOL:${RIFFPE_CXX_EXT_AESNI_AVAILABLE}>:src/AESEngineAESNI.cpp>
            $<$<BOOL:${RIFFPE_CXX_EXT_AESNEON_AVAILABLE}>:src/AESEngineARM64.cpp>
            src/Riffpe.cpp
            src/RiffpeX.cpp
            )

target_include_directories(riffpe PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_compile_definitions(riffpe PRIVATE "CMAKE_CXX_COMPILER_ID=${CMAKE_CXX_COMPILER_ID}")
target_compile_definitions(riffpe PRIVATE "CMAKE_CXX_COMPILER_VERSION=${CMAKE_CXX_COMPILER_VERSION}")

if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_options(riffpe PRIVATE ${RIFFPE_OPT_FLAGS})
endif()
if(RIFFPE_CXX_FLAG_MAES_AVAILABLE AND RIFFPE_CXX_EXT_AESNI_AVAILABLE)
    target_compile_options(riffpe PRIVATE "-maes")
endif()

if(RIFFPE_CXX_EXT_MM_LOADU_SI64_AVAILABLE)
    target_compile_definitions(riffpe PRIVATE RIFFPE_HAVE_MM_LOADU_SI64=1)
endif()
if(RIFFPE_CXX_EXT_CPUID_AVAILABLE)
    target_compile_definitions(riffpe PRIVATE RIFFPE_HAVE_CPUID=1)
endif()
if(RIFFPE_CXX_EXT_GET_CPUID_AVAILABLE)
    target_compile_definitions(riffpe PRIVATE RIFFPE_HAVE_GET_CPUID=1)
endif()
if(RIFFPE_CXX_EXT_AESNI_AVAILABLE AND NOT RIFFPE_DISABLE_ACCELERATION)
    target_compile_definitions(riffpe PRIVATE RIFFPE_HAVE_AESNI=1)
endif()
if(RIFFPE_CXX_EXT_AESNEON_AVAILABLE AND NOT RIFFPE_DISABLE_ACCELERATION)
    target_compile_definitions(riffpe PRIVATE RIFFPE_HAVE_AESNEON=1)
endif()

add_executable(test_aes_engine tests/test_aes_engine.cpp)
target_link_libraries(test_aes_engine PUBLIC riffpe)

add_executable(test_benchmark tests/test_benchmark.cpp)
target_link_libraries(test_benchmark PUBLIC riffpe)

# TODO: add more test and install targets
