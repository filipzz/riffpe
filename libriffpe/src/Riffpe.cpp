#include <riffpe/Riffpe.hpp>
#include <riffpe/AESEngine.hpp>

#include <algorithm>
#include <array>
#include <stdexcept>
#include <string>
#include <string_view>
#include <vector>

#include <cstring>

namespace riffpe
{
    using aes_engine_type = crypto::AESEngine;

    Riffpe::Riffpe(uint32_t c, uint32_t l, const uint8_t* key, size_t key_length, const uint8_t* tweak, size_t tweak_length, uint32_t chop)
        : _c(c), _l(l), _chop(chop), _aes_engine(aes_engine_type::engine_factory())
    {
        _perm_bytes_per_value = 16 / chop;
        _perm_msg_len = _perm_bytes_per_value * _c;

        if(c < 256)
            _el_size = sizeof(uint8_t);
        else if(c < 65536)
            _el_size = sizeof(uint16_t);
        else if(c < 4294967296)
            _el_size = sizeof(uint32_t);
        else
            throw std::length_error("Radix too big (must be < 32 bits)");

        _tweak_buf.resize(sizeof(_c) + sizeof(_l) + 2 + tweak_length);
        // FIXME: add non-LE version, like in generic AES
        std::memcpy(_tweak_buf.data() + 0, &_c, 4);
        _tweak_buf[4] = '_';
        std::memcpy(_tweak_buf.data() + 5, &_l, 4);
        _tweak_buf[9] = '^';
        std::memcpy(_tweak_buf.data() + 10, tweak, tweak_length);
        // add standard pkcs7 padding
        uint8_t padding_byte = int(aes_engine_type::block_size) + (-int(_tweak_buf.size()) % int(aes_engine_type::block_size));
        _tweak_buf.insert(_tweak_buf.end(), padding_byte, padding_byte);

        _aes_engine->set_key(key, key_length);

        // Absorb tweak prefix into the AES state
        std::memset(_aes_state_template.data(), 0, aes_engine_type::block_size);
        _aes_engine->encrypt_cbc(_tweak_buf.data(), nullptr, _tweak_buf.size() / aes_engine_type::block_size, _aes_state_template.data());
    }

    template<typename ElType, bool Inverse>
    ElType Riffpe::perm(ElType x, aes_state_type& aes_state)
    {
        size_t _perm_msg_len_blocks = (_perm_msg_len + aes_engine_type::block_size - 1)
                                    / aes_engine_type::block_size;
        size_t _perm_msg_len_padded = _perm_msg_len_blocks
                                    * aes_engine_type::block_size;
        // Use AES-CBC as a PRNG to generate _perm_msg_len bytes
        std::vector<uint8_t> _perm_state(_perm_msg_len_padded);
        _aes_engine->encrypt_cbc(nullptr, _perm_state.data(), _perm_msg_len_blocks, aes_state.data());
        using bytes_view = std::basic_string_view<uint8_t>;
        using permutation_element = std::tuple<bytes_view, ElType>;

        std::vector<permutation_element> permutation(_c);
        for(ElType i = 0; i < _c; ++i)
        {
            permutation[i] = { {_perm_state.data() + i*_perm_bytes_per_value, _perm_bytes_per_value}, i };
        }
        std::sort(permutation.begin(), permutation.end());
        if constexpr (Inverse)
        {
            ElType y = 0;
            for(ElType i = 0; i<_c; ++i)
                if(std::get<1>(permutation[i]) == x)
                    y = i;
            return y;
        }
        else
        {
            return std::get<1>(permutation[x]);
        }
    }

    template<typename ElType, bool Inverse>
    void Riffpe::round(uint32_t f, ElType* message)
    {
        size_t tweak_len = sizeof(ElType) * _l;
        size_t tweak_padded_blocks = (tweak_len + aes_engine_type::block_size - 1)
                                   / aes_engine_type::block_size;
        for(int i=0; i<_l; ++i)
        {
            int j = Inverse
                  ? (_l - i - 1)
                  : i;
            auto aes_state = _aes_state_template;
            ElType x = message[j];
            // Fixme: use some kind of f marker instead of f
            message[j] = f;
            message[_l] = j;
            // Absorb the message view (+f marker) as the rest of tweak into the AES state
            // This is equivalent to computing CBC-MAC into aes_state.
            _aes_engine->encrypt_cbc(reinterpret_cast<const uint8_t*>(message), nullptr, 
                                     tweak_padded_blocks, aes_state.data());
            ElType y = perm<ElType, Inverse>(x, aes_state);
            message[j] = y;
        }
    }

    template<typename ElType, bool Inverse>
    void Riffpe::enc_dec_impl(std::vector<uint32_t>& message)
    {
        size_t tweak_len = sizeof(ElType) * (_l + 1);
        size_t tweak_padded_blocks = (tweak_len + aes_engine_type::block_size - 1)
                                   / aes_engine_type::block_size;
        size_t tweak_padded_size   = tweak_padded_blocks
                                   * aes_engine_type::block_size;
        size_t el_count_padded = tweak_padded_size / sizeof(ElType);

        std::vector<ElType> message_buf(el_count_padded, 0);
        for(int i=0; i<_l; ++i)
            message_buf[i] = message[i];
        
        if constexpr (!Inverse)
        {
            // Absorbing phase
            round<ElType, Inverse>(0, message_buf.data());
            // Squeezing phase
            round<ElType, Inverse>(1, message_buf.data());
        }
        else
        {
            // Inverse absorbing phase
            round<ElType, Inverse>(1, message_buf.data());
            // Inverse squeezing phase
            round<ElType, Inverse>(0, message_buf.data());
        }

        for(int i=0; i<_l; ++i)
            message[i] = message_buf[i];
    }

    template void Riffpe::enc_dec_impl<uint8_t,  false>(std::vector<uint32_t>&);
    template void Riffpe::enc_dec_impl<uint16_t, false>(std::vector<uint32_t>&);
    template void Riffpe::enc_dec_impl<uint32_t, false>(std::vector<uint32_t>&);
    template void Riffpe::enc_dec_impl<uint8_t,  true>(std::vector<uint32_t>&);
    template void Riffpe::enc_dec_impl<uint16_t, true>(std::vector<uint32_t>&);
    template void Riffpe::enc_dec_impl<uint32_t, true>(std::vector<uint32_t>&);
}
