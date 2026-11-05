#pragma once
#include "../utils/utils.h"
#include <string>
#include <stdexcept>
#include <type_traits>
#include <cmath>
#include <concepts>

template<typename T>
struct Vec2;
template<typename T> 
struct Rect;

using Vec2i = Vec2<int>;
using Recti = Rect<int>;
using Vec2d = Vec2<double>;
using Rectd = Rect<double>;
using Vec2s = Vec2<size_t>;
using Rects = Rect<size_t>;

enum class dir { left, right, L, R, clockwise, counterClockwise, C, CC };

template<typename T>
struct Vec2 {
    static_assert(std::is_same_v<T, int> || std::is_same_v<T, double> || std::is_same_v<T, size_t>, "Vec2 only [known] to support int, double, or size_t, check before implementing");
    T x{}, y{};
    
    
    // constructors
    constexpr Vec2() = default;
    constexpr Vec2(T x, T y) : x(x), y(y) {}
    constexpr explicit Vec2(T m) : x(m), y(m) {}

    template<typename U> requires (!std::is_same_v<T, U>)
    constexpr Vec2(Vec2<U> i) : Vec2(i.template castType<T>()) {}
    

    // checking and indexing
    constexpr T size() const { return x * y; }
    constexpr size_t toIndex(int rowWidth) const {
        checkPositive();
        if (rowWidth < 0) throw std::invalid_argument("Vec2::toIndex: negative row width");
        return y * rowWidth + x;
    }

    bool isInBounds(Vec2 b) const { return x >= 0 && x < b.x && y >= 0 && y < b.y; }
    const Vec2& checkInBounds(Vec2 b, const std::string& error_message = "Vec2::checkInBounds: Vec2 out of bounds") const {
        if (!isInBounds(b)) throw std::out_of_range(error_message);
        return *this;
    }
    bool inRect(Rect<T> r) const { return (r.contains(*this)); }
    const Vec2& checkPositive(const std::string& error_message = "Vec2::checkPositive: Vec2 x or y not positive integers") const {
        if (x < 0 || y < 0) throw std::invalid_argument(error_message);
        return *this;
    }


    // operators
    Vec2 operator+(Vec2 i) const { return {x + i.x, y + i.y}; }
    Vec2 operator-(Vec2 i) const {
        if constexpr (std::is_same_v<T, size_t>)
            if (x < i.x || y < i.y) throw std::underflow_error("Vec2<size_t>: subtraction underflow");
        return {x - i.x, y - i.y};
    }
    Vec2 operator*(Vec2 i) const { return {x * i.x, y * i.y}; }
    Vec2 operator/(Vec2 i) const {
        if (i.x == 0 || i.y == 0) throw std::invalid_argument("Vec2: division by zero");
        return {x / i.x, y / i.y};
    }

    Vec2 operator+(T i) const { return {*this + Vec2(i)}; }
    Vec2 operator-(T i) const { return {*this - Vec2(i)}; }
    Vec2 operator*(T i) const { return {*this * Vec2(i)}; }
    Vec2 operator/(T i) const { return {*this / Vec2(i)}; }
    Vec2& operator+=(Vec2 i) { *this = *this + i; return *this; }
    Vec2& operator-=(Vec2 i) { *this = *this - i; return *this; }
    Vec2& operator*=(Vec2 i) { *this = *this * i; return *this; }
    Vec2& operator/=(Vec2 i) { *this = *this / i; return *this; }
    Vec2& operator+=(T i) { *this = *this + i; return *this; }
    Vec2& operator-=(T i) { *this = *this - i; return *this; }
    Vec2& operator*=(T i) { *this = *this * i; return *this; }
    Vec2& operator/=(T i) { *this = *this / i; return *this; }

    Vec2i operator%(Vec2i i) const {
        if (i.x == 0 || i.y == 0) throw std::invalid_argument("Vec2: modulo by zero");
        return {x % i.x, y % i.y};
    }
    Vec2i operator%(int i) const { return *this % Vec2i(i); }
    Vec2i& operator%=(Vec2i i) { *this = *this % i; return *this; }
    Vec2i& operator%=(int i) { *this = *this % i; return *this; }
    
