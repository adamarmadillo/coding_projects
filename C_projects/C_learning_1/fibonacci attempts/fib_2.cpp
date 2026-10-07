#include <iostream>

// ATTEMPT 2
// retarded recursion attempt (very little thought)

// insanely inefficient
long long fib(int n) {
        if (n == 0 || n == 1) {return n;}
        return fib(n - 1) + fib(n - 2);
    }

int main() {
    std::cout << "What fibonacci number would you like to calculate: \n";
    int val;
    std::cin >> val;

    // clamping the value at 91 because I don't know how to make
    // infinitely large numbers
    if (val > 92) {
        val = 92;
    }

    // WARNING!! WARNING!! fib() IS O(1.6 ^ n), RUNNING n > 50 WILL TAKE MINUTES TO CENTURIES!!!
    std::cout << "fib num " << val << ": " << fib(val) << "\n";

    return 0;
}