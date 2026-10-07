#include <iostream>
#include <array>

// ATTEMPT 3
// larger numbers, using a home brew fixed size array

// input = fibNum, intSize
// a and b are arrays of chars
// adding function adds arrays together

const int intSize = 21000;

struct overflowInt {
    char sum;
    char remainder;
};

// for each char in the array
// add the characters and carry over
// if they are larger than 10, add 1 to the carry over
overflowInt overflowAddInts(char a, char b, char c) {
    // add them together
    unsigned short sum = static_cast<unsigned short>(a) + static_cast<unsigned short>(b) + static_cast<unsigned short>(c);
    // if they add up to 10 or more, return remainder = 1 and sum -= 10
    char remainder = 0;
    if (sum >= 10) {
        remainder = 1;
        sum -= (10);
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

std::array<char, intSize> a, b = {};
int fibNum;

int main() {

    b[0] = 1;

    std::cout << "what fibonacci number? \n";
    std::cin >> fibNum;
    std::cout << "\nyour number:\n";

    int maxSize = static_cast<double>(intSize / 0.21);

    if (fibNum >= maxSize) fibNum = maxSize;

    for (int i = 0; i < fibNum; i++) {
        add(a, b);
    }

    // long string of 0s
    // iterate along the string to find the first non 0
    // set that as the starting point for printing the number
    bool writeStarted = false;
    int returnSize = 0;
    for (int i = intSize - 1; i >= 0; i--) {
        if (static_cast<int>(a[i]) != 0 || writeStarted) {
            if (! writeStarted) {
                writeStarted = 1;
                returnSize = i;
            }
            std::cout << static_cast<int>(a[i]);
        }
    }
    std::cout << "\n\nfibonacci number " << fibNum << "\n" << "digits: " << returnSize + 1 << "\nmax size for digits available:\n" << maxSize;
    return 0;
}