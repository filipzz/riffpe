#pragma once

#include <array>
#include <stdexcept>
#include <vector>

#include <cstdint>

#include "AESEngine.hpp"

namespace riffpe
{
    class RifflePermBase;
    namespace detail
    {
        // This effectively reduces code duplication between Riffpe & RiffpeX
        template<typename ElType, bool Inverse, typename RiffpeClass>
        void enc_dec_impl(std::vector<uint32_t>& message, RiffpeClass* pthis);
    }

    class RiffpeX
    {
    protected:
        const std::vector<uint32_t> _cs;
        const uint32_t _l;
        const uint32_t _chop;
        
        uint32_t _el_size;        
        std::vector<std::unique_ptr<RifflePermBase>> _perms;

        using aes_engine_type = crypto::AESEngine;
        using aes_engine_ptr  = std::unique_ptr<aes_engine_type>;
        using aes_state_type  = std::array<uint8_t, aes_engine_type::block_size>;

        aes_engine_ptr _aes_engine;
        aes_state_type _aes_state_template;

        template<typename ElType, bool Inverse>
        void enc_dec_impl(std::vector<uint32_t>& message);

    public:
        RiffpeX(uint32_t* c_begin, uint32_t* c_end, const uint8_t* key, size_t key_length, const uint8_t* tweak, size_t tweak_length, uint32_t chop = 1);
        RiffpeX(RiffpeX&&);
        ~RiffpeX();

        template<typename ElType, bool Inverse>
        void round(uint32_t f, ElType* message);

        uint32_t count() const { return _l; }

        std::vector<uint32_t> encrypt(std::vector<uint32_t> message)
        {
            if(message.size() != _l)
                throw std::length_error("Invalid message length");
            switch(_el_size)
            {
                case sizeof(uint8_t):  detail::enc_dec_impl<uint8_t,  false, RiffpeX>(message, this); break;
                case sizeof(uint16_t): detail::enc_dec_impl<uint16_t, false, RiffpeX>(message, this); break;
                case sizeof(uint32_t): detail::enc_dec_impl<uint32_t, false, RiffpeX>(message, this); break;
                default: throw std::runtime_error{"Invalid state (invalid element size)"};
            }            
            return message;
        }

        std::vector<uint32_t> decrypt(std::vector<uint32_t> message)
        {
            if(message.size() != _l)
                throw std::length_error("Invalid message length");
            switch(_el_size)
            {
                case sizeof(uint8_t):  detail::enc_dec_impl<uint8_t,  true, RiffpeX>(message, this); break;
                case sizeof(uint16_t): detail::enc_dec_impl<uint16_t, true, RiffpeX>(message, this); break;
                case sizeof(uint32_t): detail::enc_dec_impl<uint32_t, true, RiffpeX>(message, this); break;
                default: throw std::runtime_error{"Invalid state (invalid element size)"};
            }            
            return message;
        }

        const char* aes_engine_id() const { return _aes_engine->engine_id(); } // Returns engine_id of the underlying AES engine (see AESEngine class)
    };
}
