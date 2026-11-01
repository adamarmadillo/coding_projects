#pragma once
#include <cstdint>

std::uint64_t splitMix64(std::uint64_t x);   // declaration only, defined in random.cpp

struct Random {
    std::uint64_t seed;
    std::uint64_t state = splitMix64(seed);
    std::uint64_t step = 0;

    explicit Random(std::uint64_t s);

    std::uint64_t next();
    std::uint64_t back();
    std::uint8_t randomInt8();
    std::uint16_t randomInt16();
    std::uint32_t randomInt32();
    std::uint64_t randomInt64();
    bool randomBool();
    double randomDouble();
};