#pragma once

#include <array>
#include <memory>
#include <stdexcept>
#include <vector>

#include <cstdint>

#include "AESEngine.hpp"
#include "detail.hpp"

namespace riffpe
{
    class Riffpe
    {
    protected:
        const uint32_t _radix;
        const uint32_t _digits;
        const uint32_t _bytes_per_value;
        
        uint32_t _el_size;
        std::unique_ptr<RifflePermBase> _perm_fwd;
        std::unique_ptr<RifflePermBase> _perm_rev;

        using aes_engine_type = crypto::AESEngine;
        using aes_engine_ptr  = std::unique_ptr<aes_engine_type>;
        using aes_state_type  = std::array<uint8_t, aes_engine_type::block_size>;

        aes_engine_ptr _aes_engine;
        aes_state_type _aes_state_template;

        template<typename ElType, bool Inverse>
        void enc_dec_impl(std::vector<uint32_t>& message);

    public:
        Riffpe(uint32_t c, uint32_t l, const uint8_t* key, size_t key_length, const uint8_t* tweak, size_t tweak_length, uint32_t bytes_per_value = 1);
        Riffpe(Riffpe&&);
        ~Riffpe();

        template<typename ElType, bool Inverse>
        void round(uint32_t f, detail::message_span_type<ElType> message);

        uint32_t count() const { return _digits; }

        std::vector<uint32_t> encrypt(std::vector<uint32_t> message)
        {
            if(message.size() != _digits)
                throw std::length_error("Invalid message length");
            switch(_el_size)
            {
                case sizeof(uint8_t):  detail::enc_dec_impl<uint8_t,  false, Riffpe>(message, this); break;
                case sizeof(uint16_t): detail::enc_dec_impl<uint16_t, false, Riffpe>(message, this); break;
                case sizeof(uint32_t): detail::enc_dec_impl<uint32_t, false, Riffpe>(message, this); break;
                default: throw std::runtime_error{"Invalid state (invalid element size)"};
            }            
            return message;
        }

        std::vector<uint32_t> decrypt(std::vector<uint32_t> message)
        {
            if(message.size() != _digits)
                throw std::length_error("Invalid message length");
            switch(_el_size)
            {
                case sizeof(uint8_t):  detail::enc_dec_impl<uint8_t,  true, Riffpe>(message, this); break;
                case sizeof(uint16_t): detail::enc_dec_impl<uint16_t, true, Riffpe>(message, this); break;
                case sizeof(uint32_t): detail::enc_dec_impl<uint32_t, true, Riffpe>(message, this); break;
                default: throw std::runtime_error{"Invalid state (invalid element size)"};
            }            
            return message;
        }

        const char* aes_engine_id() const { return _aes_engine->engine_id(); } // Returns engine_id of the underlying AES engine (see AESEngine class)
    };
}
