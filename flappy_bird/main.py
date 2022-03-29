import pygame as pg
import os
import random
from typing import List


# Constants
WIDTH = 600
HEIGHT = 800
FPS = 60
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)


class Bird (pg.sprite.Sprite):
    def __init__(self, x, y, sprites):
        pg.sprite.Sprite.__init__(self)
        self.max_rotation = 25  # deg
        self.rot_vel = 10
        self.animation_time = 5
        self.tilt = 0
        self.tick = 0
        self.vel = 0
        self.sprites = sprites
        self.sprite_count = 0
        self.image = self.sprites[0]
        self.height = x
        # add pygame rect centered
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.height = self.rect.y
        self.score = 0
        self.radius = self.rect.width/2

    def jump(self):
        self.vel = -10.5
        self.tick = 0
        self.height = self.rect.y

    def update(self):
        self.tick += 1

        displacement = self.vel*self.tick + 1.5*self.tick**2
        falling_vel = 6
        if displacement >= falling_vel:  # TODO: make this a constant, and Increase it
            displacement = falling_vel

        elif displacement < 0:
            displacement -= 2

        self.rect.y = self.rect.y + displacement

        self.sprite_count += 1
        if self.sprite_count < self.animation_time:
            self.image = self.sprites[0]
        elif self.sprite_count < self.animation_time*2:
            self.image = self.sprites[1]
        elif self.sprite_count < self.animation_time*3:
            self.image = self.sprites[2]
        elif self.sprite_count < self.animation_time*4:
            self.image = self.sprites[1]
        elif self.sprite_count < self.animation_time*4 + 1:
            self.image = self.sprites[0]
            self.sprite_count = 0

        if displacement < 0 or self.rect.y < self.height + 50:
            if self.tilt < self.max_rotation:
                self.tilt = self.max_rotation
        else:
            if self.tilt > -90:
                self.tilt -= self.rot_vel

        # rotate the sprite and set the bird to the new sprite
        self.image = pg.transform.rotate(self.image, self.tilt)
        self.rect.center = self.rect.center


class Ground(pg.sprite.Sprite):
    def __init__(self, x, y, sprite):
        pg.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Pipe(pg.sprite.Sprite):
    def __init__(self, x, y, is_upside_down: bool, sprite):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.is_upside_down = is_upside_down
        self.image = sprite
        if is_upside_down:
            self.image = pg.transform.rotate(self.image, 180)
        self.passed = False
        self.height = self.y
        self.rect = self.image.get_rect(center=(self.x, self.y))

    # update function that updates the pipes position
    def update(self):
        self.rect.x -= 5


def load_resource(relative_path):
    return pg.image.load(os.path.join(
        os.path.dirname(__file__), relative_path)).convert()


def create_pipe_pair(x, y, sprite, ground_height):
    # create a pair of pipes with given gap between them
    # rotate the top pipe is upside down
    gap = 300
    r = random.randrange(-100, 300)
    pipe_gap = random.randint(100, 200)
    pipe_top = Pipe(x, 0 + r - gap/2, True, sprite)
    pipe_bottom = Pipe(x, y - ground_height + r + gap/2, False, sprite)
    return [pipe_top, pipe_bottom]


def main():

    # Initialize pygame
    pg.init()
    pg.font.init()
    pg.display.set_caption("Flappy Bird")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    bird_sprites = [
        pg.transform.scale2x(load_resource("res/bird1.png")),
        pg.transform.scale2x(load_resource("res/bird2.png")),
        pg.transform.scale2x(load_resource("res/bird3.png"))
    ]
    # load the other sprites and scale to fit the window
    pipe_sprite = pg.transform.scale2x(load_resource("res/pipe.png"))

    ground_sprite = pg.transform.scale(
        load_resource("res/base.png"), (WIDTH, 150))
    background_sprite = pg.transform.scale(
        load_resource("res/bg.png"), (WIDTH, HEIGHT))

    ground_height = ground_sprite.get_height()
    # create a bird object
    bird = Bird(50, int(HEIGHT/2), bird_sprites)

    # create a ground object
    ground = Ground(0, HEIGHT, ground_sprite)

    # create a list of pipes
    pipes: List[Pipe] = []

    for i in range(1, 5):
        top, bottom = create_pipe_pair(
            WIDTH + i*WIDTH/2, HEIGHT, pipe_sprite, ground_height)
        pipes.append(top)
        pipes.append(bottom)

    # create spritegroups for the sprites
    bird_group = pg.sprite.Group()
    bird_group.add(bird)
    pipe_group = pg.sprite.Group()
    pipe_group.add(*pipes)
    ground_group = pg.sprite.Group()
    ground_group.add(ground)

    # create a generall sprite group for all sprites
    all_sprites = pg.sprite.Group()
    all_sprites.add(bird)
    all_sprites.add(pipes)

    running = True
    has_added_pipe = False
    has_added_score = False
    while running:
        # tick fps
        clock.tick(FPS)
        # check for events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    bird.jump()

                if event.key == pg.K_ESCAPE:
                    running = False

        # update all sprites
        all_sprites.update()

        # check for collisions
        hits = pg.sprite.spritecollide(bird, pipe_group, False)
        if hits:
            running = False

        # check for collisions where the bird uses circle collision

        # check bird collision with ground
        hits = pg.sprite.spritecollide(bird, ground_group, False)
        if hits:
            running = False

        # check if bird has passed pipe
        for pipe in pipes:
            if pipe.rect.centerx < bird.rect.centerx and not pipe.passed:
                if not has_added_score:
                    bird.score += 1
                    has_added_score = True
                pipe.passed = True
            else:
                has_added_score = False

        # check if a pipe has left the window

        for pipe in pipes:
            if pipe.rect.x < -pipe.image.get_width():  # sketchy but works
                pipe.kill()
                pipes.remove(pipe)
                # generate a new pipe and add to pipes
                if not has_added_pipe:
                    new_pipes = create_pipe_pair(
                        4*WIDTH/2, HEIGHT, pipe_sprite, ground_height)
                    for p in new_pipes:
                        pipes.append(p)
                        pipe_group.add(p)
                        all_sprites.add(p)
                        has_added_pipe = True
                else:
                    has_added_pipe = False

        # draw all sprites
        screen.fill(BLACK)
        screen.blit(background_sprite, (0, 0))
        all_sprites.draw(screen)
        ground_group.draw(screen)

        # pygame get default font
        font = pg.font.SysFont("Arial", 30)
        text = font.render(str(bird.score), True, WHITE)
        screen.blit(text, (WIDTH/2, 50))

        pg.display.flip()

    pg.quit()


if __name__ == '__main__':
    main()
