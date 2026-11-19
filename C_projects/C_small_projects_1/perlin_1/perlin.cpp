#include <fstream>
#include <cmath>
#include <iostream>
#include <array>
#include <numbers>
#include <vector>
#include "../../C_homebrew_libs/draw/draw.h"
#include "../../C_homebrew_libs/random/random.h"
#include "../../C_homebrew_libs/smooth/smooth.h"
#include "../../C_homebrew_libs/utils/grid.h"
#include "../../C_homebrew_libs/utils/utils.h"
#include "../../C_homebrew_libs/colour_gradients.h"

constexpr double inv_sqrt2 = std::numbers::sqrt2 / 2.0;

void drawVecs(Surface& screen, const std::vector<Vec2d>& grid, Vec2i gridSize, Vec2i cellSize, int vecLength) {
    for (int i = 0; i < grid.size(); i++) {    
        Vec2i vi = grid[i] * vecLength;
        Vec2i pos(Vec2iFromIndex(i, gridSize.x) * cellSize);
        screen.drawLine(pos, pos + vi, 0xf00000);
    }
}

struct Perlin {
    std::uint64_t seed;
    Vec2s cellSize;
    Vec2i offset;
    Grid<double> values;
    Grid<Vec2d> vectors;

    Perlin(
        std::uint64_t seed, 
        Vec2i surfaceSize, 
        Vec2s cellSize, 
        Vec2i offset={0, 0}, 
        double sharpness=1
    );

    void genGrid() {
        Random random(seed);
        vectors.setByIndex([&](size_t i) {
            return Vec2dFromAngle(random.randomAngle());
        });
    }

    void genData(double sharpness) {
        values.setByPos([&](Vec2s pos) {
            Vec2i gridPos = pos / cellSize;
            Vec2d localFrac = Vec2d(pos % cellSize) / Vec2d(cellSize);
            size_t index = 0;
            std::array<double, 4> vals;
            for (const Vec2i& j : {Vec2i(0, 0), Vec2i(0, 1), Vec2i(1, 0), Vec2i(1, 1)}) {
                Vec2d v = vectors.at(gridPos + j);
                Vec2d d = localFrac - Vec2d(j);
                vals[index] = v.dot(d);
                index++;
            }
            //smoother step is more bulbous
            double L = smootherStep(vals[0], vals[1], localFrac.y);
            double R = smootherStep(vals[2], vals[3], localFrac.y);
            double o = smootherStep(L, R, localFrac.x);
            o = smoothCap(o, inv_sqrt2, 100) / inv_sqrt2;
            o = easeOut(o, sharpness);
            o = o * 0.5 + 0.5;
            return o;
        });
    }

    void draw(Surface& screen, Vec2i pos = {0, 0}) {
        screen.setByIndex([&] (size_t i) {
            std::uint8_t c = values.at(i) * 255;
            return Colour(c);
        });
    }
};

/// returns a grid of doubles from 0 to 1
Perlin::Perlin(
    std::uint64_t seed, 
    Vec2i surfaceSize,
    Vec2s cellSize,
    // NEEDS TO BE ADDED
    Vec2i offset, 
    double sharpness
) : seed(seed),
    cellSize(cellSize),
    offset(offset) {
    // no idea why below maybe think on it
    Vec2s gridSize((surfaceSize + cellSize - Vec2i(1)) / cellSize + Vec2i(1));
    vectors = Grid<Vec2d>(gridSize);
    values = Grid<double>(surfaceSize);
    
    genGrid();
    genData(sharpness);
}

int main() {
    // for me
    const bool drawGrid = false;
    const bool drawVectors = false;
    const Vec2i cellSize(32, 32);
    const int screen_height = 512, screen_width = 512;
    
    // init env
    Random random(2);
    Surface screen(Vec2i(screen_width, screen_height));
    Grid<double> noiseMatrix(screen.dim);

    Perlin perlin1(random.random<int>(), screen.dim, Vec2s(128, 128), {0, 0}, 2);
    Perlin perlin2(random.random<int>(), screen.dim, Vec2s(64, 64), {0, 0}, 2);
    Perlin perlin3(random.random<int>(), screen.dim, Vec2s(32, 32), {0, 0}, 2);
    Perlin perlin4(random.random<int>(), screen.dim, Vec2s(16, 16), {0, 0}, 2);
    Perlin perlin5(random.random<int>(), screen.dim, Vec2s(8, 8), {0, 0}, 2);
    Perlin perlin6(random.random<int>(), screen.dim, Vec2s(4, 4), {0, 0}, 2);
    Perlin perlin7(random.random<int>(), screen.dim, Vec2s(2, 2), {0, 0}, 2);

    // TO DO FIX FOR GRID/DRAW INTERACTIONS
    noiseMatrix.setByIndex([&](size_t i) {
        return (
            perlin1.values.at(i) / 2 +
            perlin2.values.at(i) / 4 +
            perlin3.values.at(i) / 8 +
            perlin4.values.at(i) / 16 +
            perlin5.values.at(i) / 32 +
            perlin6.values.at(i) / 64 +
            perlin7.values.at(i) / 64
        );
    });

    auto gradient = gradients::islands_32; 

    screen.setByIndex([&](size_t i) {
        double x = noiseMatrix.at(i);

        // space for eases
        x = easeOutIn(x, 1.5);
        x = easeIn(x, 0.4);

        size_t xi = static_cast<size_t>(x * gradient.size());
        //return Colour(255 * x, 255 * x, 255 * x);
        return gradient.at(xi);
    });

    // TO DO FIX FOR GRID/DRAW INTERACTIONS
    if (drawGrid)
        screen.drawGrid(perlin1.vectors.dim, Vec2i(perlin1.cellSize), 0x404040);

    // TO DO FIX FOR GRID/DRAW INTERACTIONS
    const int vecLength = 15;
    if (drawVectors)
        drawVecs(screen, perlin1.vectors.data, perlin1.vectors.dim, perlin1.cellSize, vecLength);

  

    //Write PPM (binary, P6)
    std::ofstream out("output.ppm", std::ios::binary);
    out << "P6\n" << screen.dim.x << " " << screen.dim.y << "\n255\n";
    out.write(reinterpret_cast<const char*>(screen.data.data()), screen.data.size() * sizeof(Pixel));
}