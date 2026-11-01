// random.cpp
#include "random.h"

std::uint64_t splitMix64(std::uint64_t x) {
    x += 0x9E3779B97F4A7C15ULL;
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ULL;
    x = (x ^ (x >> 27)) * 0x94D049BB133111EBULL;
    return x ^ (x >> 31);
}

Random::Random(std::uint64_t s) : seed(s) {}

std::uint64_t Random::next() {
    step += 1;
    state += 0x9E3779B97F4A7C15ULL;
    std::uint64_t x = state;
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9ULL;
    x = (x ^ (x >> 27)) * 0x94D049BB133111EBULL;
    return x ^ (x >> 31);
}

std::uint8_t Random::randomInt8() {
    return static_cast<std::uint8_t>(next());
}

std::uint16_t Random::randomInt16() {
    return static_cast<std::uint16_t>(next());
}

std::uint32_t Random::randomInt32() {
    return static_cast<std::uint32_t>(next());
}

std::uint64_t Random::randomInt64() {
    return next();
}

bool Random::randomBool() {
    return (next() >> 63) & 1;
}

double Random::randomDouble() {
    std::uint64_t x = next() >> 11;
    return static_cast<double>(x) * 0x1.0p-53;
}