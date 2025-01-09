#include <riffpe/AESEngine.hpp>

#include <cstdio>
#include <cstring>

int main()
{
    using aes_engine_type = riffpe::crypto::AESEngine;
    aes_engine_type* aes_engine = aes_engine_type::engine_factory();

    uint8_t test_key[] = { 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f };
    uint8_t test_ptx[] = { 0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xaa, 0xbb, 0xcc, 0xdd, 0xee, 0xff };
    uint8_t test_ctx[] = { 0x69, 0xc4, 0xe0, 0xd8, 0x6a, 0x7b, 0x04, 0x30, 0xd8, 0xcd, 0xb7, 0x80, 0x70, 0xb4, 0xc5, 0x5a };
    uint8_t out[16];
    
    printf("Engine: %s\n", aes_engine->engine_id());
    aes_engine->set_key(test_key, 16);
    aes_engine->encrypt_ecb(test_ptx, out, 1);
    if(memcmp(out, test_ctx, 16) != 0)
    {
        printf("Invalid encryption result in test 1:\n");
        printf("%02x%02x%02x%02x %02x%02x%02x%02x %02x%02x%02x%02x %02x%02x%02x%02x\n",
               out[0],  out[1],  out[2],  out[3],
               out[4],  out[5],  out[6],  out[7],
               out[8],  out[9],  out[10], out[11],
               out[12], out[13], out[14], out[15]);
        return 1;
    }

    delete aes_engine;
}