    template<typename U>
    constexpr bool operator==(Vec2<U> i) const { return x == i.x && y == i.y; }

    T squaredMagnitude() const { return x * x + y * y; }
    double magnitude() const { return std::sqrt(squaredMagnitude()); }
    double angle() const { return std::atan2(y, x); }
    double distTo(Vec2 i) const requires (!std::is_same_v<T, size_t>) { return (i - *this).magnitude(); }
    
    Vec2d normalised() const { return Vec2d(*this) / magnitude(); }
    Vec2d& normalise() requires (!std::is_same_v<T, size_t>) { *this = normalised(); return *this; }

    Vec2 perpendicular(dir dir) const requires (!std::is_same_v<T, size_t>) {
        if (dir == dir::left || dir == dir::L || dir == dir::counterClockwise || dir == dir::CC) {
            return (Vec2<T>(-1 * y, x));
        } else { return (Vec2<T>(y, -1 * x)); }
    }
    Vec2d normal(dir dir) const { return perpendicular(dir).normalised(); }
    Vec2d normal(int sign) const {
        if (sign != 1 && sign != -1) { throw std::invalid_argument("Vec2::normal: sign must be -1 or 1"); }
        return normal((sign == 1) ? dir::counterClockwise : dir::clockwise);
    }
    Vec2d normalLeft() const { return normal(dir::left); }
    Vec2d normalRight() const { return normal(dir::right); }

    template<typename U>
    double dot(Vec2<U> i) const { return x * i.x + y * i.y; }
    template<typename U> requires (!std::is_same_v<T, size_t>) 
    double cross(Vec2<U> i) const { return x * i.y - y * i.x; }

    template<typename U> requires (!std::is_same_v<U, size_t>)
    constexpr Vec2<U> castType() const { return {static_cast<U>(x), static_cast<U>(y)}; }

    template<typename U> requires (std::is_same_v<U, size_t>)
    constexpr Vec2<U> castType() const { return {size_tSafeCast(x), size_tSafeCast(y)}; }

    private:
    template<typename U>
    static constexpr size_t size_tSafeCast(U i) {
        if (!(i >= 0)) { throw std::domain_error("size_tSafeCast: cannot cast input less than 0"); }
        if constexpr (std::is_floating_point_v<U>) {
            if (i >= static_cast<double>(std::numeric_limits<size_t>::max()))
                throw std::overflow_error("size_tSafeCast: input too large for size_t");
        }
        return static_cast<size_t>(i);
    }
};

template <typename T>
struct Rect {
    Vec2<T> pos, dim;

    // init for (vec, vec) or (x, y, x, y)
    Rect(Vec2<T> pos, Vec2<T> dim) : pos(pos), dim(dim) {}
    Rect(T posx, T posy, T width, T height) : pos{posx, posy}, dim{width, height} {}

    // checks if rect corners are set -/- to +/+, checks rect dim lengths != 0
    const Rect& checkValid(const std::string& error_message = "Rect::checkValid: Rect side length less 0") const {
        dim.checkPositive(error_message);
        return *this;
    }

    // checks if rect is within bounds, b side can be = bounds as internal positions are determined by bx/by - 1
    bool isInBounds(Vec2<T> bounds) const {
        return pos.isInBounds(bounds) &&
        pos.x + dim.x <= bounds.x &&
        pos.y + dim.y <= bounds.y;
    }
    const Rect& checkInBounds(Vec2<T> bounds, const std::string& error_message = "Rect::checkInBounds: Rect out of bounds") const {
        if (!isInBounds(bounds)) throw std::out_of_range(error_message);
        return *this;
    }

    // checks if a point is in a rect, can be = a but must be < b
    bool contains(Vec2<T> p) const {
        return pos.x <= p.x && 
        p.x < pos.x + dim.x && 
        pos.y <= p.y && 
        p.y < pos.y + dim.y;
    }
};

Vec2d Vec2dFromAngle(double theta);
Vec2d Vec2dFromPolar(double theta, double magnitude);
Vec2i Vec2iFromIndex(int index, int rowWidth);