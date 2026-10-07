#include <iostream>
#include <array>

// ATTEMPT 3
// even LARGER numbers, 9 digits stored in each int
// also heavily cleaned up

// setup:
// input = fibNum, intSize
// a and b are arrays of ints
// adding function adds arrays together

// initialising integer digits (9 * intSize)
const int intSize = 100000;
const int maxSize = static_cast<double>(intSize / 0.209) * 9 - 1;

// add integers with remainders
struct overflowInt {
    int sum;
    char remainder;
};

// add the ints
// if they are larger than 1B, add 1 to the carry over
overflowInt overflowAddInts(int a, int b, int c) {
    int sum = a + b + c;
    // if they add up to 1B or more, return remainder = 1 and sum -= 1B
    char remainder = 0;
    if (sum >= 1000000000) {
        remainder = 1;
        sum -= (1000000000);
    }
    sum = static_cast<int>(sum);
    return {sum, remainder};
}

// for each int
// add them together along with the remainder from the last operation
// next remainder is the generated remainder
// generated sum is set to the int
void add(std::array<int, intSize>& a, std::array<int, intSize>& b) {
    std::array<int, intSize> z;
    char remainder = 0;
    for (int i = 0; i < intSize; i++) {
        overflowInt added = overflowAddInts(a[i], b[i], remainder);
        remainder = added.remainder;
        z[i] = added.sum;
    }
    a = b;
    b = z;
}

int findStart(const std::array<int, intSize>& arr) {
    bool found = 0;
    int index = intSize - 1;
    while (!found && index > 0) {
        if (arr[index] != 0) {
            found = 1;
        } else {
            index -= 1;
        }
    }
    return index;
}

int numDigits(const std::array<int, intSize>& arr, int startIndex) {
    int finalDigit = arr[startIndex];
    int finalDigitSize = 0;
    while (finalDigit > 0) {
        finalDigit /= 10;
        finalDigitSize++;
    }
    return (startIndex) * 9 + finalDigitSize;
}

int main() {
    // init function vars
    std::array<int, intSize> a = {};
    std::array<int, intSize> b = {1};
    int fibNum;

    // ask seq
    std::cout << "what fibonacci number? \n";
    std::cin >> fibNum;
    std::cout << "\nyour number:\n";

    // lock fibnum to the maximum size that will fit
    if (fibNum >= maxSize) fibNum = maxSize;

    // add each set of digits and carry remainders
    for (int i = 0; i < fibNum; i++) {
        add(a, b);
    }

    // print num piece wise to the terminal
    int startIndex = findStart(a);
    for (int i = startIndex; i >= 0; i--) {
        int digits = a[i];

        // include 0s, except for the first one
        if (digits < 10 && i != startIndex) {
            std::cout << '0';
        }
        //print 2 digit by 2 digit
        std::cout << digits;
    }

    // print info
    std::cout << "\n\nfibonacci number " << fibNum;
    std::cout << "\ndigits: " << numDigits(a, startIndex);
    std::cout << "\nmax size for digits available:\n" << maxSize;
    return 0;
}