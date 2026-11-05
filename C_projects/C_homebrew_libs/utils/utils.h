#pragma once
#include <stdexcept>
#include <vector>

/// @brief returns sign of x, or 0 if x = 0
inline int sign(double x) { return (x > 0) - (x < 0); };
/// @brief returns sign of x, or 0 if x = 0
inline int sign(int x) { return (x > 0) - (x < 0); };

/// @brief quantise x down to multiple of a step size
inline int quantise(int x, int step) { return step ? (x / step * step) : x; }