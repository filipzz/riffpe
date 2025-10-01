#pragma once

#include <riffpe/AESEngine.hpp>

#include <cstdint>

namespace riffpe
{
    namespace detail
    {
        inline uint32_t _validate_params(uint32_t radix, uint32_t digits)
        {
            uint32_t el_size;

            if(digits < 1)
                throw std::length_error("Cipher must have at least one digit.");

            if(radix < 256)
                el_size = sizeof(uint8_t);
            else if(radix < 65536)
                el_size = sizeof(uint16_t);
            else if(radix < 4294967296)
                el_size = sizeof(uint32_t);
            else
                throw std::length_error("Radix too big (must be < 32 bits)");
            
            return el_size;
        }

        // This effectively reduces code duplication between Riffpe & RiffpeX
        template<typename ElType, bool Inverse, typename RiffpeClass>
        inline void enc_dec_impl(std::vector<uint32_t>& message, RiffpeClass* pthis)
        {
            auto l = pthis->count();
            using aes_engine_type = crypto::AESEngine;

            size_t tweak_len = sizeof(ElType) * (l + 1);
            size_t tweak_padded_blocks = (tweak_len + aes_engine_type::block_size - 1)
                                    / aes_engine_type::block_size;
            size_t tweak_padded_size   = tweak_padded_blocks
                                    * aes_engine_type::block_size;
            size_t el_count_padded = tweak_padded_size / sizeof(ElType);

            std::vector<ElType> message_buf(el_count_padded, 0);
            for(int i=0; i<l; ++i)
                message_buf[i] = message[i];
            
            if constexpr (!Inverse)
            {
                // Absorbing phase
                pthis->template round<ElType, Inverse>(0, message_buf.data());
                // Squeezing phase
                pthis->template round<ElType, Inverse>(1, message_buf.data());
            }
            else
            {
                // Inverse absorbing phase
                pthis->template round<ElType, Inverse>(1, message_buf.data());
                // Inverse squeezing phase
                pthis->template round<ElType, Inverse>(0, message_buf.data());
            }

            for(int i=0; i<l; ++i)
                message[i] = message_buf[i];
        }
    }
}
