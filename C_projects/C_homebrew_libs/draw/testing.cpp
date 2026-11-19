#include <fstream>
#include <cmath>
#include <iostream>
#include "draw.h"
#include "../smooth/smooth.h"
#include <vector>
#include "../random/random.h"
#include "../colour_gradients.h"

double sm(double x) {
    double o = x;
    o = inOutPlateau(o, 0.2, 4);
    //o = easeIn(o, 1.1);
    return o;
}

int main() {
    Surface screen(Vec2i(256, 256));
    Random random(1);

    screen.setByPos([&] (Vec2i p) {
        return Colour(p.x, p.y, (p.x + p.y) / 2);
    });

    // Write PPM (binary, P6)
    std::ofstream out("output.ppm", std::ios::binary);
    out << "P6\n" << screen.dim.x << " " << screen.dim.y << "\n255\n";
    out.write(reinterpret_cast<const char*>(screen.data.data()), screen.size() * sizeof(Pixel));
}