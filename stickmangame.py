from tkinter import *

from game import Game
from sprites import PlatformSprite, BouncerSprite, DoorSprite
from stickfiguresprite import StickFigureSprite

#################################################################################


g = Game()


platform2 = PlatformSprite(g, PhotoImage(file="images/platform1.png"), 100, 950, 100, 10)
g.sprites.append(platform2)

platform3 = BouncerSprite(g, PhotoImage(file="images/bouncer1.png"), 200, 900, 100, 10)
g.sprites.append(platform3)

#platform4 = PlatformSprite(g, PhotoImage(file="images/platform1.png"), 100, 850, 100, 10)
#g.sprites.append(platform4)

platform6 = PlatformSprite(g, PhotoImage(file="images/platform1.png"), 50, 800, 100, 10)
g.sprites.append(platform6)

#platform8 = PlatformSprite(g, PhotoImage(file="images/platform1.png"), 200, 700, 100, 10)
#g.sprites.append(platform8)

platform9 = PlatformSprite(g, PhotoImage(file="images/platform1.png"), 350, 700, 100, 10)
g.sprites.append(platform9)

platform10 = BouncerSprite(g, PhotoImage(file="images/bouncer1.png"), 500, 700, 100, 10)
g.sprites.append(platform10)

#platform11 = PlatformSprite(g, PhotoImage(file="images/platform1.png"), 300, 900, 100, 10)
#g.sprites.append(platform11)

#platform12 = PlatformSprite(g, PhotoImage(file="images/platform1.png"), 200, 700, 100, 10)
#g.sprites.append(platform12)

#platform13 = PlatformSprite(g, PhotoImage(file="images/platform1.png"), 600, 800, 100, 10)
#g.sprites.append(platform13)

#platform14 = PlatformSprite(g, PhotoImage(file="images/platform1.png"), 450, 850, 100, 10)
#g.sprites.append(platform14)

#platform15 = PlatformSprite(g, PhotoImage(file="images/platform1.png"), 200, 50, 100, 10)
#g.sprites.append(platform15)

#platform16 = PlatformSprite(g, PhotoImage(file="images/platform1.png"), 50, 100, 100, 10)
#g.sprites.append(platform16)
door = DoorSprite(g, PhotoImage(file="images/door_closed.png"), 600, 820, 40, 35)
g.sprites.append(door)
sf = StickFigureSprite(g)
g.sprites.append(sf)
g.mainloop()
