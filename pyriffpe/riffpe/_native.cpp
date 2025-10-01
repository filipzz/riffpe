#include <riffpe/Riffpe.hpp>
#include <riffpe/RiffpeX.hpp>
#include <riffpe/AESEngine.hpp>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <algorithm>
#include <array>
#include <string>
#include <string_view>
#include <vector>

#include <cstring>

namespace py = pybind11;
using riffpe::Riffpe;
using riffpe::RiffpeX;
using riffpe::crypto::AESEngine;


class CBCTweakablePRNG
{
protected:
    using aes_engine_type = AESEngine;
    using aes_engine_ptr  = aes_engine_type*;
    using aes_state_type  = std::array<uint8_t, aes_engine_type::block_size>;
    
    aes_engine_ptr _aes_engine;
    aes_state_type _state;

    void _absorb_tweak(const py::bytes& tweak)
    {
        // Absorb tweak into CBC state, effectively computing CBC-MAC
        py::buffer_info tweak_info(py::buffer(tweak).request());
        size_t tweak_len = tweak_info.shape[0];
        if((tweak_len % 16) != 0)
            throw std::length_error("Not implemented: `tweak_len` not divisible by 16");
        _aes_engine->encrypt_cbc(reinterpret_cast<const uint8_t*>(tweak_info.ptr), nullptr, tweak_len / 16, _state.data());
    }

public:
    CBCTweakablePRNG(const py::bytes& key, const py::bytes& tweak)
     : _aes_engine(aes_engine_type::engine_factory())
    {
        py::buffer_info key_info(py::buffer(key).request());
        _aes_engine->set_key(reinterpret_cast<const uint8_t*>(key_info.ptr), key_info.shape[0]);
        reset(tweak);
    };

    CBCTweakablePRNG(const py::bytes& key, const py::bytes& tweak, const py::bytes& iv)
     : _aes_engine(aes_engine_type::engine_factory())
    {
        py::buffer_info key_info(py::buffer(key).request());
        _aes_engine->set_key(reinterpret_cast<const uint8_t*>(key_info.ptr), key_info.shape[0]);
        reset(tweak, iv);
    };

    void reset(const py::bytes& tweak)
    {
        ::memset(_state.data(), 0, _state.size());
        _absorb_tweak(tweak);
    };

    void reset(const py::bytes& tweak, const py::bytes& iv)
    {
        py::buffer_info iv_info(py::buffer(iv).request());
        if(iv_info.shape[0] != 16)
            throw std::length_error("Invalid IV length, must be 16");
        ::memcpy(_state.data(), iv_info.ptr, _state.size());
        _absorb_tweak(tweak);
    };

    ~CBCTweakablePRNG() { if(_aes_engine) { delete _aes_engine; } }

    py::bytes get_bytes(size_t count)
    {
        std::string result(count, '\0');
        if((count % 16) != 0)
            throw std::length_error("Not implemented: `count` not divisible by 16");
        _aes_engine->encrypt_cbc(nullptr, reinterpret_cast<uint8_t*>(result.data()), count / 16, _state.data());
        return py::bytes(result);
    }

    size_t block_size() const { return aes_engine_type::block_size; }
};


Riffpe make_riffpe_py(uint32_t radix, uint32_t digits, py::bytes key, py::bytes tweak, uint32_t bytes_per_value)
{
    py::buffer_info key_info(py::buffer(key).request());
    size_t key_len = key_info.shape[0];

    py::buffer_info tweak_info(py::buffer(tweak).request());
    size_t tweak_len = tweak_info.shape[0];

    return Riffpe(radix, digits, reinterpret_cast<const uint8_t*>(key_info.ptr), key_len, reinterpret_cast<const uint8_t*>(tweak_info.ptr), tweak_len, bytes_per_value);
}


RiffpeX make_riffpex_py(std::vector<uint32_t> radices, py::bytes key, py::bytes tweak, uint32_t bytes_per_value)
{
    py::buffer_info key_info(py::buffer(key).request());
    size_t key_len = key_info.shape[0];

    py::buffer_info tweak_info(py::buffer(tweak).request());
    size_t tweak_len = tweak_info.shape[0];

    return RiffpeX(radices.data(), radices.data() + radices.size(), reinterpret_cast<const uint8_t*>(key_info.ptr), key_len, reinterpret_cast<const uint8_t*>(tweak_info.ptr), tweak_len, bytes_per_value);
}

PYBIND11_MODULE(_native, m)
{
    m.doc() = "Native Riffpe tools";

    py::class_<CBCTweakablePRNG>(m, "CBCTweakablePRNG")
        .def(py::init<py::bytes, py::bytes>())
        .def(py::init<py::bytes, py::bytes, py::bytes>())
        .def("reset", py::overload_cast<const py::bytes&>(&CBCTweakablePRNG::reset))
        .def("reset", py::overload_cast<const py::bytes&, const py::bytes&>(&CBCTweakablePRNG::reset))
        .def("get_bytes", &CBCTweakablePRNG::get_bytes)
        .def_property_readonly("block_size", &CBCTweakablePRNG::block_size)
        ;
    
    py::class_<Riffpe>(m, "Riffpe")
        .def(py::init<>(&make_riffpe_py), 
             py::arg("c"), py::arg("l"), py::arg("key"), py::arg("tweak"), py::arg("bytes_per_value") = 16)
        .def("encrypt", &Riffpe::encrypt)
        .def("decrypt", &Riffpe::decrypt)
        .def("_aes_engine_id", &Riffpe::aes_engine_id)
        ;
    
    py::class_<RiffpeX>(m, "RiffpeX")
        .def(py::init<>(&make_riffpex_py), 
             py::arg("cs"), py::arg("key"), py::arg("tweak"), py::arg("bytes_per_value") = 16)
        .def("encrypt", &RiffpeX::encrypt)
        .def("decrypt", &RiffpeX::decrypt)
        .def("_aes_engine_id", &RiffpeX::aes_engine_id)
        ;
}
