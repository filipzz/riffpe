cmake_minimum_required(VERSION 3.18 FATAL_ERROR)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Release")
endif()

project(riffpe-native CXX)

# CMake 3.14+
include(FetchContent)

FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG        v2.6.2
)
FetchContent_MakeAvailable(pybind11)

set (CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})
include(CheckHWAcceleration)

if(CMAKE_BUILD_TYPE STREQUAL "Release")
    add_compile_options(${RIFFPE_OPT_FLAGS})
endif()
if(CXX_EXT_MM_LOADU_SI64_AVAILABLE)
    add_compile_definitions(HAVE_MM_LOADU_SI64=1)
endif()
if(CXX_EXT_CPUID_AVAILABLE)
    add_compile_definitions(HAVE_CPUID=1)
endif()
if(CXX_EXT_GET_CPUID_AVAILABLE)
    add_compile_definitions(HAVE_GET_CPUID=1)
endif()

pybind11_add_module(riffpe_native ${CMAKE_CURRENT_SOURCE_DIR}/src/riffpe_native.cpp)

add_executable(test_riffpe_native test/test_riffpe_native.cpp)

add_library(riffpe_native_crypto
            STATIC
            src/aes_generic.cpp
            $<CXX_AESNI_AVAILABLE?src/aes_x86_aesni.cpp>
            )

target_link_libraries(riffpe_native      PUBLIC riffpe_native_crypto)
target_link_libraries(test_riffpe_native PUBLIC riffpe_native_crypto)

# Install Python modules to the root source directory (this is where the Python interface will be looking for them)
install(TARGETS riffpe_native DESTINATION ${CMAKE_SOURCE_DIR})
