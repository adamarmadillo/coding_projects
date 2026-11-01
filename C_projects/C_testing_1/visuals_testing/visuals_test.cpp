#include <fstream>
#include <vector>
#include <cstdint>
#include "random.h"
#include <cmath>
#include <iostream>

struct Pixel { uint8_t r, g, b; };
struct Vec2 { double x, y; };
double pi = 3.14159265358979323846;
Random R(2);

Vec2 dir(double angle) {
    double r = angle * pi * 2;
    return Vec2(std::cos(r), std::sin(r));
};

Vec2 randomDir() {
    return dir(R.randomDouble());
};

int main() {
    const int screenWidth = 256, screenHeight = 256;
    std::vector<Pixel> image(screenWidth * screenHeight);

    const int gridWidth = 8, gridHeight = 8;
    std::vector<Vec2> vectorGrid((gridWidth + 1) * (gridHeight + 1));
    for (int i = 0; i < (gridWidth + 1) * (gridHeight + 1); i++) {
        vectorGrid.at(i) = randomDir();
    }

    // Set pixel colours: here, a simple gradient
    for (int y = 0; y < screenHeight; ++y)
        for (int x = 0; x < screenWidth; ++x) {
            int cellX = x * gridWidth / screenWidth;
            int cellY = y * gridHeight / screenHeight;
            
            int xval = static_cast<int>(vectorGrid.at(cellY * (gridWidth + 1) + cellX).x * 255);
            int yval = static_cast<int>(vectorGrid.at(cellY * (gridWidth + 1) + cellX).y * 255);
            image[y * screenWidth + x] = { (uint8_t)x, (uint8_t)y, (uint8_t)xval };
        }

    // Write PPM (binary, P6)
    std::ofstream out("output.ppm", std::ios::binary);
    out << "P6\n" << screenWidth << " " << screenHeight << "\n255\n";
    out.write(reinterpret_cast<const char*>(image.data()), image.size() * sizeof(Pixel));

    std::cout << vectorGrid.at(2).x;
}
