import pyxel
import random
class Bullet:
    def __init__(self, x, y, img, dx=0, dy=-4,damage=1,gaiz=False,chaiz=False,bunretu=False):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.w=img.width/2
        self.h=img.height/2
       
        self.damage=damage
        self.img = img
        self.gaiz=gaiz
        self.chaiz=chaiz
        if self.gaiz:
            self.w=img.width
        self.bunretu=bunretu
        self.bunnretutaim=0
        if bunretu:
            self.bunnretutaim=random.uniform(300, 600)

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def update2(self,player_x):
        if self.gaiz:
            self.x=player_x-4
            
        elif self.chaiz:
            self.x=player_x+16
            
            
        else:
            self.x += self.dx
        self.y += self.dy
        

        


    
    

    
        

    def draw(self):
        
        pyxel.rect(self.x, self.y, 2, 2, 7)
        
        
       
        pyxel.blt(self.x-self.w/2, self.y-self.h/2, self.img, 0, 0, self.img.width, self.img.height,0)

    
    
            

    def is_on_screen(self):
        return 0 <= self.x <= pyxel.width and 0 <= self.y <= pyxel.height