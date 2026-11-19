#include <SFML/Graphics.hpp>
#include <optional>

int main() {
    const float W = 800.f, H = 600.f, R = 25.f;
    sf::RenderWindow window(sf::VideoMode({800u, 600u}), "Bouncy Ball");
    window.setFramerateLimit(60);

    sf::CircleShape ball(R);
    ball.setFillColor(sf::Color::Red);
    ball.setPosition({100.f, 100.f});

    sf::Vector2f vel(200.f, 0.f);
    const float gravity = 900.f;
    const float restitution = 0.8f;

    sf::Clock clock;
    while (window.isOpen()) {
        while (const std::optional event = window.pollEvent())
            if (event->is<sf::Event::Closed>()) window.close();

        float dt = clock.restart().asSeconds();

        vel.y += gravity * dt;
        ball.move(vel * dt);

        sf::Vector2f p = ball.getPosition();

        if (p.y + 2*R > H) {
            ball.setPosition({p.x, H - 2*R});
            vel.y = -vel.y * restitution;
        } else if (p.y < 0) {
            ball.setPosition({p.x, 0.f});
            vel.y = -vel.y * restitution;
        }
        p = ball.getPosition();
        if (p.x + 2*R > W) {
            ball.setPosition({W - 2*R, p.y});
            vel.x = -vel.x * restitution;
        } else if (p.x < 0) {
            ball.setPosition({0.f, p.y});
            vel.x = -vel.x * restitution;
        }

        window.clear(sf::Color::Black);
        window.draw(ball);
        window.display();
    }
}