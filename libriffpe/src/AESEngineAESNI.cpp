#include "AESEngineAESNI.hpp"

#include <stdexcept>
#include <sstream>

#include "x86_utils.hpp"

namespace riffpe
{
    namespace crypto
    {
        namespace
        {
            /* This variant of keyExpansion is used by AES_128, AES_256 */
            template<uint8_t rcon, uint8_t shuf>
            static inline __m128i key_expansion_assist_a(__m128i v1, __m128i v3)
            {
                __m128i v2, v4;
                v2 = _mm_aeskeygenassist_si128 (v3, rcon);
                v2 = _mm_shuffle_epi32(v2, shuf);
                v4 = _mm_slli_si128 (v1, 0x4);
                v1 = _mm_xor_si128 (v1, v4);
                v4 = _mm_slli_si128 (v4, 0x4);
                v1 = _mm_xor_si128 (v1, v4);
                v4 = _mm_slli_si128 (v4, 0x4);
                v1 = _mm_xor_si128 (v1, v4);
                v1 = _mm_xor_si128 (v1, v2);
                return v1;
            }

            /* This variant of keyExpansion is used by AES_192 */
            template<uint8_t rcon>
            static inline void key_expansion_assist_b(__m128i &v1, __m128i &v3)
            {
                __m128i v2, v4;
                v2 =_mm_aeskeygenassist_si128 (v3, rcon);
                v2 = _mm_shuffle_epi32 (v2, 0x55);
                v4 = _mm_slli_si128 (v1, 0x4);
                v1 = _mm_xor_si128 (v1, v4);
                v4 = _mm_slli_si128 (v4, 0x4);
                v1 = _mm_xor_si128 (v1, v4);
                v4 = _mm_slli_si128 (v4, 0x4);
                v1 = _mm_xor_si128 (v1, v4);
                v1 = _mm_xor_si128 (v1, v2);
                v2 = _mm_shuffle_epi32(v1, 0xff);
                v4 = _mm_slli_si128 (v3, 0x4);
                v3 = _mm_xor_si128 (v3, v4);
                v3 = _mm_xor_si128 (v3, v2);
            }

            template<size_t round_count>
            inline static void do_aes_enc_transform(
                __m128i& state,
                const __m128i* key
            ) {
                state = _mm_xor_si128(state, *key++);
                if constexpr (round_count == 14) {
                    state = _mm_aesenc_si128(state, *key++);
                    state = _mm_aesenc_si128(state, *key++);
                }
                if constexpr (round_count >= 12) {
                    state = _mm_aesenc_si128(state, *key++);
                    state = _mm_aesenc_si128(state, *key++);
                }
                state = _mm_aesenc_si128(state, *key++);
                state = _mm_aesenc_si128(state, *key++);
                state = _mm_aesenc_si128(state, *key++);
                state = _mm_aesenc_si128(state, *key++);
                state = _mm_aesenc_si128(state, *key++);
                state = _mm_aesenc_si128(state, *key++);
                state = _mm_aesenc_si128(state, *key++);
                state = _mm_aesenc_si128(state, *key++);
                state = _mm_aesenc_si128(state, *key++);
                state = _mm_aesenclast_si128(state, *key);
            }
        
            template<size_t round_count>
            inline static void encrypt_ecb_loop(
                const uint8_t* in, uint8_t* out, size_t block_count, const __m128i* key_begin
            ) {
                __m128i aes_state;
                for(int i=0; i<block_count; ++i)
                {
                    aes_state = loadu_mm128i(in);
                    in += 16;
                    do_aes_enc_transform<round_count>(aes_state, key_begin);
                    storeu_mm128i(out, aes_state);
                    out += 16;
                }
            }

