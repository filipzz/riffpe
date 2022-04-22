#include "aes.hpp"

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <string>
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


PYBIND11_MODULE(riffpe_native, m)
{
    m.doc() = "Native Riffpe tools";

    py::class_<CBCTweakablePRNG>(m, "CBCTweakablePRNG")
        .def(py::init<py::bytes, py::bytes>())
        .def("get_bytes", &CBCTweakablePRNG::get_bytes)
        .def_property_readonly("block_size", &CBCTweakablePRNG::block_size)
        ;
}
