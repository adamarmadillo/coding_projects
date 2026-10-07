#include <iostream>

int fibNum;

int addArrays(int a[], int b[], int aLen, int bLen) {
    int zLen;
    char over;
    int extra = 0;
    if (aLen < bLen) {
        zLen = bLen;
        over = 'b';
    } else if (aLen > bLen) {
        zLen = aLen;
        over = 'a';
    } else {
        zLen = bLen;
        over = 'n';
        long long added = a[zLen] + b[zLen];
        if (added > 2147483647) {
            extra = 1;
        } 
    }
    int z[zLen + extra];
    int carryOver = 0;
    long long added;
    for (int n = 0; n < zLen - 1; n++) {
        added = a[n] + b[n];
        z[n] = carryOver;
        if (added + carryOver > 2147483647) {
            carryOver = 1;
            added -= 2147483647;
        } else {carryOver = 0;}
        z[n] += added;
    }
    int zEnd = zLen - 1;
    z[zEnd] = carryOver;
    if (over == 'a') {
        added = a[zEnd];
    } else if (over == 'b') {
        added = b[zEnd];
    } else {
        added = a[zEnd] + b[zEnd];
    }
    if (added + carryOver > 2147483647) {
        carryOver = 1;
        added -= 2147483647;
    } else {carryOver = 0;}
    z[zEnd] += added;
    if (extra) {
        z[zEnd + 1] = 1;
    }

    return (z, zLen);
    //check both digits are present
    //if only one then set the val
    //iterate adding each digit
    //if the 
}

int main() {
    std::cout << "Fib: \n";
    std::cin >> fibNum;

    int a[1] = {0};
    int b[1] = {0};
    int aLen = sizeof(a) / 4;
    int blen = sizeof(b) / 4;

    int z[0];
    int zLen;

    int x[1] = {27};
    int y[1] = {29};

    int j[1], jLen = addArrays(x, y, 1, 1);
    for (int i : j) {
        std::cout << z;
    }

    //for (int i = 0; i < fibNum; i++) {
    //    int z = addArrays();
    //    moveArrays();
    //    printArrays();    
    //}
}