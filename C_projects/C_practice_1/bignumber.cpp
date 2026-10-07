#include <iostream>
#include <array>
#include <string>
#include <bitset>
#include <vector>
#include <cstdint>

using u8 = uint8_t;
using u16 = uint16_t;
using u32 = uint32_t;
using u64 = uint64_t;

struct BigNum {
    std::vector<u32> legs = {};

    // no checks for if legs.length() > max uint32_t

    bool isEmpty() const {
        return (legs.size() == 0);
    }
    
    void trim() {
        while (legs.size() != 0 && legs.back() == 0) {
            legs.pop_back();
        }
    }
    
    bool operator==(const BigNum& o) const {
        if (legs.size() != o.legs.size()) return false;
        if (legs.size() == 0) return true;
        for (u32 i = legs.size() - 1; i + 1 > 0; i--) {
            if (legs.at(i) != o.legs.at(i)) return false;
        }
        return true;
    }
    bool operator<(const BigNum& o) const {
        if (legs.size() != o.legs.size()) {
            return legs.size() < o.legs.size();
        }
        if (legs.size() == 0) return false;
        for (u32 i = legs.size() - 1; i + 1 > 0; i--) {
            if (legs.at(i) != o.legs.at(i)) {
                return legs.at(i) < o.legs.at(i);
            }
        }
        return false;
    }
    bool operator>(const BigNum& o) const {
        return (o < *this);
    }
    bool operator!=(const BigNum& o) const {
    return !(*this == o);
    }
    bool operator<=(const BigNum& o) const {
        return (*this < o) || (*this == o);
    }
    bool operator>=(const BigNum& o) const {
        return (*this > o) || (*this == o);
    }

    BigNum operator&(const BigNum& o) const {
        BigNum r;
        for(u32 i = 0; i < legs.size() && i < o.legs.size(); i++) {
            if (i < o.legs.size()) {
                r.legs.push_back(legs.at(i) & o.legs.at(i));
            }
            // no else because if only leg remains then & will always be 0
        }
        return r;
    }
    BigNum operator^(const BigNum o) const {
        BigNum r;
        for(u32 i = 0; i < legs.size() || i < o.legs.size(); i++) {
            if (i < legs.size() && i < o.legs.size()) {
                r.legs.push_back(legs.at(i) ^ o.legs.at(i));
            } else {
                r.legs.push_back((legs.size() > o.legs.size()) ? legs.at(i) : o.legs.at(i));
            }
            // else is just whatever remains because 1 ^ 0 = 1, 0 ^ 0 = 0
        }
        return r;
    }

    // init (r-eturn, c-arry); for i while at least one leg {
    // total = carry; if leg present (total += leg); carry extra over;}
    // if carry still present, add to new leg; return r
    BigNum operator+(const BigNum& o) const {
        BigNum r; // initialise return num
        u8 c = 0; // carry over starts at 0
        for(u32 i = 0; i < legs.size() || i < o.legs.size(); i++) { // iterate over each until neither has any legs left
            u64 a = c; // add carry over
            if (i < legs.size()) { // if this has leg then add it
                a += legs.at(i);
            } 
            if (i < o.legs.size()) { // if o has leg then add it
                a += o.legs.at(i);
            }
            c = (a >= (1ull << 32)) ? 1 : 0; // check if there is another carry over
            r.legs.push_back(u32(a)); // add
        }
        if (c) {
            r.legs.push_back(1);
        }
        return r;
    }

    //BigNum operator-(const BigNum& o) const {
    //    BigNum r;
    //
    //}

    /*
    // same as above but for - / * % ^
    // copies but for adding different int sizes

    std::string decimal() const {

    }
*/
    std::string baseUint() const {
        std::string s;
        for (u32 i = 0; i < legs.size(); i++) {
            s += std::to_string(legs.at(i));
            s += "-";
        }
        s.pop_back();
        if (s.size() == 0) {
            return "0";
        }
        return s;
    }
};

/*

binary to base 10

find the largest possible base 10 and subtract until cant
find the next largest base 10 and subtract until cant
all the way until 1s

each byte:
1, 2, 4, 8, 16, 32, 64, 128
256, 512, 1024, 2048, 4096, 8192, 16384, 32768
65536, 131072, 262144, 524288, 1|048576, 2|097152, 4|194304, 8|388608

10, 100, 1000, 10000, 100000, 1|000000, 10|000000, 100|000000, 1000|000000
00000000 00000000 00000000 00001010
00000000 00000000 00000000 01100100
00000000 00000000 00000011 11101000
00000000 00000000 00100111 00010000
00000000 00000001 10000110 10100000
00000000 00001111 01000010 01000000
00000000 10011000 10010110 10000000
00000101 11110101 11100001 00000000
00111011 10011010 11001010 00000000


000000000000000000000000000 01 01
 00000000000000000000000001 10 01
  0000000000000000000000111 11 01
   000000000000000000100111 00 01
    00000000000000011000011 01 01
     0000000000001111010000 10 01
      000000001001100010010 11 01
       00000101111101011110 00 01
        0011101110011010110 01 01


*/

int main() {
    BigNum x;
    x.legs = {3223u};
    for (u32 i = 0; i <= 21; i++) {
        x = x + x;
    }

    BigNum y;
    y.legs = {25u};
    for (u32 i = 0; i <= 22; i++) {
        y = y + y;
    }

    bool a = (x != y);

    std::cout << x.baseUint() << "\n";
    std::cout << y.baseUint() << "\n";
    std::cout << std::boolalpha << a;

    return 0;
}