#include <iostream>
#include <string>
#include <array>
#include <sstream>

// ATTEMPT 3
// addition function will switch around pointers to different buffers
// ALSO bug fixed leading 0s on sections being left out


// setup:
// input = fibNum, intSize
// a and b are arrays of ints
// adding function adds arrays together

// initialising integer digits (9 * intSize)
const int intSize = 2500;
const int maxSize = intSize / 0.209 * 9 - 1;
const int base = 1000000000;

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
    if (sum >= base) {
        remainder = 1;
        sum -= base;
    }
    return {sum, remainder};
}

// for each int
// add them together along with the remainder from the last operation
// next remainder is the generated remainder
// generated sum is set to the int
void add(
    const std::array<int, intSize>& a,
    const std::array<int, intSize>& b,
    std::array<int, intSize>& c
) {
    char remainder = 0;
    for (int i = 0; i < intSize; i++) {
        overflowInt added = overflowAddInts(a[i], b[i], remainder);
        remainder = added.remainder;
        c[i] = added.sum;
    }
}

void cycleAdd(
    std::array<int, intSize>& a,
    std::array<int, intSize>& b,
    std::array<int, intSize>& c,
    int& turn,
    int fibNum
) {
    for (int i = 0; i < fibNum; i++) {
        if (turn == 0) {
            add(a, b, c);
        } else if (turn == 1) {
            add(b, c, a);
        } else {
            add(c, a, b);
        }
        turn++;
        turn %= 3;
    }
}

int findStart(const std::array<int, intSize>& arr) {
    bool found = false;
    int index = intSize - 1;
    while (!found && index > 0) {
        if (arr[index] != 0) {
            found = true;
        } else {
            index -= 1;
        }
    }
    return index;
}

int getNumDigits(const std::array<int, intSize>& arr, int startIndex) {
    int finalDigit = arr[startIndex];
    int finalDigitSize = 0;
    while (finalDigit > 0) {
        finalDigit /= 10;
        finalDigitSize++;
    }
    return (startIndex) * 9 + finalDigitSize;
}

void printPostInfo(int fibNum, int numDigits, int maxSize) {
    std::cout << "\n\nfibonacci number " << fibNum;
    std::cout << "\ndigits: " << numDigits;
    std::cout << "\nmax size for digits available:\n" << maxSize;
}

std::string leadZeros(int input) {
    std::ostringstream oss;
    oss << input;
    std::string s = "000000000";
    s.replace(9 - oss.str().length(), 9, oss.str());
    return s;
}

void printOutputNum(const std::array<int, intSize>& outputNum, int startIndex) {
    std::cout << outputNum[startIndex];
    for (int i = startIndex - 1; i >= 0; i--) {
        // print 9 digit by 9 digit
        std::cout << leadZeros(outputNum[i]);
    }
}

void askSeq(int& fibNum) {
    std::cout << "what fibonacci number? \n";
    std::cin >> fibNum;
    // lock fibnum to the maximum size that will fit
    if (fibNum >= maxSize) {
        fibNum = maxSize;
    }
    std::cout << "\nyour number:\n";
}

int main() {

    // init function vars
    std::array<int, intSize> a = {}, c = {};
    std::array<int, intSize> b = {1};
    int fibNum;
    int turn = 0;
    std::array<int, intSize>* pointers[3] = {&a, &b, &c};

    // run the prompt sequence
    askSeq(fibNum);

    // add the numbers until the target is reached
    cycleAdd(a, b, c, turn, fibNum);

    // set the output number to the specified number
    const std::array<int, intSize>& outputNum = *pointers[turn];

    // find the start index and print the number
    int startIndex = findStart(outputNum);
    printOutputNum(outputNum, startIndex);

    // print info
    printPostInfo(fibNum, getNumDigits(outputNum, startIndex), maxSize);

    return 0;
}