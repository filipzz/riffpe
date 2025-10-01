#pragma once

#include <riffpe/AESEngine.hpp>

#include <algorithm>
#include <stdexcept>
#include <string_view>
#include <vector>

#include <cstdint>

namespace riffpe
{
    class RifflePermBase
    {
    protected:
        using aes_engine_type = crypto::AESEngine;
        using aes_state_type  = std::array<uint8_t, aes_engine_type::block_size>;
    public:
        virtual ~RifflePermBase() {}
        virtual void recompute(aes_state_type& prng_iv) = 0;

        static std::unique_ptr<RifflePermBase> make_unique(uint32_t el_size, uint32_t bytes_per_value, uint32_t elements, aes_engine_type& prng);
    };

    template<typename ElType>
    class RifflePerm : public RifflePermBase
    {
    public:
        virtual ~RifflePerm() {}
        virtual ElType forward(ElType) = 0;
        virtual ElType reverse(ElType) = 0;

        static std::unique_ptr<RifflePerm<ElType>> make_unique(uint32_t bytes_per_value, uint32_t elements, aes_engine_type& prng);
    };

    template<typename ElType>
    class RifflePermImpl : public RifflePerm<ElType>
    {
    protected:
        using typename RifflePermBase::aes_engine_type;
        using typename RifflePermBase::aes_state_type;
        using bytes_view = std::basic_string_view<uint8_t>;
        using permutation_element = std::tuple<bytes_view, ElType>;

        uint32_t _elements;
        aes_engine_type& _aes_engine;

        uint32_t _el_size;
        uint32_t _perm_msg_len;
        uint32_t _perm_msg_len_blocks;
        uint32_t _perm_msg_len_padded;
        uint32_t _perm_bytes_per_value;
        std::vector<uint8_t> _perm_state;
        std::vector<permutation_element> _permutation;
            
    public:
        using element_type = ElType;

        RifflePermImpl(
            uint32_t elements,
            aes_engine_type& prng, 
            uint32_t bytes_per_value
        ) : _elements(elements), _aes_engine(prng), _permutation(elements), _perm_bytes_per_value(bytes_per_value)
        {
            _perm_msg_len = _perm_bytes_per_value * _elements;
            _perm_msg_len_blocks = (_perm_msg_len + aes_engine_type::block_size - 1)
                                 / aes_engine_type::block_size;
            _perm_msg_len_padded = _perm_msg_len_blocks
                                 * aes_engine_type::block_size;
            // Use AES-CBC as a PRNG to generate _perm_msg_len bytes
            _perm_state.resize(_perm_msg_len_padded);
        }
        virtual ~RifflePermImpl() {}

        inline void recompute(aes_state_type& prng_iv) override
        {
            _aes_engine.encrypt_cbc(nullptr, _perm_state.data(), _perm_msg_len_blocks, prng_iv.data());
            for(ElType i = 0; i < _elements; ++i)
            {
                _permutation[i] = { {_perm_state.data() + i*_perm_bytes_per_value, _perm_bytes_per_value}, i };
            }
            std::sort(_permutation.begin(), _permutation.end());
        }

        inline ElType forward(ElType x) override
        {
            return std::get<1>(_permutation[x]);
        }

        inline ElType reverse(ElType x) override
        {
            ElType y = 0;
            for(ElType i = 0; i<_elements; ++i)
                if(std::get<1>(_permutation[i]) == x)
                    y = i;
            return y;
        }

    };

    template<typename ElType>
    std::unique_ptr<RifflePerm<ElType>> inline RifflePerm<ElType>::make_unique(uint32_t bytes_per_value, uint32_t elements, aes_engine_type& prng)
    {
        using ret = std::unique_ptr<RifflePerm<ElType>>;
        return ret(new RifflePermImpl<ElType>(elements, prng, bytes_per_value));
    }

    std::unique_ptr<RifflePermBase> inline RifflePermBase::make_unique(uint32_t el_size, uint32_t bytes_per_value, uint32_t elements, aes_engine_type& prng)
    {
        switch(el_size)
        {
            case sizeof(uint32_t): return RifflePerm<uint32_t>::make_unique(bytes_per_value, elements, prng);
            case sizeof(uint16_t): return RifflePerm<uint16_t>::make_unique(bytes_per_value, elements, prng);
            case sizeof(uint8_t):  return RifflePerm<uint8_t >::make_unique(bytes_per_value, elements, prng);
            default: throw std::length_error("Invalid element size");
        }
    }
}
