#include "aes.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <algorithm>
#include <array>
#include <string>
#include <string_view>
#include <vector>

#include <cstring>

namespace py = pybind11;


class CBCTweakablePRNG
{
protected:
    using aes_engine_type = riffpe::crypto::AESEngine;
    aes_engine_type aes_engine;
    std::array<uint8_t, aes_engine_type::block_size> state;

public:
    CBCTweakablePRNG(const py::bytes& key, const py::bytes& tweak)
    {
        py::buffer_info key_info(py::buffer(key).request());
        aes_engine.set_key(reinterpret_cast<const uint8_t*>(key_info.ptr), key_info.shape[0]);
        ::memset(state.data(), 0, state.size());
        // Absorb tweak into CBC state, effectively computing CBC-MAC
        py::buffer_info tweak_info(py::buffer(tweak).request());
        size_t tweak_len = tweak_info.shape[0];
        if((tweak_len % 16) != 0)
            throw std::length_error("Not implemented: `tweak_len` not divisible by 16");
        aes_engine.encrypt_cbc(reinterpret_cast<const uint8_t*>(tweak_info.ptr), nullptr, tweak_len / 16, state.data());
    };

    py::bytes get_bytes(size_t count)
    {
        std::string result(count, '\0');
        if((count % 16) != 0)
            throw std::length_error("Not implemented: `count` not divisible by 16");
        aes_engine.encrypt_cbc(nullptr, reinterpret_cast<uint8_t*>(result.data()), count / 16, state.data());
        return py::bytes(result);
    }

    size_t block_size() const { return riffpe::crypto::AESEngine::block_size; }
};


class Riffpe
{
protected:
    const uint32_t _c;
    const uint32_t _l;
    const uint32_t _chop;
    std::vector<uint8_t> _tweak;

    uint32_t _el_size;
    uint32_t _perm_msg_len;
    uint32_t _perm_bytes_per_value;

    using aes_engine_type = riffpe::crypto::AESEngine;
    using aes_state_type = std::array<uint8_t, aes_engine_type::block_size>;
    
    aes_engine_type _aes_engine;
    aes_state_type _aes_state_template;

public:
    Riffpe(uint32_t c, uint32_t l, py::bytes key, py::bytes tweak, uint32_t chop = 1)
        : _c(c), _l(l), _chop(chop)
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

        py::buffer_info tweak_info(py::buffer(tweak).request());
        size_t tweak_len = tweak_info.shape[0];
        _tweak.resize(sizeof(_c) + sizeof(_l) + 2 + tweak_len);
        // FIXME: add non-LE version, like in generic AES
        std::memcpy(_tweak.data() + 0, &_c, 4);
        _tweak[4] = '_';
        std::memcpy(_tweak.data() + 5, &_l, 4);
        _tweak[9] = '^';
        std::memcpy(_tweak.data() + 10, tweak_info.ptr, tweak_len);
        // add standard pkcs7 padding
        uint8_t padding_byte = int(aes_engine_type::block_size) + (-int(_tweak.size()) % int(aes_engine_type::block_size));
        _tweak.insert(_tweak.end(), padding_byte, padding_byte);

        py::buffer_info key_info(py::buffer(key).request());
        size_t key_len = key_info.shape[0];
        _aes_engine.set_key(reinterpret_cast<const uint8_t*>(key_info.ptr), key_len);

        // Absorb tweak prefix into the AES state
        std::memset(_aes_state_template.data(), 0, aes_engine_type::block_size);
        _aes_engine.encrypt_cbc(_tweak.data(), nullptr, _tweak.size() / aes_engine_type::block_size, _aes_state_template.data());
    }

    template<typename ElType, bool Inverse>
    ElType perm(ElType x, aes_state_type& aes_state)
    {
        size_t _perm_msg_len_blocks = (_perm_msg_len + aes_engine_type::block_size - 1)
                                    / aes_engine_type::block_size;
        size_t _perm_msg_len_padded = _perm_msg_len_blocks
                                    * aes_engine_type::block_size;
        // Use AES-CBC as a PRNG to generate _perm_msg_len bytes
        std::vector<uint8_t> _perm_state(_perm_msg_len_padded);
        _aes_engine.encrypt_cbc(nullptr, _perm_state.data(), _perm_msg_len_blocks, aes_state.data());
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
    void round(uint32_t f, ElType* message)
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
            // Absorb the message view (+f marker) as the rest of tweak into the AES state
            // This is equivalent to computing CBC-MAC into aes_state.
            _aes_engine.encrypt_cbc(reinterpret_cast<const uint8_t*>(message), nullptr, 
                                    tweak_padded_blocks, aes_state.data());
            ElType y = perm<ElType, Inverse>(x, aes_state);
            message[j] = y;
        }
    }

    template<typename ElType, bool Inverse>
    void enc_dec_impl(std::vector<uint32_t>& message)
    {
        size_t tweak_len = sizeof(ElType) * _l;
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
};


PYBIND11_MODULE(riffpe_native, m)
{
    m.doc() = "Native Riffpe tools";

    py::class_<CBCTweakablePRNG>(m, "CBCTweakablePRNG")
        .def(py::init<py::bytes, py::bytes>())
        .def("get_bytes", &CBCTweakablePRNG::get_bytes)
        .def_property_readonly("block_size", &CBCTweakablePRNG::block_size)
        ;
    
    py::class_<Riffpe>(m, "Riffpe")
        .def(py::init<uint32_t, uint32_t, py::bytes, py::bytes, uint32_t>(), 
             py::arg("c"), py::arg("l"), py::arg("key"), py::arg("tweak"), py::arg("chop") = 1)
        .def("enc", &Riffpe::enc)
        .def("dec", &Riffpe::dec)
        ;
}
