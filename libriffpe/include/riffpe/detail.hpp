#pragma once

#include <cstddef>
#include <cstdint>


namespace riffpe
{
    class RifflePermBase;
    namespace detail
    {
        // This effectively reduces code duplication between Riffpe & RiffpeX
        template<typename ElType, bool Inverse, typename RiffpeClass>
        void enc_dec_impl(std::vector<uint32_t>& message, RiffpeClass* pthis);

        template<typename ElType>
        struct message_span_type {
            size_t byte_size;
            inline constexpr size_t elem_size() { return byte_size / sizeof(ElType); }
            union {
                uint8_t* as_bytes;
                ElType* as_elems;
            } data;
        };
    }
}

