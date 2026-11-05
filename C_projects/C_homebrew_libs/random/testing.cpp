#include "random.h"
#include <iostream>

Random Rand(2);

int main() {
    for (int i = 0; i < 20; i++) {
        std::cout << Rand.randomDouble() << "\n";
    }
}