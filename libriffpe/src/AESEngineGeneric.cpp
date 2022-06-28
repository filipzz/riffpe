#include "AESEngineGeneric.hpp"
#include "mem_utils.hpp" // load_u32_le , store_u32_le, extract_byte

#include <exception>
#include <sstream>

namespace riffpe
{
    namespace crypto
    {
        namespace {
            // construct SBox and forward tables in compile-time
            constexpr std::array<uint8_t, 256> FSBox = {
                0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5,
                0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
                0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0,
                0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
                0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC,
                0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
                0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A,
                0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
                0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0,
                0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
                0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B,
                0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
                0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85,
                0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
                0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5,
                0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
                0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17,
                0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
                0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88,
                0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
                0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C,
                0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
                0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9,
                0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
                0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6,
                0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
                0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E,
                0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
                0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94,
                0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
                0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68,
                0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
            };

            constexpr inline uint8_t xtime(uint8_t a)
            {
                uint8_t b = a << 1;
                if(a & 0x80) b ^= 0x1b;
                return b;
            }

            template<int Variant>
            constexpr inline std::array<uint32_t, 256> mkftab()
            {
                static_assert((0 <= Variant) && (Variant <= 3), "Invalid Variant in mkftab");
                std::array<uint32_t, 256> res = {0};
                for(int i=0; i<256; ++i)
                {
                    uint8_t x = FSBox[i];
                    if constexpr (Variant == 0)
                        res[i] = (uint32_t)(xtime(x)) << 0 | (uint32_t)(x) << 8 | (uint32_t)(x) << 16 | (uint32_t)(xtime(x) ^ x) << 24;
                    else if constexpr (Variant == 1)
                        res[i] = (uint32_t)(xtime(x)) << 8 | (uint32_t)(x) << 16 | (uint32_t)(x) << 24 | (uint32_t)(xtime(x) ^ x) << 0;
                    else if constexpr (Variant == 2)
                        res[i] = (uint32_t)(xtime(x)) << 16 | (uint32_t)(x) << 24 | (uint32_t)(x) << 0 | (uint32_t)(xtime(x) ^ x) << 8;
                    else
                        res[i] = (uint32_t)(xtime(x)) << 24 | (uint32_t)(x) << 0 | (uint32_t)(x) << 8 | (uint32_t)(xtime(x) ^ x) << 16;
                }
                return res;
            }

            constexpr std::array<uint32_t, 256> FTab0 = mkftab<0>();
            constexpr std::array<uint32_t, 256> FTab1 = mkftab<1>();
            constexpr std::array<uint32_t, 256> FTab2 = mkftab<2>();
            constexpr std::array<uint32_t, 256> FTab3 = mkftab<3>();
            constexpr std::array<uint32_t, 10> RCons = { 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36 };

            static constexpr inline uint32_t _make_word(uint8_t a, uint8_t b, uint8_t c, uint8_t d)
            {
                return (uint32_t)(a)
                    |  (uint32_t)(b) << 8
                    |  (uint32_t)(c) << 16
                    |  (uint32_t)(d) << 24;
            }

            using namespace util;
        }

