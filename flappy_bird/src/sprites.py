import pygame as pg


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
