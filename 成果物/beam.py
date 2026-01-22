import pyxel

class Beam:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.w = 1
        self.h = 1
        self.img = img
        self.i=0
        
    def draw(self,player_x,player_y):
        
        pyxel.rect(self.x, self.y, 2, 2, 7)
        
        self.w=self.img.width/2
        self.h=self.img.height/2

        
       
        pyxel.blt(player_x-self.img.width/2, player_y-self.i, self.img, 0, 0, self.img.width, self.i,0)
        if self.i<700:
            self.i+=4

    
    