#pragma once
#include "../Vec2/Vec2.h"
#include <string>
#include <vector>
#include <algorithm>
#include <stdexcept>

template<typename T>
struct Grid {
    Vec2s dim;
    std::vector<T> data;

    Grid() : dim(), data() {}
    Grid(Vec2s dim) : dim(dim), data(dim.size()) {}
    Grid(int width, int height) : dim(width, height), data(dim.size()) {}

    T& at(Vec2s pos) { return data.at(pos.toIndex(dim.x)); }
    const T& at(Vec2s pos) const { return data.at(pos.toIndex(dim.x)); }
    T& at(size_t index) { return data.at(index); }
    const T& at(size_t index) const { return data.at(index); }

    void setAt(Vec2i pos, T value, bool throwOutOfBounds=true) { 
        if (pos.isInBounds(dim)) { at(pos) = value; }
        else if (throwOutOfBounds) throw std::out_of_range("Grid::setAt: pos out of range");
    }
    void setAt(size_t index, T value, bool throwOutOfBounds=true) { 
        if (index < data.size()) { at(index) = value; }
        else if (throwOutOfBounds) throw std::out_of_range("Grid::setAt: pos out of range");
    }

    void fill(T value) {
        std::fill(data.begin(), data.end(), value);
    }

    template<typename C>
    void setByIndex(C&& callable) {
        for (size_t i = 0; i < data.size(); i++)
            data[i] = callable(i);
    }

    template<typename C>
    void setByPos(C&& callable) {
        for (size_t i = 0; i < data.size(); i++)
            data[i] = callable(Vec2iFromIndex(i, dim.x));
    }

    constexpr size_t size() { return dim.size(); }
};