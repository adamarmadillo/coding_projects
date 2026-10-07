#include <iostream>
#include <string>

std::string x = "hello world";

int main() {

    std::cout << x.at(4) << "\n";
    std::cout << x.substr(3, 7) << "\n";
    std::cout << x.find("world") << "\n";
    std::cout << x.find("fart") << "\n";

    std::string y1, y2, y3, y4;
    y1 = y2 = y3 = y4 = x;

    y1 += "!!!";
    std::cout << y1 << "\n";
    
    y2.insert(0, "Well... ");
    std::cout << y2 << "\n";
    
    y3.erase(3, 4);
    std::cout << y3 << "\n";

    y4.pop_back();
    std::cout << y4 << "\n";

    return 0;
}

