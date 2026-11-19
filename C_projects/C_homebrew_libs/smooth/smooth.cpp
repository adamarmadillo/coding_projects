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
double inOutPlateau(double t, double a, double midSlope)
{
    t = std::clamp(t, 0.0, 1.0);
    a = std::clamp(a, 0.001, 0.499);
    const double s = std::clamp(midSlope, 0.0, 1.0 / (1.0 - a));

    // Rise covered by each ease section; the middle covers s*(1-2a).
    const double R = (1.0 - s * (1.0 - 2.0 * a)) / 2.0;

    // Ease-in cubic p(x) = c2*x^2 + c3*x^3 on [0,a]:
    // p(0)=0, p'(0)=0, p(a)=R, p'(a)=s
    const double c2 = (3.0 * R - s * a) / (a * a);
    const double c3 = (s * a - 2.0 * R) / (a * a * a);
    auto ease = [&](double x) { return c2 * x * x + c3 * x * x * x; };

    if (t < a)       return ease(t);
    if (t > 1.0 - a) return 1.0 - ease(1.0 - t);
    return R + s * (t - a);
}