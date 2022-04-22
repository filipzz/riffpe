#pragma once

#include <array>
#include <cstdint>

namespace riffpe
{
    namespace crypto
    {
        class AESEngine
        {
        public:
            static constexpr size_t max_round_count = 14;
            static constexpr size_t block_size = 16;
            
        protected:
            std::array<std::array<uint32_t, block_size / sizeof(uint32_t)>, max_round_count+1> _key;
            size_t _round_count = 0;
        
        public:
            void set_key(const uint8_t* key, size_t size);

            void encrypt_ecb(const uint8_t* in, uint8_t* out, size_t block_count);
            void encrypt_cbc(const uint8_t* in, uint8_t* out, size_t block_count, uint8_t* state); // use state[in] as IV
        };
    }
}