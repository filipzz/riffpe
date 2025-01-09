#include <riffpe/Riffpe.hpp>
#include <riffpe/AESEngine.hpp>

#include "RifflePerm.hpp"
#include "riffpe_detail.hpp"
#include "mem_utils.hpp"  // store_u32_le

#include <algorithm>
#include <stdexcept>
#include <vector>

#include <cstring>

namespace riffpe
{
    using aes_engine_type = crypto::AESEngine;

    Riffpe::Riffpe(uint32_t c, uint32_t l, const uint8_t* key, size_t key_length, const uint8_t* tweak, size_t tweak_length, uint32_t chop)
        : _c(c), _l(l), _chop(chop), _aes_engine(aes_engine_type::engine_factory())
    {
        _el_size = detail::_validate_params(_c, _l, _chop);

        static_assert(sizeof(uint32_t)*2 + sizeof(uint64_t) == 16);
        std::vector<uint8_t> _tweak_buf;
        _tweak_buf.reserve(sizeof(uint32_t)*2 + sizeof(uint64_t) + tweak_length);
        riffpe::util::push_u32_le(_tweak_buf, _c);
        riffpe::util::push_u32_le(_tweak_buf, _l);
        riffpe::util::push_u64_le(_tweak_buf, tweak_length);
        _tweak_buf.insert(_tweak_buf.end(), tweak, tweak + tweak_length);
        // add standard pkcs7 padding
        uint8_t padding_byte = int(aes_engine_type::block_size) + (-int(_tweak_buf.size()) % int(aes_engine_type::block_size));
        _tweak_buf.insert(_tweak_buf.end(), padding_byte, padding_byte);

        _aes_engine->set_key(key, key_length);

        // Absorb tweak prefix into the AES state
        std::memset(_aes_state_template.data(), 0, aes_engine_type::block_size);
        _aes_engine->encrypt_cbc(_tweak_buf.data(), nullptr, _tweak_buf.size() / aes_engine_type::block_size, _aes_state_template.data());

        _perm = RifflePermBase::make_unique(_el_size, _chop, c, *_aes_engine);
    }

    Riffpe::Riffpe(Riffpe&&) = default;
    Riffpe::~Riffpe() = default;

    template<typename ElType, bool Inverse>
    void Riffpe::round(uint32_t f, ElType* message)
    {
        size_t tweak_len = sizeof(ElType) * _l;
        size_t tweak_padded_blocks = (tweak_len + aes_engine_type::block_size - 1)
                                   / aes_engine_type::block_size;
        auto& perm = dynamic_cast<RifflePerm<ElType>&>(*_perm);

        for(int i=0; i<_l; ++i)
        {
            int j = Inverse
                  ? (_l - i - 1)
                  : i;
            auto aes_state = _aes_state_template;
            ElType x = message[j];
            message[j] = f;
            message[_l] = j;
            // Absorb the message view (+f marker) as the rest of tweak into the AES state
            // This is equivalent to computing CBC-MAC into aes_state.
            _aes_engine->encrypt_cbc(reinterpret_cast<const uint8_t*>(message), nullptr, 
                                     tweak_padded_blocks, aes_state.data());
            perm.recompute(aes_state);
            if constexpr (Inverse)
                message[j] = perm.reverse(x);
            else
                message[j] = perm.forward(x);
        }
    }

    template void detail::enc_dec_impl<uint8_t,  false, Riffpe>(std::vector<uint32_t>&, Riffpe*);
    template void detail::enc_dec_impl<uint16_t, false, Riffpe>(std::vector<uint32_t>&, Riffpe*);
    template void detail::enc_dec_impl<uint32_t, false, Riffpe>(std::vector<uint32_t>&, Riffpe*);
    template void detail::enc_dec_impl<uint8_t,  true, Riffpe>(std::vector<uint32_t>&, Riffpe*);
    template void detail::enc_dec_impl<uint16_t, true, Riffpe>(std::vector<uint32_t>&, Riffpe*);
    template void detail::enc_dec_impl<uint32_t, true, Riffpe>(std::vector<uint32_t>&, Riffpe*);
}
