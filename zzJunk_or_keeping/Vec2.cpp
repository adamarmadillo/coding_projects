


Vec2i::Vec2i(int x, int y) : x(x), y(y) {};
Vec2i::Vec2i(int m) : x(m), y(m) {};
Vec2i::Vec2i() : x(0), y(0) {};

bool Vec2i::isInBounds(Vec2i b) const {
    return x >= 0 && x < b.x && 
    y >= 0 && y < b.y;
}
void Vec2i::checkInBounds(Vec2i b, const std::string& error_message) const {
    if (!isInBounds(b)) {
        throw std::out_of_range(error_message);
    }
}
bool Vec2i::inRect(Recti r) const {
    return (r.contains(*this));
}

Vec2i Vec2i::operator+(Vec2i i) const { return {x + i.x, y + i.y}; }
Vec2i Vec2i::operator-(Vec2i i) const { return {x - i.x, y - i.y}; }
Vec2i Vec2i::operator*(int i) const { return {x * i, y * i}; }
Vec2i Vec2i::operator/(int i) const {
    if (i == 0) throw std::invalid_argument("Vec2i: division by zero");
    return {x / i, y / i};
}
Vec2i Vec2i::operator+=(Vec2i i) { *this = *this + i; return *this; }
Vec2i Vec2i::operator-=(Vec2i i) { *this = *this - i; return *this; }
Vec2i Vec2i::operator*=(int i) { *this = *this * i; return *this; }
Vec2i Vec2i::operator/=(int i) { *this = *this / i; return *this; }


// init for (vec, vec) or (x, y, x, y)
Recti::Recti(Vec2i pos, Vec2i size) : pos(pos), size(size) {};
Recti::Recti(int posx, int posy, int width, int height) : pos{posx, posy}, size{width, height} {};

// checks if rect corners are set -/- to +/+, checks rect size lengths != 0
void Recti::checkValid(const std::string& error_message) const {
    if (size.x <= 0 || size.y <= 0) { throw std::invalid_argument(error_message); }
}

// checks if rect is within bounds, b side can be = bounds as internal positions are determined by bx/by - 1
bool Recti::isInBounds(Vec2i bounds) const {
    return pos.isInBounds(bounds) &&
    pos.x + size.x <= bounds.x &&
    pos.y + size.y <= bounds.y;
}
void Recti::checkInBounds(Vec2i bounds, const std::string& error_message) const {
    if (!isInBounds(bounds)) { throw std::out_of_range(error_message); }
}

// checks if a point is in a rect, can be = a but must be < b
bool Recti::contains(Vec2i p) const {
    return pos.x <= p.x && 
    p.x < pos.x + size.x && 
    pos.y <= p.y && 
    p.y < pos.y + size.y;
}