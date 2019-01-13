import time
from tkinter import PhotoImage

import stickmanutils
from stickmanutils import collided_left, collided_right, collided_top, collided_bottom
from sprites import Sprite, BouncerSprite


class StickFigureSprite(Sprite):

    FALLING_SPEED = 3
    MOVING_SPEED = 1.5
    INITIAL_STICKMAN_X = 0
    INITIAL_STICKMAN_Y = 950

    def __init__(self, game):
        Sprite.__init__(self, game)
        self.images_left = [
            PhotoImage(file="images/figure-L1.gif"),
            PhotoImage(file="images/figure-L2.gif"),
            PhotoImage(file="images/figure-L3.gif")
        ]
        self.images_right = [
            PhotoImage(file="images/figure-R1.gif"),
            PhotoImage(file="images/figure-R2.gif"),
            PhotoImage(file="images/figure-R3.gif")
        ]
        self.image = game.canvas.create_image(self.INITIAL_STICKMAN_X, self.INITIAL_STICKMAN_Y, image=self.images_left[0], anchor='nw')
        self.x = -0.5
        self.y = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = stickmanutils.Coords()

        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)

    def turn_left(self, evt):
        if self.y == 0:
            self.x = -1 * self.MOVING_SPEED
        else:
            self.x = -1 * self.MOVING_SPEED

    def turn_right(self, evt):
        if self.y == 0:
            self.x = self.MOVING_SPEED
        else:
            self.x = self.MOVING_SPEED

    def jump(self, evt):
        if self.y == 0:
            self.y = -1 * self.FALLING_SPEED
            self.jump_count = 0

    def animate(self):
        if self.x != 0 and self.y == 0:
            if time.time() - self.last_time > 0.1:
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image >= 2:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
        if self.x < 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.images_left[2])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_left[self.current_image])
        elif self.x > 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.images_right[2])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_right[self.current_image])

    def coords(self):

        if not self.game.running:
            return

        xy = list(self.game.canvas.coords(self.image))
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + 27
        self.coordinates.y2 = xy[1] + 30
        return self.coordinates

    def move(self):
        self.animate()
        if self.y < 0:
            self.jump_count += 1
            if self.jump_count > 20:
                self.y = self.FALLING_SPEED
        if self.y > 0:
            self.jump_count -= 1

        co = self.coords()
        left = True
        right = True
        top = True
        bottom = True
        falling = True

        if self.y > 0 and co.y2 >= self.game.canvas_height:
            self.y = 0
            bottom = False
        elif self.y < 0 and co.y1 <= 0:
            self.y = 0
            top = False

        if self.x > 0 and co.x2 >= self.game.canvas_width:
            self.x = 0
            right = False
        elif self.x < 0 and co.x1 <= 0:
            self.x = 0
            left = False

        for sprite in self.game.sprites:
            if sprite == self:
                continue

            sprite_co = sprite.coords()
            if top and self.y < 0 and collided_top(co, sprite_co):
                self.y = -self.y
                top = False

            if bottom and self.y > 0 and collided_bottom(self.y, co, sprite_co):

                if isinstance(sprite, BouncerSprite):
                    self.y = self.y - 10
                    self.jump_count = self.jump_count + 1
                    falling = True
                else:
                    self.y = sprite_co.y1 - co.y2

                    if self.y < 0:
                        self.y = 0
                    bottom = False
                    top = False

            if bottom and falling and self.y == 0 and co.y2 < self.game.canvas_height and collided_bottom(1, co, sprite_co):
                falling = False

            if left and self.x < 0 and collided_left(co, sprite_co):
                self.x = 0
                left = False
                if sprite.endgame:
                    self.game.running = False

            if right and self.x > 0 and collided_right(co, sprite_co):
                self.x = 0
                right = False
                if sprite.endgame:
                    self.game.running = False

        if falling and bottom and self.y == 0 and co.y2 < self.game.canvas_height:
            self.y = self.FALLING_SPEED

        self.game.canvas.move(self.image, self.x, self.y)