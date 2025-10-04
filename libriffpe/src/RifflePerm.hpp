#pragma once

#include "../include/riffpe/AESEngine.hpp"

#include <memory>
#include <stdexcept>
#include <vector>

#include <cstdint>

#include "radix_tree.hpp"

namespace riffpe
{
    class RifflePermBase
    {
    protected:
        using aes_engine_type = crypto::AESEngine;
        using aes_state_type  = std::array<uint8_t, aes_engine_type::block_size>;
    public:
        virtual ~RifflePermBase() {}

        static std::unique_ptr<RifflePermBase> make_unique_fwd(uint32_t el_size, uint32_t bytes_per_value, uint32_t elements, aes_engine_type& prng);
        static std::unique_ptr<RifflePermBase> make_unique_rev(uint32_t el_size, uint32_t bytes_per_value, uint32_t elements, aes_engine_type& prng);
    };

    template<typename ElType>
    class RifflePermCommon : public RifflePermBase
    {
    protected:
        using typename RifflePermBase::aes_engine_type;
        using typename RifflePermBase::aes_state_type;
        using bytes_view = typename radix_tree<ElType>::bytes_view;
        using permutation_element = typename radix_tree<ElType>::element_type;

        uint32_t _elements;
        aes_engine_type& _aes_engine;

        uint32_t _el_size;
        uint32_t _perm_msg_len;
        uint32_t _perm_msg_len_blocks;
        uint32_t _perm_msg_len_padded;
        uint32_t _perm_bytes_per_value;
        std::vector<uint8_t> _perm_state;
            
    public:
        using element_type = ElType;

        RifflePermCommon(
            uint32_t elements,
            aes_engine_type& prng, 
            uint32_t bytes_per_value
        ) : _elements(elements), _aes_engine(prng), _perm_bytes_per_value(bytes_per_value)
        {
            _perm_msg_len = _perm_bytes_per_value * _elements;
            _perm_msg_len_blocks = (_perm_msg_len + aes_engine_type::block_size - 1)
                                 / aes_engine_type::block_size;
            _perm_msg_len_padded = _perm_msg_len_blocks
                                 * aes_engine_type::block_size;
            // Use AES-CBC as a PRNG to generate _perm_msg_len bytes
            _perm_state.resize(_perm_msg_len_padded);
        }
        virtual ~RifflePermCommon() {}
    };

    template<typename ElType>
    class RifflePermFwd : public RifflePermCommon<ElType> {
    protected:
        using typename RifflePermBase::aes_engine_type;
        using typename RifflePermBase::aes_state_type;
        using bytes_view = typename radix_tree<ElType>::bytes_view;
        using permutation_element = typename radix_tree<ElType>::element_type;

        using RifflePermCommon<ElType>::_aes_engine;
        using RifflePermCommon<ElType>::_perm_state;
        using RifflePermCommon<ElType>::_perm_msg_len_blocks;
        using RifflePermCommon<ElType>::_perm_bytes_per_value;
        using RifflePermCommon<ElType>::_elements;

        radix_tree<ElType> _fwd_permutation;
    public:
        RifflePermFwd(
            uint32_t elements,
            aes_engine_type& prng, 
            uint32_t bytes_per_value
        ) : RifflePermCommon<ElType>(elements, prng, bytes_per_value) {
            // 
        }

        inline ElType forward(aes_state_type& prng_iv, ElType x) {
            _aes_engine.encrypt_cbc(nullptr, _perm_state.data(), _perm_msg_len_blocks, prng_iv.data());
            _fwd_permutation.clear();
            for(ElType i = 0; i < _elements; ++i)
                _fwd_permutation.insert({_perm_state.data() + i*_perm_bytes_per_value, _perm_bytes_per_value}, i);
            
            return _fwd_permutation.nth_element(x);
        }
    };

    template<typename ElType>
    class RifflePermRev : public RifflePermCommon<ElType> {
    protected:
        using typename RifflePermBase::aes_engine_type;
        using typename RifflePermBase::aes_state_type;
        using bytes_view = typename radix_tree<ElType>::bytes_view;
        using permutation_element = typename radix_tree<ElType>::element_type;

        using RifflePermCommon<ElType>::_aes_engine;
        using RifflePermCommon<ElType>::_perm_state;
        using RifflePermCommon<ElType>::_perm_msg_len_blocks;
        using RifflePermCommon<ElType>::_perm_bytes_per_value;
        using RifflePermCommon<ElType>::_elements;

        std::vector<permutation_element> _rev_permutation;
    public:
        RifflePermRev(
            uint32_t elements,
            aes_engine_type& prng, 
            uint32_t bytes_per_value
        ) : RifflePermCommon<ElType>(elements, prng, bytes_per_value), _rev_permutation(elements) {
            auto it = _rev_permutation.begin();
            for(ElType i = 0; i < _elements; ++i)
                *it++ = { {_perm_state.data() + i*_perm_bytes_per_value, _perm_bytes_per_value}, i };
        }

        inline ElType reverse(aes_state_type& prng_iv, ElType x) {
            _aes_engine.encrypt_cbc(nullptr, _perm_state.data(), _perm_msg_len_blocks, prng_iv.data());
            auto b = _rev_permutation.begin(), e = _rev_permutation.end(), n = b + x;

            // Simple rank select
            ElType rank = 0;
            for(auto it = b; it < e; ++it)
            {
                if(*it < *n) rank ++;
            }
            return rank;
        }
    };

    std::unique_ptr<RifflePermBase> inline RifflePermBase::make_unique_fwd(uint32_t el_size, uint32_t bytes_per_value, uint32_t elements, aes_engine_type& prng)
    {
        switch(el_size)
        {
            case sizeof(uint32_t): return std::make_unique<RifflePermFwd<uint32_t>>(elements, prng, bytes_per_value);
            case sizeof(uint16_t): return std::make_unique<RifflePermFwd<uint16_t>>(elements, prng, bytes_per_value);
            case sizeof(uint8_t):  return std::make_unique<RifflePermFwd<uint8_t >>(elements, prng, bytes_per_value);
            default: throw std::length_error("Invalid element size");
        }
    }

    std::unique_ptr<RifflePermBase> inline RifflePermBase::make_unique_rev(uint32_t el_size, uint32_t bytes_per_value, uint32_t elements, aes_engine_type& prng)
    {
        switch(el_size)
        {
            case sizeof(uint32_t): return std::make_unique<RifflePermRev<uint32_t>>(elements, prng, bytes_per_value);
            case sizeof(uint16_t): return std::make_unique<RifflePermRev<uint16_t>>(elements, prng, bytes_per_value);
            case sizeof(uint8_t):  return std::make_unique<RifflePermRev<uint8_t >>(elements, prng, bytes_per_value);
            default: throw std::length_error("Invalid element size");
        }
    }
}
