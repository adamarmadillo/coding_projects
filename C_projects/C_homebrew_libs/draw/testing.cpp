#include <fstream>
#include <cmath>
#include <iostream>
#include "draw.h"
#include "../smooth/smooth.h"
#include <vector>
#include "../random/random.h"

int main() {
    Surface screen(Vec2i(512, 256));

    Grid<Colour> quads(Vec2i(32, 16));  // 512 cells
    quads.setByIndex([&](size_t i) {
        int r = (i % 8) * 32 + 16;
        int g = ((i / 8) % 8) * 32 + 16;
        int b = (i / 64) * 32 + 16;
        return Colour(r, g, b);
    });

    Random rand(1);
    rand.shuffle(quads.data);

    screen.setByPos([&](Vec2i pos) {
        return quads.at(pos / 16);
    });

    //screen.setByPos([&](Vec2i pos) {
    //    Colour c;
    //    c.r = quantise(pos.x * 2, 32);
    //    c.g = quantise(pos.y * 2, 32);
    //    c.b = quantise(pos.x / 4, 32) / 2 + quantise(pos.y / 4, 32) * 2;
    //    return c;
    //});

    // Write PPM (binary, P6)
    std::ofstream out("output.ppm", std::ios::binary);
    out << "P6\n" << screen.dim.x << " " << screen.dim.y << "\n255\n";
    out.write(reinterpret_cast<const char*>(screen.data.data()), screen.size() * sizeof(Pixel));
}