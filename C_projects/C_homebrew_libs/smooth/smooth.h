#pragma once
#include "../utils/utils.h"
#include <cmath>
#include <stdexcept>
#include <algorithm>

double smoothFunc(double i);
double smoothStep(double a, double b, double step);
double smootherFunc(double i);
double smootherStep(double a, double b, double step);

double smoothCap(double i, double cap, int sharpness=10);

double easeIn(double i, double sharpness=10);
double easeOut(double i, double sharpness=10);
double easeInOut(double i, double sharpness=10);
double easeOutIn(double i, double sharpness=10);

double inOutPlateau(double i, double a, double midslope=0.1);