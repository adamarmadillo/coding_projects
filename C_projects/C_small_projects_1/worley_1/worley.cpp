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



int main() {
    // for me
    const bool drawGrid = false;
    const bool drawVectors = false;
    const Vec2i cellSize(16, 32);
    const int screen_height = 512, screen_width = 512;

    // init env
    Random random(4);
    Surface screen(Vec2i(screen_width, screen_height));
    Grid<double> noiseMatrix(screen.dim);

    const int nPoints = 100;
    std::vector<Vec2i> points;
    for (int i = 0; i < nPoints; i++) {
        points.push_back({Vec2d(random.random<double>(), random.random<double>()) * screen.dim});
    }


    const double maxDist = 64;
    noiseMatrix.setByPos([&](Vec2i p) {
        double d = maxDist;
        double s = maxDist;
        for (Vec2i v : points) {
            double d0 = (v - p).magnitude();
            if (d0 < d) { s = d; d = d0; }
        }
        return (d != maxDist) ? 1-0.9 * d / maxDist : 0;
    });

    //screen.setByIndex([&](size_t i) {
    //    uint8_t c = 255 - std::min(8 * noiseMatrix.at(i), 255.0);
    //    return Colour(c, c, c);
    //});

    screen.setByIndex([&](size_t i) {
        double c = noiseMatrix.at(i);
        c = easeOut(c, 1.1);
        return Colour{c * 255, c * 255, c * 255};
    });

    //Write PPM (binary, P6)
    std::ofstream out("output.ppm", std::ios::binary);
    out << "P6\n" << screen.dim.x << " " << screen.dim.y << "\n255\n";
    out.write(reinterpret_cast<const char*>(screen.data.data()), screen.data.size() * sizeof(Pixel));
}