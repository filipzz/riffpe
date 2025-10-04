#pragma once

#include <cstddef>
#include <cstdint>

namespace riffpe
{
    namespace util
    {
        constexpr inline uint32_t load_u32_le(const uint8_t* ptr)
        {
            return (uint32_t)(ptr[0])
                |  (uint32_t)(ptr[1]) << 8
                |  (uint32_t)(ptr[2]) << 16
                |  (uint32_t)(ptr[3]) << 24;
        }

        template<int Byte, typename UInt>
        constexpr inline uint8_t extract_byte(UInt value)
        {
            return (value >> (Byte * 8)) & 0xFF;
        }

        constexpr inline void store_u32_le(uint8_t* ptr, uint32_t value)
        {
            ptr[0] = extract_byte<0>(value);
            ptr[1] = extract_byte<1>(value);
            ptr[2] = extract_byte<2>(value);
            ptr[3] = extract_byte<3>(value);
        }

        constexpr inline void store_u64_le(uint8_t* ptr, uint64_t value)
        {
            ptr[0] = extract_byte<0>(value);
            ptr[1] = extract_byte<1>(value);
            ptr[2] = extract_byte<2>(value);
            ptr[3] = extract_byte<3>(value);
            ptr[4] = extract_byte<4>(value);
            ptr[5] = extract_byte<5>(value);
            ptr[6] = extract_byte<6>(value);
            ptr[7] = extract_byte<7>(value);
        }

        template<typename ByteContainer>
        constexpr inline void push_u32_le(ByteContainer& container, uint32_t value) {
            container.push_back(extract_byte<0>(value));
            container.push_back(extract_byte<1>(value));
            container.push_back(extract_byte<2>(value));
            container.push_back(extract_byte<3>(value));
        }

        template<typename ByteContainer>
        constexpr inline void push_u64_le(ByteContainer& container, uint64_t value) {
            container.push_back(extract_byte<0>(value));
            container.push_back(extract_byte<1>(value));
            container.push_back(extract_byte<2>(value));
            container.push_back(extract_byte<3>(value));
            container.push_back(extract_byte<4>(value));
            container.push_back(extract_byte<5>(value));
            container.push_back(extract_byte<6>(value));
            container.push_back(extract_byte<7>(value));
        }

        template<typename ByteContainer>
        constexpr inline void push_pkcs7_padding(ByteContainer& container, size_t block_size = 16u) {
            uint8_t padding_byte = int(block_size) + (-int(container.size()) % int(block_size));
            container.insert(container.end(), padding_byte, padding_byte);
        }
    }
}
