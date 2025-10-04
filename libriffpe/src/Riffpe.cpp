#include "../include/riffpe/Riffpe.hpp"
#include "../include/riffpe/AESEngine.hpp"

#include <vector>

#include <cstring>

#include "RifflePerm.hpp"
#include "riffpe_detail.hpp"
#include "mem_utils.hpp"  // store_u32_le

namespace riffpe
{
    using aes_engine_type = crypto::AESEngine;

    Riffpe::Riffpe(
        uint32_t radix, 
        uint32_t digits,
        const uint8_t* key, 
        size_t key_length, 
        const uint8_t* tweak, 
        size_t tweak_length, 
        uint32_t bytes_per_value
    )
        : _radix(radix), _digits(digits), _bytes_per_value(bytes_per_value), _aes_engine(aes_engine_type::engine_factory())
    {
        _el_size = detail::_validate_params(_radix, _digits);

        static_assert(sizeof(uint32_t)*2 + sizeof(uint64_t) == 16);
        std::vector<uint8_t> _tweak_buf;
        _tweak_buf.reserve(sizeof(uint32_t)*2 + sizeof(uint64_t) + tweak_length);
        riffpe::util::push_u32_le(_tweak_buf, _radix);
        riffpe::util::push_u32_le(_tweak_buf, _digits);
        riffpe::util::push_u64_le(_tweak_buf, tweak_length);
        _tweak_buf.insert(_tweak_buf.end(), tweak, tweak + tweak_length);
        // add standard pkcs7 padding
        riffpe::util::push_pkcs7_padding(_tweak_buf, aes_engine_type::block_size);

        _aes_engine->set_key(key, key_length);

        // Absorb tweak prefix into the AES state
        std::memset(_aes_state_template.data(), 0, aes_engine_type::block_size);
        _aes_engine->encrypt_cbc(_tweak_buf.data(), nullptr, _tweak_buf.size() / aes_engine_type::block_size, _aes_state_template.data());

        _perm_fwd = RifflePermBase::make_unique_fwd(_el_size, _bytes_per_value, _radix, *_aes_engine);
        _perm_rev = RifflePermBase::make_unique_rev(_el_size, _bytes_per_value, _radix, *_aes_engine);
    }

    Riffpe::Riffpe(Riffpe&&) = default;
    Riffpe::~Riffpe() = default;

    template<typename ElType, bool Inverse>
    void Riffpe::round(uint32_t f, detail::message_span_type<ElType> message)
    {
        auto& perm_fwd = dynamic_cast<RifflePermFwd<ElType>&>(*_perm_fwd);
        auto& perm_rev = dynamic_cast<RifflePermRev<ElType>&>(*_perm_rev);

        for(int i=0; i<_digits; ++i)
        {
            int j = Inverse
                  ? (_digits - i - 1)
                  : i;
            auto aes_state = _aes_state_template;
            ElType x = message.data.as_elems[j];
            message.data.as_elems[j] = f;
            message.data.as_elems[_digits] = j;
            // Absorb the message view (+f marker) as the rest of tweak into the AES state
            // This is equivalent to computing CBC-MAC into aes_state.
            _aes_engine->encrypt_cbc(message.data.as_bytes, nullptr, 
                                     message.byte_size / aes_engine_type::block_size, aes_state.data());
            if constexpr (Inverse)
                message.data.as_elems[j] = perm_rev.reverse(aes_state, x);
            else
                message.data.as_elems[j] = perm_fwd.forward(aes_state, x);
        }
    }

    template void detail::enc_dec_impl<uint8_t,  false, Riffpe>(std::vector<uint32_t>&, Riffpe*);
    template void detail::enc_dec_impl<uint16_t, false, Riffpe>(std::vector<uint32_t>&, Riffpe*);
    template void detail::enc_dec_impl<uint32_t, false, Riffpe>(std::vector<uint32_t>&, Riffpe*);
    template void detail::enc_dec_impl<uint8_t,  true, Riffpe>(std::vector<uint32_t>&, Riffpe*);
    template void detail::enc_dec_impl<uint16_t, true, Riffpe>(std::vector<uint32_t>&, Riffpe*);
    template void detail::enc_dec_impl<uint32_t, true, Riffpe>(std::vector<uint32_t>&, Riffpe*);
}
