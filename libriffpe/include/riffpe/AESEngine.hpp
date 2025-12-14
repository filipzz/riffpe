#pragma once

#include <cstdint>
#include <cstddef>

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
            size_t _round_count = 0;

        public:
            virtual ~AESEngine() {}
            virtual void set_key(const uint8_t* key, size_t size) = 0;

            virtual void encrypt_ecb(const uint8_t* in, uint8_t* out, size_t block_count) = 0;
            virtual void encrypt_cbc(const uint8_t* in, uint8_t* out, size_t block_count, uint8_t* state) = 0; // use state[in] as IV

            static AESEngine* engine_factory(); // FIXME: optionally add "options" parameter to help select which engine to use
            virtual const char* engine_id() const = 0; // Returns a string representation of current engine name
        };
    }
}