        void AESEngineGeneric::set_key(const uint8_t *key, size_t size)
        {
            switch(size)
            {
                case 16:
                {
                    // Load 128-bit key
                    _round_count = 10;
                    _key[0][0] = load_u32_le(key);
                    _key[0][1] = load_u32_le(key+4);
                    _key[0][2] = load_u32_le(key+8);
                    _key[0][3] = load_u32_le(key+12);
                    for(int i=0; i<10; i++)
                    {
                        _key[i+1][0] = _key[i][0] ^ RCons[i] ^ _make_word(
                            FSBox[extract_byte<1>(_key[i][3])],
                            FSBox[extract_byte<2>(_key[i][3])],
                            FSBox[extract_byte<3>(_key[i][3])],
                            FSBox[extract_byte<0>(_key[i][3])]
                        );
                        _key[i+1][1] = _key[i][1] ^ _key[i+1][0];
                        _key[i+1][2] = _key[i][2] ^ _key[i+1][1];
                        _key[i+1][3] = _key[i][3] ^ _key[i+1][2];
                    }
                    break;
                }
                case 24:
                {
                    // Load 192-bit key
                    _round_count = 12;
                    _key[0][0] = load_u32_le(key);
                    _key[0][1] = load_u32_le(key+4);
                    _key[0][2] = load_u32_le(key+8);
                    _key[0][3] = load_u32_le(key+12);
                    _key[1][0] = load_u32_le(key+16);
                    _key[1][1] = load_u32_le(key+20);
                    int i=0, r=1;
                    for(;;)
                    {
                        _key[r][2] = _key[r-1][0] ^ RCons[i++] ^ _make_word(
                            FSBox[extract_byte<1>(_key[r][1])],
                            FSBox[extract_byte<2>(_key[r][1])],
                            FSBox[extract_byte<3>(_key[r][1])],
                            FSBox[extract_byte<0>(_key[r][1])]
                        );
                        _key[r][3] = _key[r-1][1] ^ _key[r][2];

                        r++; // r = 2 mod 3
                        _key[r][0] = _key[r-2][2] ^ _key[r-1][3];
                        _key[r][1] = _key[r-2][3] ^ _key[r  ][0];
                        _key[r][2] = _key[r-1][0] ^ _key[r  ][1];
                        _key[r][3] = _key[r-1][1] ^ _key[r  ][2];

                        r++; // r = 0 mod 3
                        _key[r][0] = _key[r-2][2] ^ RCons[i++] ^ _make_word(
                            FSBox[extract_byte<1>(_key[r-1][3])],
                            FSBox[extract_byte<2>(_key[r-1][3])],
                            FSBox[extract_byte<3>(_key[r-1][3])],
                            FSBox[extract_byte<0>(_key[r-1][3])]
                        );
                        _key[r][1] = _key[r-2][3] ^ _key[r][0];
                        _key[r][2] = _key[r-1][0] ^ _key[r][1];
                        _key[r][3] = _key[r-1][1] ^ _key[r][2];

                        // Break just after r == 12
                        if(r == _round_count)
                            break;

                        r++; // r = 1 mod 3
                        _key[r][0] = _key[r-2][2] ^ _key[r-1][3];
                        _key[r][1] = _key[r-2][3] ^ _key[r  ][0];
                    }
                    break;
                }
                case 32:
                {
                    // Load 256-bit key
                    _round_count = 14;
                    _key[0][0] = load_u32_le(key);
                    _key[0][1] = load_u32_le(key+4);
                    _key[0][2] = load_u32_le(key+8);
                    _key[0][3] = load_u32_le(key+12);
                    _key[1][0] = load_u32_le(key+16);
                    _key[1][1] = load_u32_le(key+20);
                    _key[1][2] = load_u32_le(key+24);
                    _key[1][3] = load_u32_le(key+28);
                    int i=0, r=2;
                    for(;;)
                    {
                        _key[r][0] = _key[r-2][0] ^ RCons[i++] ^ _make_word(
                            FSBox[extract_byte<1>(_key[r-1][3])],
                            FSBox[extract_byte<2>(_key[r-1][3])],
                            FSBox[extract_byte<3>(_key[r-1][3])],
                            FSBox[extract_byte<0>(_key[r-1][3])]
                        );
                        _key[r][1] = _key[r-2][1] ^ _key[r][0];
                        _key[r][2] = _key[r-2][2] ^ _key[r][1];
                        _key[r][3] = _key[r-2][3] ^ _key[r][2];

                        // Break just after r == 14
                        if(r == _round_count)
                            break;

                        r++; // r = 1 mod 2
                        _key[r][0] = _key[r-2][0] ^ _make_word(
                            FSBox[extract_byte<0>(_key[r-1][3])],
                            FSBox[extract_byte<1>(_key[r-1][3])],
                            FSBox[extract_byte<2>(_key[r-1][3])],
                            FSBox[extract_byte<3>(_key[r-1][3])]
                        );
                        _key[r][1] = _key[r-2][1] ^ _key[r][0];
                        _key[r][2] = _key[r-2][2] ^ _key[r][1];
                        _key[r][3] = _key[r-2][3] ^ _key[r][2];

                        r++; // r = 0 mod 2
                    }
                    break;
                }
                default:
                {
                    // Invalid key size
                    std::ostringstream oss;
                    oss << "ERROR: [" << __FILE__ << ":" << __LINE__ << "]: Invalid key size: " << size;
                    throw std::invalid_argument(oss.str());
                }
            }
        }

        inline static void do_fwd_round(
            std::array<uint32_t, 4>& astate, 
            const std::array<uint32_t, 4>& bstate,
            const std::array<uint32_t, 4>& rkey)
        {
            astate[0] = rkey[0]
                      ^ FTab0[extract_byte<0>(bstate[0])]
                      ^ FTab1[extract_byte<1>(bstate[1])]
                      ^ FTab2[extract_byte<2>(bstate[2])]
                      ^ FTab3[extract_byte<3>(bstate[3])];
            astate[1] = rkey[1]
                      ^ FTab0[extract_byte<0>(bstate[1])]
                      ^ FTab1[extract_byte<1>(bstate[2])]
                      ^ FTab2[extract_byte<2>(bstate[3])]
                      ^ FTab3[extract_byte<3>(bstate[0])];
            astate[2] = rkey[2]
                      ^ FTab0[extract_byte<0>(bstate[2])]
                      ^ FTab1[extract_byte<1>(bstate[3])]
                      ^ FTab2[extract_byte<2>(bstate[0])]
                      ^ FTab3[extract_byte<3>(bstate[1])];
            astate[3] = rkey[3]
                      ^ FTab0[extract_byte<0>(bstate[3])]
                      ^ FTab1[extract_byte<1>(bstate[0])]
                      ^ FTab2[extract_byte<2>(bstate[1])]
                      ^ FTab3[extract_byte<3>(bstate[2])];
        }

