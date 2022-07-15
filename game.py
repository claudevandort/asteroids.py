import pygame
from models import SpaceShip, Asteroid
from utils import load_sprite, print_text

asteroids = []
bullets = []


class Asteroids:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Asteroids.py")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)

        self.ship = SpaceShip((400, 300))
        global asteroids
        asteroids = [Asteroid.create_random(self.screen, self.ship.position) for _ in range(6)]

        self.collision_count = 0

    def main_loop(self):
        while True:
            self._handle_input()
            self._game_logic()
            self._draw()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.ship is not None:
                    self.ship.shoot()
        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_ESCAPE] or is_key_pressed[pygame.K_q]:
            quit()
        if self.ship is None:
            return
        if is_key_pressed[pygame.K_RIGHT]:
            self.ship.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.ship.rotate(clockwise=False)
        elif is_key_pressed[pygame.K_UP]:
            self.ship.accelerate()

    @property
    def game_objects(self):
        global asteroids, bullets
        objects = [*asteroids, *bullets, self.ship]
        if self.ship:
            objects.append(self.ship)
        return objects

    def _game_logic(self):
        global asteroids, bullets
        for obj in self.game_objects:
            if obj:
                obj.move(self.screen)
        rect = self.screen.get_rect()
        for bullet in bullets[:]:
            if not rect.collidepoint(bullet.position):
                bullets.remove(bullet)
        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                if asteroid.collides_with(bullet):
                    asteroids.remove(asteroid)
                    asteroid.split()
                    bullets.remove(bullet)
                    break
        if self.ship:
            for asteroid in asteroids[:]:
                if asteroid.collides_with(self.ship):
                    self.ship = None
                    self.message = "You Lost!"
                    break
        if not asteroids and self.ship:
            self.message = "You Won!"

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        for obj in self.game_objects:
            if obj:
                obj.draw(self.screen)
        if self.message:
            print_text(self.screen, self.message, self.font)
        pygame.display.flip()

        self.clock.tick(30)
