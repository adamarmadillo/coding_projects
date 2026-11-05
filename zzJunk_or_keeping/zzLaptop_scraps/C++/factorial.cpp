#include <iostream>
// waddeva
long long x;

long long factorial(long long x) {
    if (x == 1) {return 1;}
    return x * factorial(x - 1);
}

int n = 1;

int main() {
    while (n == 1) {
        std::cin >> x;
        if (x == 0) {
            n = 1;
        }
        std::cout << factorial(x) << "\n";
    }
}