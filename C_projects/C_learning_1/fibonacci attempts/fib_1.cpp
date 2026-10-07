#include <iostream>

// ATTEMPT 1
// naive int addition

int main() {
    std::cout << "What fibonacci number would you like to calculate: \n";
    int val;
    std::cin >> val;
    // clamping the value at 91 because I don't know how to make
    // infinitely large numbers
    if (val > 91) {
        val = 91;
    }
    long long a = 0, b = 1, z;
    for (int i = 1; i <= val; i++) {
        z = a + b;
        a = b;
        b = z;
        if (i == val) {
            std::cout << "fib num " << i << ": " << a << "\n";
        }
    }
    return 0;
}