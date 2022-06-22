cmake_minimum_required(VERSION 3.18 FATAL_ERROR)

if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE "Release")
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)


# CMake 3.14+
include(FetchContent)

FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG        v2.6.2
)
FetchContent_MakeAvailable(pybind11)


# TODO: optionally allow linking to an already built libriffpe instead of adding it as a subproject
set(RIFFPE_LIBRIFFPE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/../../libriffpe CACHE PATH "Path to libriffpe CMake sources")
add_subdirectory(${RIFFPE_LIBRIFFPE_DIR} libriffpe)


project(pyriffpe CXX)

pybind11_add_module(_native ${CMAKE_CURRENT_SOURCE_DIR}/_native.cpp)
target_link_libraries(_native PUBLIC riffpe)

# Install Python modules to the root source directory (this is where the Python interface will be looking for them)
install(TARGETS _native DESTINATION ${CMAKE_SOURCE_DIR})
