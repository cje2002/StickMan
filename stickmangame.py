import time
from tkinter import *

import stickmanutils
from stickmanutils import within_x, within_y


def collided_left(co1, co2):
    if within_y(co1, co2):
        if co1.x1 <= co2.x2 and co1.x1 >= co2.x1:
            return True
    return False


def collided_right(co1, co2):
    if within_y(co1, co2):
        if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
            return True
    return False


def collided_top(co1, co2):
    if within_x(co1, co2):
        if co1.y1 <= co2.y2 and co1.y1 >= co2.y1:
            return True
    return False


def collided_bottom(y, co1, co2):
    if within_x(co1, co2):
        y_calc = co1.y2 + y
        if y_calc >= co2.y1 and y_calc <= co2.y2:
            return True
    return False

#################################################################################

class Sprite:
    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coordinates = None

    def move(self):
        pass

    def coords(self):
        return self.coordinates


#################################################################################

class PlatformSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
        self.coordinates = stickmanutils.Coords(x, y, x + width, y + height)

#################################################################################

class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Mr. Stick Man Races for the Exit")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=800, height=1000, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.canvas_height = 1000
        self.canvas_width = 800

        self.bg = PhotoImage(file="images/background.png")
        self.bg1 = PhotoImage(file="images/background1.png")
        w = self.bg.width()
        h = self.bg.height()

        for x in range(0, 8):
            for y in range(0, 10):
                if (x + y) % 2 == 0:
                    bgImage = self.bg
                else:
                    bgImage = self.bg1

                self.canvas.create_image(x * w, y * h, image=bgImage, anchor='nw')

        self.sprites = []
        self.running = True

    def mainloop(self):
        while 1:
            if self.running == True:
                for sprite in self.sprites:
                    sprite.move()
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)


#################################################################################
class StickFigureSprite(Sprite):

    FALLING_SPEED = 4
    MOVING_SPEED = 1.5

    def __init__(self, game):
        Sprite.__init__(self, game)
        self.images_left = [
            PhotoImage(file="images/figure-R1.gif"),
            PhotoImage(file="images/figure-R2.gif"),
            PhotoImage(file="images/figure-R3.gif")
        ]
        self.images_right = [
            PhotoImage(file="images/figure-R1.gif"),
            PhotoImage(file="images/figure-R2.gif"),
            PhotoImage(file="images/figure-R3.gif")
        ]
        self.image = game.canvas.create_image(200, 470, image=self.images_left[0], anchor='nw')
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

    def turn_right(self, evt):
        if self.y == 0:
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


#################################################################################


class DoorSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor='nw')
        self.coordinates = stickmanutils.Coords(x, y, x + (width / 2), y + height)
        self.endgame = True

#################################################################################

g = Game()


platform2 = PlatformSprite(g, PhotoImage(file="images/platform1.png"), 150, 950, 100, 10)
g.sprites.append(platform2)

platform3 = PlatformSprite(g, PhotoImage(file="images/platform1.png"), 300, 900, 100, 10)
g.sprites.append(platform3)

platform4 = PlatformSprite(g, PhotoImage(file="images/platform1.png"), 100, 700, 100, 10)
g.sprites.append(platform4)

platform6 = PlatformSprite(g, PhotoImage(file="images/platform1.png"), 600, 900, 100, 10)
g.sprites.append(platform6)

platform7 = PlatformSprite(g, PhotoImage(file="images/platform1.png"), 450, 850, 100, 10)
g.sprites.append(platform7)

platform8 = PlatformSprite(g, PhotoImage(file="images/platform1.png"), 200, 50, 100, 10)
g.sprites.append(platform8)

platform9 = PlatformSprite(g, PhotoImage(file="images/platform1.png"), 50, 100, 100, 10)
g.sprites.append(platform9)

door = DoorSprite(g, PhotoImage(file="images/door_closed.png"), 45, 30, 40, 35)
g.sprites.append(door)
sf = StickFigureSprite(g)
g.sprites.append(sf)
g.mainloop()