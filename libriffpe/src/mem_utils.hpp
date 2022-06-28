#pragma once

#include <cstdint>

namespace riffpe
{
    namespace util
    {
        static constexpr inline uint32_t load_u32_le(const uint8_t* ptr)
        {
            return (uint32_t)(ptr[0])
                |  (uint32_t)(ptr[1]) << 8
                |  (uint32_t)(ptr[2]) << 16
                |  (uint32_t)(ptr[3]) << 24;
        }

        template<int Byte>
        static constexpr inline uint8_t extract_byte(uint32_t value)
        {
            return (value >> (Byte * 8)) & 0xFF;
        }

        static constexpr inline void store_u32_le(uint8_t* ptr, uint32_t value)
        {
            ptr[0] = extract_byte<0>(value);
            ptr[1] = extract_byte<1>(value);
            ptr[2] = extract_byte<2>(value);
            ptr[3] = extract_byte<3>(value);
        }
    }
}