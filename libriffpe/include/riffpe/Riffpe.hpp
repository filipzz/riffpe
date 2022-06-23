#pragma once

#include <array>
#include <stdexcept>
#include <vector>

#include <cstdint>

#include "AESEngine.hpp"

namespace riffpe
{
    class Riffpe
    {
    protected:
        const uint32_t _c;
        const uint32_t _l;
        const uint32_t _chop;
        
        uint32_t _el_size;
        uint32_t _perm_msg_len;
        uint32_t _perm_msg_len_blocks;
        uint32_t _perm_bytes_per_value;
        std::vector<uint8_t> _perm_state;
        

        using aes_engine_type = crypto::AESEngine;
        using aes_engine_ptr  = std::unique_ptr<aes_engine_type>;
        using aes_state_type  = std::array<uint8_t, aes_engine_type::block_size>;

        aes_engine_ptr _aes_engine;
        aes_state_type _aes_state_template;

        template<typename ElType, bool Inverse>
        void enc_dec_impl(std::vector<uint32_t>& message);

    public:
        Riffpe(uint32_t c, uint32_t l, const uint8_t* key, size_t key_length, const uint8_t* tweak, size_t tweak_length, uint32_t chop = 1);

        template<typename ElType, bool Inverse>
        ElType perm(ElType x, aes_state_type& aes_state);

        template<typename ElType, bool Inverse>
        void round(uint32_t f, ElType* message);

        std::vector<uint32_t> enc(std::vector<uint32_t> message)
        {
            if(message.size() != _l)
                throw std::length_error("Invalid message length");
            switch(_el_size)
            {
                case sizeof(uint8_t):  enc_dec_impl<uint8_t,  false>(message); break;
                case sizeof(uint16_t): enc_dec_impl<uint16_t, false>(message); break;
                case sizeof(uint32_t): enc_dec_impl<uint32_t, false>(message); break;
                default: throw std::runtime_error{"Invalid state (invalid element size)"};
            }            
            return message;
        }

        std::vector<uint32_t> dec(std::vector<uint32_t> message)
        {
            if(message.size() != _l)
                throw std::length_error("Invalid message length");
            switch(_el_size)
            {
                case sizeof(uint8_t):  enc_dec_impl<uint8_t,  true>(message); break;
                case sizeof(uint16_t): enc_dec_impl<uint16_t, true>(message); break;
                case sizeof(uint32_t): enc_dec_impl<uint32_t, true>(message); break;
                default: throw std::runtime_error{"Invalid state (invalid element size)"};
            }            
            return message;
        }

        const char* aes_engine_id() const { return _aes_engine->engine_id(); } // Returns engine_id of the underlying AES engine (see AESEngine class)
    };
}
