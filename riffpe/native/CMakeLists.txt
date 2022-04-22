cmake_minimum_required(VERSION 3.18 FATAL_ERROR)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_CUDA_SEPARABLE_COMPILATION ON)
set(CMAKE_CUDA_RESOLVE_DEVICE_SYMBOLS ON)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Release")
endif()

set(LANGUAGES CXX)

project(riffpe-native ${LANGUAGES})

if(MSVC)
    if(CMAKE_CXX_COMPILER_ID STREQUAL "Clang")
        add_compile_options(
            $<$<CONFIG:RELEASE>:-O3>
            $<$<COMPILE_LANGUAGE:CXX>:-march=native>
            $<$<COMPILE_LANGUAGE:CXX>:-mtune=native>
        )
    endif()
else()
    add_compile_options(
        $<$<CONFIG:RELEASE>:-O3>
        $<$<COMPILE_LANGUAGE:CXX>:-march=native>
        $<$<COMPILE_LANGUAGE:CXX>:-mtune=native>
    )
endif()

find_program(CCACHE_PATH ccache)
if(CCACHE_PATH)
    set(CCACHE_CACHE_DIR ${CMAKE_CACHEFILE_DIR}/CMakeFiles/ccache)
    make_directory(${CCACHE_CACHE_DIR})
    set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE "\"${CMAKE_COMMAND}\" -E env \"CCACHE_DIR=${CCACHE_CACHE_DIR}\" \"${CCACHE_PATH}\"")
endif()

# CMake 3.14+
include(FetchContent)

FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG        v2.6.2
)
FetchContent_MakeAvailable(pybind11)

pybind11_add_module(riffpe_native ${CMAKE_CURRENT_SOURCE_DIR}/src/riffpe_native.cpp)

add_executable(test_riffpe_native test/test_riffpe_native.cpp)

add_library(riffpe_native_crypto STATIC src/aes_x86_aesni.cpp)
target_link_libraries(riffpe_native      PUBLIC riffpe_native_crypto)
target_link_libraries(test_riffpe_native PUBLIC riffpe_native_crypto)

# Install Python modules to the root source directory (this is where the Python interface will be looking for them)
install(TARGETS riffpe_native DESTINATION ${CMAKE_SOURCE_DIR})
