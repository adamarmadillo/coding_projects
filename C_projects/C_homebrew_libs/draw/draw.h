#pragma once
#include "../Vec2/Vec2.h"
#include "../utils/utils.h"
#include "../utils/grid.h"
#include <vector>
#include <cstdint>
#include <string>
#include <stdexcept>
#include <concepts>
#include <fstream> // DO THIS

struct Colour {
    std::uint8_t r, g, b;
    
    template<typename T> requires (!std::is_same_v<uint8_t, T>)
    constexpr Colour(T r, T g, T b) : r(static_cast<uint8_t>(r)), g(static_cast<uint8_t>(g)), b(static_cast<uint8_t>(b)) {};
    constexpr Colour(uint8_t r, uint8_t g, uint8_t b) : r(r), g(g), b(b) {};
    constexpr Colour(uint32_t rgb) : r(rgb >> 16 & 0xFF), g(rgb >> 8 & 0xFF), b(rgb & 0xFF) {};
    constexpr explicit Colour() : r(), g(), b() {};
    
    Colour& q(Colour);
};

struct Pixel {
    std::uint8_t r{}, g{}, b{};
    
    constexpr explicit Pixel() = default;
    constexpr explicit Pixel(uint8_t r, uint8_t g, uint8_t b) : r(r), g(g), b(b) {}
    constexpr Pixel(Colour c) : r(c.r), g(c.g), b(c.b) {}
};

struct Surface : Grid<Pixel> {
    using Grid<Pixel>::Grid;

    void setAt(Vec2i pos, Pixel p, bool strictBounds=false);
    void setAt(size_t i, Pixel p, bool strictBounds=false);
    void drawRect(Recti rect, Colour colour, bool strictBounds = false);
    void drawRect(Recti rect, uint32_t colour, bool strictBounds = false);
    void drawLine(Vec2i pointA, Vec2i pointB, Colour c, bool strictBounds = false);
    void drawLine(Vec2i pointA, Vec2i pointB, uint32_t c, bool strictBounds = false);
    void drawGrid(Vec2i gridSize, Vec2i cellSize, Colour c, Vec2i cornerPos = {0, 0}, bool strictBounds = false);

    private :
    void plotLineHigh(Vec2i a, Vec2i b, Colour c, bool strictBounds);
    void plotLineLow(Vec2i a, Vec2i b, Colour c, bool strictBounds);
};