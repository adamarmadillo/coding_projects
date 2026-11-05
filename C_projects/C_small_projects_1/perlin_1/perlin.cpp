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

    double valueAt(Vec2i pos) { return values.at(pos); }
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
    const Vec2i cellSize(16, 32);
    const int screen_height = 1024, screen_width = 1024;

    
    // init env
    Random random(2);
    Surface screen(Vec2i(screen_width, screen_height));
    Grid<double> noiseMatrix(screen.dim);

    Perlin perlin1(1, screen.dim, Vec2s(90, 90), {0, 0}, 0);
    Perlin perlin2(2, screen.dim, Vec2s(53, 53), {0, 0}, 1);
    Perlin perlin3(3, screen.dim, Vec2s(18, 18), {0, 0}, 1);
    Perlin perlin4(4, screen.dim, Vec2s(15, 15), {0, 0}, 2);
    Perlin perlin5(5, screen.dim, Vec2s(8, 8), {0, 0}, 4);
    Perlin perlin6(6, screen.dim, Vec2s(7, 7), {0, 0}, 4);
    Perlin perlin7(7, screen.dim, Vec2s(5, 5), {0, 0}, 2);

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

    std::vector<Colour> pallete{
0x0a2a5e, 0x0a2c62, 0x0b2e66, 0x0b306a, 0x0c326e, 0x0c3472, 0x0d3676, 0x0d387a,
0x0e3a7e, 0x0e3c82, 0x0f3e86, 0x0f408a, 0x10428e, 0x104492, 0x114696, 0x12489a,
0x144c9e, 0x1a5aa8, 0x3a7cbc, 0x7ab0d6, 0xbcd8ea, 0xe4f0f8, 0xf6fafd, 0xffffff,
0xffffff, 0xffffff, 0xffffff, 0xffffff, 0xffffff, 0xffffff, 0xffffff, 0xffffff,
};

    screen.setByIndex([&](size_t i) {
        return pallete.at(static_cast<size_t>(noiseMatrix.at(i) * 32 * 1));
    });

    //screen.setByIndex([&](size_t i) {
    //    uint8_t c = noiseMatrix.at(i) * 256;
    //    return Colour(c, c, c).q(0x501040);
    //});

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