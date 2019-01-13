import time
from tkinter import Tk, Canvas, PhotoImage

NUM_UP_DOWN_BACKGROUND_TILES = 10
NUM_LEFT_RIGHT_BACKGROUND_TILES = 8

CANVAS_HEIGHT = 1000
CANVAS_WIDTH = 800


class Game:

    def on_closing(self):
        self.running = False

    def __init__(self):
        self.window = Tk()
        self.window.title("Mr. Stick Man Races for the Exit")
        self.window.resizable(0, 0)
        self.window.wm_attributes("-topmost", 1)

        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.canvas = Canvas(self.window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, highlightthickness=0)
        self.canvas.pack()

        self.window.update()

        self.canvas_height = CANVAS_HEIGHT
        self.canvas_width = CANVAS_WIDTH

        self.bg_tile_image = PhotoImage(file="images/background.png")
        self.alt_bg_tile_image = PhotoImage(file="images/background1.png")

        bg_tile_width = self.bg_tile_image.width()
        bg_tile_height = self.bg_tile_image.height()

        for x in range(0, NUM_LEFT_RIGHT_BACKGROUND_TILES):
            for y in range(0, NUM_UP_DOWN_BACKGROUND_TILES):
                if (x + y) % 2 == 0:
                    background = self.bg_tile_image
                else:
                    background = self.alt_bg_tile_image

                self.canvas.create_image(x * bg_tile_width, y * bg_tile_height, image=background, anchor='nw')

        self.sprites = []
        self.running = True

    def mainloop(self):

        while 1:
            if self.running:
                for sprite in self.sprites:
                    sprite.move()
                self.window.update_idletasks()
                self.window.update()
                time.sleep(0.005)
