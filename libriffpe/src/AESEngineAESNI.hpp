#pragma once

#include <array>
#include <cstdint>

#include <riffpe/AESEngine.hpp>
#include "compiler_id.h"
#include "x86_utils.hpp"

namespace riffpe
{
    namespace crypto
    {
        class AESEngineAESNI : public AESEngine
        {
        public:
            using AESEngine::max_round_count;
            using AESEngine::block_size;
            
        protected:
            std::array<__m128i, max_round_count+1> _key;

        public:
            virtual ~AESEngineAESNI() {}
            void set_key(const uint8_t* key, size_t size);

            void encrypt_ecb(const uint8_t* in, uint8_t* out, size_t block_count);
            void encrypt_cbc(const uint8_t* in, uint8_t* out, size_t block_count, uint8_t* state);

            const char* engine_id() const { return "AES Engine x86-aes-ni " RIFFPE_COMPILER_ID; }
        };
    }
}
