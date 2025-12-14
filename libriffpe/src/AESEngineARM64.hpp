#pragma once

#include "../include/riffpe/AESEngine.hpp"

#include <array>

#include <cstdint>

#include "compiler_id.h"
#include "arm_utils.hpp"

namespace riffpe
{
    namespace crypto
    {
        class AESEngineARM64 : public AESEngine
        {
        public:
            using AESEngine::max_round_count;
            using AESEngine::block_size;
            
        protected:
            std::array<uint8x16_t, max_round_count+1> _key;

        public:
            virtual ~AESEngineARM64() {}
            void set_key(const uint8_t* key, size_t size);

            void encrypt_ecb(const uint8_t* in, uint8_t* out, size_t block_count);
            void encrypt_cbc(const uint8_t* in, uint8_t* out, size_t block_count, uint8_t* state);

            const char* engine_id() const { return "AES Engine arm-neon-aese " RIFFPE_COMPILER_ID; }
        };
    }
}
