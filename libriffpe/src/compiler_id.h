#pragma once


#define _STR(x)   _XSTR(x)
#define _XSTR(x)  #x

#define RIFFPE_COMPILER_ID "(" _STR(CMAKE_CXX_COMPILER_ID) " v. " _STR(CMAKE_CXX_COMPILER_VERSION) ")"