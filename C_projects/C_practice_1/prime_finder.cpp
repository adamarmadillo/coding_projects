#include <iostream>

// initialise

int inputNum;

bool checkPrime(unsigned int n) {
    auto i = 2u;
    bool isPrime = true;
    bool sqrtReached = false;
    while (isPrime && !sqrtReached) {
        if (n % i == 0) {
            isPrime = false;
        } else if (n / i <= i) {
            sqrtReached = true;
        }
        i++;
    }
    return isPrime;
}

// start at 1
// increase the number by 1
// test if it can be divided by 2 up to the sqrt of the prime
// square root can be tested if the number divide by the test is less than the test itself
unsigned int calculatePrime(unsigned int input) {
    auto n = 2u;
    for (int primeIndex = 1; primeIndex < input; primeIndex++) {
        bool isPrime = false;
        while (!isPrime) {
            n++;
            isPrime = checkPrime(n);
        }
    }
    return n;
}

int main() {
    std::cout << "What prime number would you like to calculate?\n";
    std::cin >> inputNum;
    
    auto output = calculatePrime(inputNum);
    std::cout << "\n" << output;

    return 0;
}