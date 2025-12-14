#include "../include/riffpe/Riffpe.hpp"

#include <array>
#include <iostream>
#include <random>
#include <vector>

#include "../src/perf.hpp"


template<typename Container>
void assert_equals(const Container& exp, const Container& act) {
    if(!std::equal(exp.cbegin(), exp.cend(), act.begin())) {
        std::cerr << "Error during warmup: ";
        for(auto it1 = exp.cbegin(), it2 = act.cbegin(); 
            it1 != exp.cend();
            ++it1, ++it2) {
            std::cerr << *it1 << " =?= " << *it2 <<", ";
        }
        std::cerr << std::endl;
        exit(1);
    }
}

int main(int argc, const char* argv[]) {
    int radix = 100;
    constexpr int digits = 8;

    std::array<uint8_t, 16> key = { 0x00, 0x11, 0x22, 0x33, 0x44, 0x55, 0x66, 0x77, 0x88, 0x99, 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF };

    auto fpe = riffpe::Riffpe(radix, digits, key.data(), key.size(), nullptr, 0, 16);

    auto warmup_ptx = std::vector<uint32_t> { 12, 34, 56, 78, 12, 34, 56, 78 };
    auto warmup_ctx = fpe.encrypt(warmup_ptx);
    auto warmup_out = fpe.decrypt(warmup_ctx);

    auto rng = std::mt19937_64();
    auto dist = std::uniform_int_distribution<uint32_t>(0, 99);
    
    constexpr size_t reps = 10'000;
    
    auto ptx = warmup_ptx;
    std::vector<uint64_t> tsev;
    for(size_t i=0; i<reps; ++i) {
        for(auto& digit : ptx) digit = dist(rng);
        tsev.push_back(ts());
        auto ctx = fpe.encrypt(ptx);
        tsev.push_back(ts());
        auto out = fpe.decrypt(ctx);
        tsev.push_back(ts());
    }

    uint64_t total_encrypt = 0;
    uint64_t total_decrypt = 0;
    
    for(auto it = tsev.begin(); it != tsev.end();) {
        auto t1 = *it++;
        auto t2 = *it++;
        auto t3 = *it++;
        total_encrypt += (t2-t1);
        total_decrypt += (t3-t2);
    }

    std::cout << "total_encrypt: " << total_encrypt << std::endl;
    std::cout << "total_decrypt: " << total_decrypt << std::endl;

    dist(rng);
}
