import pygame
import math
pygame.init()

WIDTH, HEIGHT = 1280, 800
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (169, 169, 169)
GREEN = (0, 255, 0)


WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Plant Simulation")

class Planet:
    #AU står för Astronomical Units
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 150 / AU # 1AU = 100 pixlar
    TIMESTEP = 3600*24 # 1 dag


    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0
    
    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x_point = point[0] * self.SCALE + WIDTH / 2
                y_point = point[1] * self.SCALE + HEIGHT / 2
                updated_points.append((x_point, y_point))
            pygame.draw.lines(win, self.color, False, updated_points, 2)
        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        distance = max(distance, 1)
        force = self.G  * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

class Moon:
    def __init__(self, planet, orbit_radius_px, speed, radius, color):
        self.planet = planet
        self.orbit_radius = orbit_radius_px
        self.speed = speed
        self.angle = 0
        self.radius = radius
        self.color = color

    def update(self):
        self.angle += self.speed

    def draw(self, win):
        earth_x = self.planet.x * Planet.SCALE + WIDTH / 2
        earth_y = self.planet.y * Planet.SCALE + HEIGHT / 2
        moon_x = earth_x + math.cos(self.angle) * self.orbit_radius
        moon_y = earth_y + math.sin(self.angle) * self.orbit_radius
        pygame.draw.circle(win, self.color, (int(moon_x), int(moon_y)), self.radius)

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GRAY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    moon = Moon(earth, orbit_radius_px=35, speed=0.05, radius=5, color=DARK_GRAY)

    planets = [sun, earth, mercury]

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)
        

        moon.update()
        moon.draw(WIN)
        pygame.display.update()

    pygame.quit()
main()