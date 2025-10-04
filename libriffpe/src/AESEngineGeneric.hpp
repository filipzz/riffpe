#pragma once

#include "../include/riffpe/AESEngine.hpp"

#include <array>

#include <cstdint>

#include "compiler_id.h"

namespace riffpe
{
    namespace crypto
    {
        class AESEngineGeneric : public AESEngine
        {
        public:
            using AESEngine::max_round_count;
            using AESEngine::block_size;
            
        protected:
            std::array<std::array<uint32_t, block_size / sizeof(uint32_t)>, max_round_count+1> _key;

        public:
            virtual ~AESEngineGeneric() {}
            void set_key(const uint8_t* key, size_t size);

            void encrypt_ecb(const uint8_t* in, uint8_t* out, size_t block_count);
            void encrypt_cbc(const uint8_t* in, uint8_t* out, size_t block_count, uint8_t* state);

            const char* engine_id() const { return "AES Engine Generic " RIFFPE_COMPILER_ID; }
        };
    }
}