            template<size_t round_count>
            inline static void encrypt_cbc_loop(
                const uint8_t* in, uint8_t* out, size_t block_count, const __m128i* key_begin, uint8_t* state
            ) { 
                __m128i cbc_state = loadu_mm128i(state);
                for(int i=0; i<block_count; ++i) {
                    if(in) {
                        cbc_state = _mm_xor_si128(cbc_state, loadu_mm128i(in));
                        in += 16;
                    }
                    do_aes_enc_transform<round_count>(cbc_state, key_begin);
                    if(out) {
                        storeu_mm128i(out, cbc_state);
                        out += 16;
                    }
                }
                storeu_mm128i(state, cbc_state);
            }
        }

        void AESEngineAESNI::set_key(const uint8_t *key, size_t size)
        {
            switch(size)
            {
                case 16:
                {
                    // Load 128-bit key
                    _round_count = 10;
                    std::array<__m128i, 11> _tmp_key;
                    _tmp_key[0] = loadu_mm128i(key);
                    _tmp_key[1] = key_expansion_assist_a<0x01, 0xff>(_tmp_key[0], _tmp_key[0]);
                    _tmp_key[2] = key_expansion_assist_a<0x02, 0xff>(_tmp_key[1], _tmp_key[1]);
                    _tmp_key[3] = key_expansion_assist_a<0x04, 0xff>(_tmp_key[2], _tmp_key[2]);
                    _tmp_key[4] = key_expansion_assist_a<0x08, 0xff>(_tmp_key[3], _tmp_key[3]);
                    _tmp_key[5] = key_expansion_assist_a<0x10, 0xff>(_tmp_key[4], _tmp_key[4]);
                    _tmp_key[6] = key_expansion_assist_a<0x20, 0xff>(_tmp_key[5], _tmp_key[5]);
                    _tmp_key[7] = key_expansion_assist_a<0x40, 0xff>(_tmp_key[6], _tmp_key[6]);
                    _tmp_key[8] = key_expansion_assist_a<0x80, 0xff>(_tmp_key[7], _tmp_key[7]);
                    _tmp_key[9] = key_expansion_assist_a<0x1b, 0xff>(_tmp_key[8], _tmp_key[8]);
                    _tmp_key[10] = key_expansion_assist_a<0x36, 0xff>(_tmp_key[9], _tmp_key[9]);
                    #pragma unroll
                    for(int i=0; i<_tmp_key.size(); ++i)
                        _key[i] = _tmp_key[i];
                    break;
                }
                case 24:
                {
                    // Load 192-bit key
                    _round_count = 12;
                    std::array<__m128i, 13> _tmp_key;
                    __m128i temp1 = loadu_mm128i(key);
                    __m128i temp3 = loadu_mm64i(key+16);

                    #define SHUFFLE_HELPER_A(x) _mm_castpd_si128(_mm_shuffle_pd(_mm_castsi128_pd(_tmp_key[x]), _mm_castsi128_pd(temp1),0))
                    #define SHUFFLE_HELPER_B()  _mm_castpd_si128(_mm_shuffle_pd(_mm_castsi128_pd(temp1), _mm_castsi128_pd(temp3),1))
                    _tmp_key[0]=temp1;
                    _tmp_key[1]=temp3;
                    key_expansion_assist_b<0x01>(temp1, temp3);
                    _tmp_key[1] = SHUFFLE_HELPER_A(1);
                    _tmp_key[2] = SHUFFLE_HELPER_B();
                    key_expansion_assist_b<0x02>(temp1, temp3);
                    _tmp_key[3]=temp1;
                    _tmp_key[4]=temp3;
                    key_expansion_assist_b<0x04>(temp1, temp3);
                    _tmp_key[4] = SHUFFLE_HELPER_A(4);
                    _tmp_key[5] = SHUFFLE_HELPER_B();
                    key_expansion_assist_b<0x08>(temp1, temp3);
                    _tmp_key[6]=temp1;
                    _tmp_key[7]=temp3;
                    key_expansion_assist_b<0x10>(temp1, temp3);
                    _tmp_key[7] = SHUFFLE_HELPER_A(7);
                    _tmp_key[8] = SHUFFLE_HELPER_B();
                    key_expansion_assist_b<0x20>(temp1, temp3);
                    _tmp_key[9]=temp1;
                    _tmp_key[10]=temp3;
                    key_expansion_assist_b<0x40>(temp1, temp3);
                    _tmp_key[10] = SHUFFLE_HELPER_A(10);
                    _tmp_key[11] = SHUFFLE_HELPER_B();
                    key_expansion_assist_b<0x80>(temp1, temp3);
                    _tmp_key[12]=temp1;
                    #undef SHUFFLE_HELPER_A
                    #undef SHUFFLE_HELPER_B
                    #pragma unroll
                    for(int i=0; i<_tmp_key.size(); ++i)
                        _key[i] = _tmp_key[i];
                    break;
                }
                case 32:
                {
                    // Load 256-bit key
                    _round_count = 14;
                    std::array<__m128i, 15> _tmp_key;
                    _tmp_key[0] = loadu_mm128i(key);
                    _tmp_key[1] = loadu_mm128i(key+16);
                    _tmp_key[2] = key_expansion_assist_a<0x01, 0xff>(_tmp_key[0], _tmp_key[1]);
                    _tmp_key[3] = key_expansion_assist_a<0x00, 0xaa>(_tmp_key[1], _tmp_key[2]);
                    _tmp_key[4] = key_expansion_assist_a<0x02, 0xff>(_tmp_key[2], _tmp_key[3]);
                    _tmp_key[5] = key_expansion_assist_a<0x00, 0xaa>(_tmp_key[3], _tmp_key[4]);
                    _tmp_key[6] = key_expansion_assist_a<0x04, 0xff>(_tmp_key[4], _tmp_key[5]);
                    _tmp_key[7] = key_expansion_assist_a<0x00, 0xaa>(_tmp_key[5], _tmp_key[6]);
                    _tmp_key[8] = key_expansion_assist_a<0x08, 0xff>(_tmp_key[6], _tmp_key[7]);
                    _tmp_key[9] = key_expansion_assist_a<0x00, 0xaa>(_tmp_key[7], _tmp_key[8]);
                    _tmp_key[10] = key_expansion_assist_a<0x10, 0xff>(_tmp_key[8], _tmp_key[9]);
                    _tmp_key[11] = key_expansion_assist_a<0x00, 0xaa>(_tmp_key[9], _tmp_key[10]);
                    _tmp_key[12] = key_expansion_assist_a<0x20, 0xff>(_tmp_key[10], _tmp_key[11]);
                    _tmp_key[13] = key_expansion_assist_a<0x00, 0xaa>(_tmp_key[11], _tmp_key[12]);
                    _tmp_key[14] = key_expansion_assist_a<0x40, 0xff>(_tmp_key[12], _tmp_key[13]);
                    for(int i=0; i<_tmp_key.size(); ++i)
                        _key[i] = _tmp_key[i];
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

        void AESEngineAESNI::encrypt_ecb(const uint8_t* in, uint8_t* out, size_t block_count)
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
            
            switch(_round_count) {
                case 10: return encrypt_ecb_loop<10>(in, out, block_count, _key.data());
                case 12: return encrypt_ecb_loop<12>(in, out, block_count, _key.data());
                case 14: return encrypt_ecb_loop<14>(in, out, block_count, _key.data());
                default: /* unreachable */ return;
            }
        }

        void AESEngineAESNI::encrypt_cbc(const uint8_t* in, uint8_t* out, size_t block_count, uint8_t* state)
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
            
            switch(_round_count) {
                case 10: return encrypt_cbc_loop<10>(in, out, block_count, _key.data(), state);
                case 12: return encrypt_cbc_loop<12>(in, out, block_count, _key.data(), state);
                case 14: return encrypt_cbc_loop<14>(in, out, block_count, _key.data(), state);
                default: /* unreachable */ return;
            }

        }
    }
}
