#include <riffpe/RiffpeX.hpp>
#include <riffpe/AESEngine.hpp>

#include "RifflePerm.hpp"
#include "riffpe_detail.hpp"
#include "riffpe_detail.hpp"
#include "mem_utils.hpp"

#include <algorithm>
#include <stdexcept>
#include <vector>

#include <cstring>

namespace riffpe
{
    using aes_engine_type = crypto::AESEngine;

    RiffpeX::RiffpeX(uint32_t* c_begin, uint32_t* c_end, const uint8_t* key, size_t key_length, const uint8_t* tweak, size_t tweak_length, uint32_t chop)
        : _cs(c_begin, c_end), _l(c_end - c_begin), _chop(chop), _aes_engine(aes_engine_type::engine_factory())
    {
        uint32_t maxc = *std::max_element(c_begin, c_end);
        _el_size = detail::_validate_params(maxc, _l, chop);

        std::vector<uint8_t> _tweak_buf((sizeof(maxc) + 1) * _l + tweak_length);
        uint8_t* uptr = _tweak_buf.data();
        for(const uint32_t& c : _cs)  // _validate_params ensures there is at least one element in _cs
        {
            util::store_u32_le(uptr, c);
            uptr[4] = ':';
            uptr += 5;
        }
        // Change the last ':' to '^'
        uptr[-1] = '^';
        std::memcpy(uptr, tweak, tweak_length);
        // add standard pkcs7 padding
        uint8_t padding_byte = int(aes_engine_type::block_size) + (-int(_tweak_buf.size()) % int(aes_engine_type::block_size));
        _tweak_buf.insert(_tweak_buf.end(), padding_byte, padding_byte);

        _aes_engine->set_key(key, key_length);

        // Absorb tweak prefix into the AES state
        std::memset(_aes_state_template.data(), 0, aes_engine_type::block_size);
        _aes_engine->encrypt_cbc(_tweak_buf.data(), nullptr, _tweak_buf.size() / aes_engine_type::block_size, _aes_state_template.data());

        for(auto c : _cs)
            _perms.emplace_back(RifflePermBase::make_unique(_el_size, _chop, c, *_aes_engine));
    }

    RiffpeX::RiffpeX(RiffpeX&&) = default;
    RiffpeX::~RiffpeX() = default;    

    template<typename ElType, bool Inverse>
    void RiffpeX::round(uint32_t f, ElType* message)
    {
        size_t tweak_len = sizeof(ElType) * _l;
        size_t tweak_padded_blocks = (tweak_len + aes_engine_type::block_size - 1)
                                   / aes_engine_type::block_size;
        for(int i=0; i<_l; ++i)
        {
            int j = Inverse
                  ? (_l - i - 1)
                  : i;
            auto& perm = dynamic_cast<RifflePerm<ElType>&>(*_perms[j]);
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

    template void detail::enc_dec_impl<uint8_t,  false, RiffpeX>(std::vector<uint32_t>&, RiffpeX*);
    template void detail::enc_dec_impl<uint16_t, false, RiffpeX>(std::vector<uint32_t>&, RiffpeX*);
    template void detail::enc_dec_impl<uint32_t, false, RiffpeX>(std::vector<uint32_t>&, RiffpeX*);
    template void detail::enc_dec_impl<uint8_t,  true, RiffpeX>(std::vector<uint32_t>&, RiffpeX*);
    template void detail::enc_dec_impl<uint16_t, true, RiffpeX>(std::vector<uint32_t>&, RiffpeX*);
    template void detail::enc_dec_impl<uint32_t, true, RiffpeX>(std::vector<uint32_t>&, RiffpeX*);
}
