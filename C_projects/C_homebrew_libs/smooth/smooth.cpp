#include "smooth.h"

double smoothFunc(double i) {
    return -2 * i * i * i + 3 * i * i;
}
double smoothStep(double a, double b, double x) {
    double ratio = smoothFunc(x);
    return a * (1 - ratio) + b * ratio;
}

double smootherFunc(double i) {
    return 6 * std::pow(i, 5) - 15 * std::pow(i, 4) + 10 * std::pow(i, 3);
}
double smootherStep(double a, double b, double x) {
    double ratio = smootherFunc(x);
    return a * (1 - ratio) + b * ratio;
}

double smoothCap(double i, double c, int k) {
    if (k < 0) { throw std::invalid_argument("smoothCap: cannot take negative sharpness"); }
    return i / std::pow(1 + std::pow(std::abs(i / c), k), (1.0 / k));
}

double easeIn(double i, double k) {
    if (k < 0) { throw std::invalid_argument("easeOut: cannot take negative sharpness"); }
    if (i < -1 || i > 1) { throw std::out_of_range("easeOut: cannot take |input| > 1"); }
    double o = 1 - (1 + k) * (1 - std::abs(i)) / (1 + k * (1 - std::abs(i)));
    return sign(i) * o;
}
double easeOut(double i, double k) {
    if (k < 0) { throw std::invalid_argument("easeIn: cannot take negative sharpness"); }
    if (i < -1 || i > 1) { throw std::out_of_range("easeIn: cannot take |input| > 1"); }
    double o = (1 + k) * std::abs(i) / (1 + k * std::abs(i));
    return sign(i) * o;
}
double easeInOut(double i, double k) {
    if (k < 0) { throw std::invalid_argument("easeOut: cannot take negative sharpness"); }
    if (i < -1 || i > 1) { throw std::out_of_range("easeInOut: cannot take |input| > 1"); }
    if (std::abs(i) < 0.5) {
        return 0.5 * easeIn(i * 2, k); 
    } else {
        return sign(i) * 0.5 + 0.5 * easeOut(2 * (i - sign(i) * 0.5), k);
    }
}
double easeOutIn(double i, double k) {
    if (k < 0) { throw std::invalid_argument("easeOut: cannot take negative sharpness"); }
    if (i < -1 || i > 1) { throw std::out_of_range("easeInOut: cannot take |input| > 1"); }
    else if (std::abs(i) < 0.5) {
        return 0.5 * easeOut(i * 2, k); 
    } else {
        return sign(i) * 0.5 + 0.5 * easeIn(2 * (i - sign(i) * 0.5), k);
    }
}