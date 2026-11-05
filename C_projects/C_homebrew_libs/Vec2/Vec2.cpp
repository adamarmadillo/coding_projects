#include "Vec2.h"

Vec2d Vec2dFromAngle(double r) { return {std::cos(r), std::sin(r)}; }
Vec2d Vec2dFromPolar(double r, double m) { return {std::cos(r) * m, std::sin(r) * m}; }
Vec2i Vec2iFromIndex(int i, int x) { return {i % x, i / x}; }