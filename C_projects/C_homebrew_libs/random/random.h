#pragma once
#include <cstdint>
#include <numbers>
#include <vector>
#include <concepts>

std::uint64_t splitMix64(std::uint64_t x);   // declaration only, defined in random.cpp

struct Random {
    std::uint64_t seed;
    std::uint64_t state = splitMix64(seed);
    std::uint64_t step = 0;

    explicit Random(std::uint64_t s);

    std::uint64_t next();
    std::uint64_t back();

    template<typename T> requires (!std::is_same_v<T, bool> && !std::is_same_v<T, double>) 
    T random() {
        return static_cast<T>(next());
    };

    template<typename T> requires (std::is_same_v<T, double>) 
    T random() {
        std::uint64_t x = next() >> 11;
        return static_cast<double>(x) * 0x1.0p-53;
    };

    template<typename T> requires (std::is_same_v<T, bool>) 
    T random() {
        return (next() >> 63) & 1;
    };

    double randomAngle() {
        return random<double>() * std::numbers::pi * (random<bool>() ? 1 : -1);
    };

    template<typename T>
    void shuffle(std::vector<T>& v) {
        for (size_t i = v.size(); i > 1; i--) {
            size_t j = random<size_t>() % i;
            std::swap(v[i - 1], v[j]);
        }
    };
};
