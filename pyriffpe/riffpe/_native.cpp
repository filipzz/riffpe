#include <riffpe/Riffpe.hpp>
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
using riffpe::crypto::AESEngine;


class CBCTweakablePRNG
{
protected:
    using aes_engine_type = AESEngine;
    using aes_engine_ptr  = aes_engine_type*;
    using aes_state_type  = std::array<uint8_t, aes_engine_type::block_size>;
    
    aes_engine_ptr _aes_engine;
    aes_state_type _state;

public:
    CBCTweakablePRNG(const py::bytes& key, const py::bytes& tweak)
     : _aes_engine(aes_engine_type::engine_factory())
    {
        py::buffer_info key_info(py::buffer(key).request());
        _aes_engine->set_key(reinterpret_cast<const uint8_t*>(key_info.ptr), key_info.shape[0]);
        ::memset(_state.data(), 0, _state.size());
        // Absorb tweak into CBC state, effectively computing CBC-MAC
        py::buffer_info tweak_info(py::buffer(tweak).request());
        size_t tweak_len = tweak_info.shape[0];
        if((tweak_len % 16) != 0)
            throw std::length_error("Not implemented: `tweak_len` not divisible by 16");
        _aes_engine->encrypt_cbc(reinterpret_cast<const uint8_t*>(tweak_info.ptr), nullptr, tweak_len / 16, _state.data());
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


Riffpe make_riffpe_py(uint32_t c, uint32_t l, py::bytes key, py::bytes tweak, uint32_t chop)
{
    py::buffer_info key_info(py::buffer(key).request());
    size_t key_len = key_info.shape[0];

    py::buffer_info tweak_info(py::buffer(tweak).request());
    size_t tweak_len = tweak_info.shape[0];

    return Riffpe(c, l, reinterpret_cast<const uint8_t*>(key_info.ptr), key_len, reinterpret_cast<const uint8_t*>(tweak_info.ptr), tweak_len, chop);
}

PYBIND11_MODULE(_native, m)
{
    m.doc() = "Native Riffpe tools";

    py::class_<CBCTweakablePRNG>(m, "CBCTweakablePRNG")
        .def(py::init<py::bytes, py::bytes>())
        .def("get_bytes", &CBCTweakablePRNG::get_bytes)
        .def_property_readonly("block_size", &CBCTweakablePRNG::block_size)
        ;
    
    py::class_<Riffpe>(m, "Riffpe")
        .def(py::init<>(&make_riffpe_py), 
             py::arg("c"), py::arg("l"), py::arg("key"), py::arg("tweak"), py::arg("chop") = 1)
        .def("enc", &Riffpe::enc)
        .def("dec", &Riffpe::dec)
        .def("_aes_engine_id", &Riffpe::aes_engine_id)
        ;
}
