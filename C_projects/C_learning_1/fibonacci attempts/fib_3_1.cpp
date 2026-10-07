#include <iostream>
#include <array>

// ATTEMPT 3
// even larger numbers, 2 digits stored in each char
// also heavily cleaned up

// setup:
// input = fibNum, intSize
// a and b are arrays of chars
// adding function adds arrays together

// initialising integer digits (2 * intSize)
const int intSize = 104501;
const int maxSize = static_cast<double>(intSize / 0.209) * 2 - 1;

// add integers with remainders
struct overflowInt {
    char sum;
    char remainder;
};

// add the characters
// if they are larger than 100, add 1 to the carry over
overflowInt overflowAddInts(char a, char b, char c) {
    // add them together
    unsigned short sum = a + b + c;
    // if they add up to 100 or more, return remainder = 1 and sum -= 100
    char remainder = 0;
    if (sum >= 100) {
        remainder = 1;
        sum -= (100);
    }
    sum = static_cast<char>(sum);
    return {sum, remainder};
}

// for each character
// add them together along with the remainder from the last operation
// next remainder is the generated remainder
// generated sum is set to the character
void add(std::array<char, intSize>& a, std::array<char, intSize>& b) {
    std::array<char, intSize> z;
    char remainder = 0;
    for (unsigned int i = 0; i < intSize; i++) {
        overflowInt added = overflowAddInts(a[i], b[i], remainder);
        remainder = added.remainder;
        z[i] = added.sum;
    }
    a = b;
    b = z;
}

int findStart(std::array<char, intSize> arr) {
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

int numDigits(std::array<char, intSize> arr, int startIndex) {
    return (startIndex + 1) * 2 - ((arr[startIndex] < 10) ? 1 : 0);
}

int main() {
    // init function vars
    std::array<char, intSize> a = {};
    std::array<char, intSize> b = {1};
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