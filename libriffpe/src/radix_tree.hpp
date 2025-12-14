#pragma once
/**
 * An optimized version of radix tree for storing RifflePerm elements
 */

#include <algorithm>
#include <array>
#include <stdexcept>
#include <vector>
#include <string_view>

#include <cstdint>

using bytes_view = std::basic_string_view<uint8_t>;

template<
    typename ElType,
    typename KeyType,
    size_t BucketCount = (sizeof(ElType) == 1) ? 16 : 256
>
class radix_tree {
public:
    using key_type = KeyType;
    using element_type = std::tuple<bytes_view, ElType>;

protected:
    constexpr static size_t bucket_count = BucketCount;
    constexpr static size_t bkey_div = (1 << (sizeof(typename key_type::value_type) * 8)) / bucket_count;
    std::array<std::vector<element_type>, bucket_count> _buckets;
    // bucket_count must be a power of 2
    static_assert(!(bucket_count & (bucket_count-1)));

public:
    radix_tree() = default;

    void insert(bytes_view key, ElType element) {
        uint8_t bkey = key[0];
        bkey /= bkey_div;
        _buckets[bkey].emplace_back(key, element);
    }

    void clear() {
        for(auto& bucket: _buckets) {
            bucket.clear();
        }
    }

    ElType nth_element(ElType index) {
        size_t cum = 0, ncum;
        for(auto& bucket : _buckets) {
            ncum = cum + bucket.size();
            if(index < ncum) {
                // The result is in this bucket
                auto b = bucket.begin(), e = bucket.end(), n = b + (index - cum);
                std::nth_element(b, n, e);
                return std::get<1>(*n);
            }
            cum = ncum;
        }
        throw std::out_of_range("nth_element out of radix_tree");
    }

    size_t size() const {
        size_t cum = 0;
        for(const auto& bucket : _buckets) {
            cum += bucket.size();
        }
        return cum;
    }
};
