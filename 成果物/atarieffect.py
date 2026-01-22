import pyxel

class Effect:
    def __init__(self, x, y,gaiz=False):
        self.img = pyxel.Image(32, 32)
        self.img.load(x=0, y=0, filename="effect/kougeki.png")
        self.img2=pyxel.Image(32, 32)
        self.img2.load(x=0, y=0, filename="effect/kemuri_gray (1).png")
        self.x = x
        self.y = y
        self.framecount=30
        self.bosskill=gaiz
        if self.bosskill:
            self.img = pyxel.Image(64, 64)
            self.img.load(x=0, y=0, filename="effect/bakuhatsu_01大.png")
            self.img2=pyxel.Image(64, 64)
            self.img2.load(x=0, y=0, filename="effect/kemuri_01大.png")



        

    def draw(self):
        self.framecount-=1
        if self.framecount>=15:
            pyxel.blt(self.x-self.img.width/2, self.y-self.img.height/2, self.img, 0, 0, self.img.width, self.img.height,0)
        else :
            pyxel.blt(self.x-self.img.width/2, self.y-self.img.height/2, self.img2, 0, 0, self.img.width, self.img.height,0)

    