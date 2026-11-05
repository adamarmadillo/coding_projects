#include "draw.h"

Colour& Colour::q(Colour c) {
    r = quantise(r, c.r);
    g = quantise(g, c.g);
    b = quantise(b, c.b);
    return *this;
}

void Surface::setAt(Vec2i pos, Pixel p, bool strictBounds) {
    Grid<Pixel>::setAt(pos, p, strictBounds);
}
void Surface::setAt(size_t i, Pixel p, bool strictBounds) {
    Grid<Pixel>::setAt(i, p, strictBounds);
}

// draw rect, throws if rect is bad, smallest is 1px otherwise throws
void Surface::drawRect(Recti r, Colour c, bool strictBounds) {
    r.checkValid();
    if (strictBounds){ 
        r.checkInBounds(dim);
        for (int x = r.pos.x; x < r.pos.x + r.dim.x; x++)
            for (int y = r.pos.y; y < r.pos.y + r.dim.y; y++)
                setAt({x, y}, c);
    } else { 
        for (int x = r.pos.x; x < r.pos.x + r.dim.x; x++)
            for (int y = r.pos.y; y < r.pos.y + r.dim.y; y++) {
                Vec2i p(x, y);
                if (p.isInBounds(dim))
                    setAt(p, c);
            }
    }
}
void Surface::drawRect(Recti r, uint32_t c, bool strictBounds) {
    drawRect(r, c, strictBounds);
}


// make these 2 private on draw.h
void Surface::plotLineLow(Vec2i a, Vec2i b, Colour c, bool strictBounds) { // assumes [-1 < dy/dx < 1], [dx > 0], [a.x < b.x] 
    int dx = b.x - a.x;
    int dy = b.y - a.y;
    int yi = 1;
    if (dy < 0) {
        yi = -1;
        dy = -dy;
    }
    int D = (2 * dy) - dx;
    int y = a.y;

    for (int x = a.x; x <= b.x; x++) {
        if (strictBounds) {
            setAt({x, y}, c);
        } else if (Vec2i(x, y).isInBounds(dim)) {
            setAt({x, y}, c);
        }
        if (D > 0) {
            y += yi;
            D += (2 * (dy - dx));
        } else {
            D += 2*dy;
        }
    }
}

void Surface::plotLineHigh(Vec2i a, Vec2i b, Colour c, bool strictBounds) { // assumes [-1 < dx/dy < 1], [dy > 0], [a.y < b.y] 
    int dx = b.x - a.x;
    int dy = b.y - a.y;
    int xi = 1;
    if (dx < 0) {
        xi = -1;
        dx = -dx;
    }
    int D = (2 * dx) - dy;
    int x = a.x;

    for (int y = a.y; y <= b.y; y++) {
        if (strictBounds) {
            setAt({x, y}, c);
        } else if (Vec2i(x, y).isInBounds(dim)) {
            setAt({x, y}, c);
        }
        if (D > 0) {
            x += xi;
            D += (2 * (dx - dy));
        } else {
            D += 2*dx;
        }
    }
}

// https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
void Surface::drawLine(Vec2i a, Vec2i b, Colour c, bool strictBounds) {
    if (strictBounds) {
        a.checkInBounds(dim, "drawLine: point a out of bounds");
        b.checkInBounds(dim, "drawLine: point b out of bounds");
    }
    if (std::abs(a.y - b.y) <= std::abs(a.x - b.x)) {
        if (a.x > b.x) std::swap(a, b);
        plotLineLow(a, b, c, strictBounds);
    } else {
        if (a.y > b.y) std::swap(a, b);
        plotLineHigh(a, b, c, strictBounds);
    }
}
void Surface::drawLine(Vec2i a, Vec2i b, uint32_t c, bool strictBounds) {
    drawLine(a, b, Colour(c), strictBounds);
}

void Surface::drawGrid(Vec2i gridSize, Vec2i cellSize, Colour c, Vec2i cornerPos, bool strictBounds) {
    for (int ix = 0; ix <= gridSize.x; ix++) {
        int x = cornerPos.x + ix * cellSize.x;
        drawLine(
            {x, cornerPos.y}, 
            {x, cornerPos.y + gridSize.y * cellSize.y}, 
            c, strictBounds
        );
    }
    for (int iy = 0; iy <= gridSize.y; iy++) {
        int y = cornerPos.y + iy * cellSize.y;
        drawLine(
            {cornerPos.x, y}, 
            {cornerPos.x + gridSize.x * cellSize.x, y}, 
            c, strictBounds
        );
    }
}