        inline static void do_aes_enc_transform(
            std::array<uint32_t, 4>& state,
            std::array<std::array<uint32_t, 4>, 15>& key,
            size_t round_count)
        {
            std::array<uint32_t, 4> tstate;
            state[0] ^= key[0][0];
            state[1] ^= key[0][1];
            state[2] ^= key[0][2];
            state[3] ^= key[0][3];
            int i;
            for(i = 0; i < (round_count-2); i+=2)
            {
                do_fwd_round(tstate, state, key[i+1]);
                do_fwd_round(state, tstate, key[i+2]);
            }
            do_fwd_round(tstate, state, key[i+1]);
            state[0] = key[i+2][0] ^ _make_word(
                FSBox[extract_byte<0>(tstate[0])],
                FSBox[extract_byte<1>(tstate[1])],
                FSBox[extract_byte<2>(tstate[2])],
                FSBox[extract_byte<3>(tstate[3])]
            );
            state[1] = key[i+2][1] ^ _make_word(
                FSBox[extract_byte<0>(tstate[1])],
                FSBox[extract_byte<1>(tstate[2])],
                FSBox[extract_byte<2>(tstate[3])],
                FSBox[extract_byte<3>(tstate[0])]
            );
            state[2] = key[i+2][2] ^ _make_word(
                FSBox[extract_byte<0>(tstate[2])],
                FSBox[extract_byte<1>(tstate[3])],
                FSBox[extract_byte<2>(tstate[0])],
                FSBox[extract_byte<3>(tstate[1])]
            );
            state[3] = key[i+2][3] ^ _make_word(
                FSBox[extract_byte<0>(tstate[3])],
                FSBox[extract_byte<1>(tstate[0])],
                FSBox[extract_byte<2>(tstate[1])],
                FSBox[extract_byte<3>(tstate[2])]
            );
        }

        void AESEngineGeneric::encrypt_ecb(const uint8_t* in, uint8_t* out, size_t block_count)
        {
            // nullptr on in or out is prohibited.
            if(!in)
            {
                std::ostringstream oss;
                oss << "ERROR: [" << __FILE__ << ":" << __LINE__ << "]: Argument `in` is nullptr.";
                throw std::invalid_argument(oss.str());
            }
            if(!out)
            {
                std::ostringstream oss;
                oss << "ERROR: [" << __FILE__ << ":" << __LINE__ << "]: Argument `out` is nullptr.";
                throw std::invalid_argument(oss.str());
            }
            
            std::array<uint32_t, 4> aes_state;

            for(int i=0; i<block_count; ++i)
            {
                aes_state[0] ^= load_u32_le(in);
                aes_state[1] ^= load_u32_le(in+4);
                aes_state[2] ^= load_u32_le(in+8);
                aes_state[3] ^= load_u32_le(in+12);
                in += 16;
                do_aes_enc_transform(aes_state, _key, _round_count);
                store_u32_le(out,    aes_state[0]);
                store_u32_le(out+4,  aes_state[1]);
                store_u32_le(out+8,  aes_state[2]);
                store_u32_le(out+12, aes_state[3]);
                out += 16;
            }
        }

        void AESEngineGeneric::encrypt_cbc(const uint8_t* in, uint8_t* out, size_t block_count, uint8_t* state)
        {
            // nullptr on in means input is all-0,
            // nullptr on out means output should be discarded,
            // nullptr on state is prohibited.
            if(!state)
            {
                std::ostringstream oss;
                oss << "ERROR: [" << __FILE__ << ":" << __LINE__ << "]: Argument `state` is nullptr.";
                throw std::invalid_argument(oss.str());
            }
            
            std::array<uint32_t, 4> cbc_state;
            cbc_state[0] = load_u32_le(state);
            cbc_state[1] = load_u32_le(state+4);
            cbc_state[2] = load_u32_le(state+8);
            cbc_state[3] = load_u32_le(state+12);

            for(int i=0; i<block_count; ++i)
            {
                if(in)
                {
                    cbc_state[0] ^= load_u32_le(in);
                    cbc_state[1] ^= load_u32_le(in+4);
                    cbc_state[2] ^= load_u32_le(in+8);
                    cbc_state[3] ^= load_u32_le(in+12);
                    in += 16;
                }
                do_aes_enc_transform(cbc_state, _key, _round_count);
                if(out)
                {
                    store_u32_le(out,    cbc_state[0]);
                    store_u32_le(out+4,  cbc_state[1]);
                    store_u32_le(out+8,  cbc_state[2]);
                    store_u32_le(out+12, cbc_state[3]);
                    out += 16;
                }
            }
            
            store_u32_le(state,    cbc_state[0]);
            store_u32_le(state+4,  cbc_state[1]);
            store_u32_le(state+8,  cbc_state[2]);
            store_u32_le(state+12, cbc_state[3]);
        }
    }
}