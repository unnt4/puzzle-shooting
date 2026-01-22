import pyxel
import math
from bullet import Bullet
import random
class Boss:
    def __init__(self, x, y,w,h, hp,stage):
        
        self.img = pyxel.Image(112, 127)
        self.img.load(x=0, y=0, filename="boss_img/ボス赤.png")
        self.img2 =pyxel.Image(32, 32)
        self.img2.load(x=0, y=0, filename="boss_img/ボス弾.png")
        self.img3 =pyxel.Image(32, 30)
        self.img3.load(x=0, y=0, filename="boss_img/ボス弾赤.png")
        self.img4 =pyxel.Image(29, 29)
        self.img4.load(x=0, y=0, filename="boss_img/ボス弾緑.png")
        self.img5 =pyxel.Image(8, 9)
        self.img5.load(x=0, y=0, filename="boss_img/ボス弾緑小.png")
        self.img6 =pyxel.Image(8, 8)
        self.img6.load(x=0, y=0, filename="boss_img/ボス弾赤小.png")


        self.img7 =pyxel.Image(19, 19)
        self.img7.load(x=0, y=0, filename="boss_img/ボス弾赤中.png")
        self.img8 =pyxel.Image(19, 19)
        self.img8.load(x=0, y=0, filename="boss_img/ボス弾緑中.png")
        self.img9 =pyxel.Image(19, 19)
        self.img9.load(x=0, y=0, filename="boss_img/ボス弾青中.png")


        self.deru=True
       
        
        


        self.stage=stage
        self.bosstouka=8                    #####画像透過用
        if stage==2:
            self.img = pyxel.Image(240, 240)
            self.img.load(x=0, y=0, filename="boss_img/ブイ破壊.png")
            self.bosstouka=0
        
        if stage==3:
            self.img = pyxel.Image(250, 253)
            self.img.load(x=0, y=0, filename="boss_img/finalboss.png")
            self.bosstouka=0
        
        if stage==4:
            self.img = pyxel.Image(416,278)
            self.img.load(x=0, y=0, filename="boss_img/ですかお.jpg")
            self.bosstouka=7
        
        if stage==14:
            self.img = pyxel.Image(146, 146)
            self.img.load(x=0, y=0, filename="boss_img/ですひだり.jpg")
            self.bosstouka=7
        
        if stage==24:
            self.img = pyxel.Image(146, 146)
            self.img.load(x=0, y=0, filename="boss_img/ですみぎ.jpg")
            self.bosstouka=7
        
        self.stage=stage
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.bulletx = x
        self.bullety = y
        self.hp = hp
        self.direction = 1
        self.directiony = 1
        self.bullets = []
        self.hit_timer = 0
        self.kankaku=50

    

        self.syometu=800

        self.bosshpx=self.hp/500
        

    def update(self, player_x,player_y):
        if self.stage==2:
            self.kankaku=40
        elif self.stage == 3:
            self.kankaku = 30  
        elif self.stage==4:
            self.kankaku =30
        if self.hit_timer > 0:
            self.hit_timer -= 1
        if self.hp>0:
            if self.y<900:
                if self.stage==1:# ボスの移動
                    self.x += self.direction * 1
                    if self.x <= 300 or self.x + self.w >=800:
                        self.direction *= -1  # 方向を反転
            
            # ボスの移動
                if self.stage==14 or self.stage==24:
                    self.y += self.directiony * 1
                    if self.y <=200  or self.y >=203:
                        self.directiony *= -1  # 方向を反転

        
        # ボスの移動
                #self.bulletx += self.direction * 2
                #if self.bulletx <= 0 or self.bulletx + self.w >= pyxel.width:
                 #   self.direction *= -1  # 方向を反転
        
        

        # 弾の発射ロジック
        if self.hp>0 and self.deru:
            if pyxel.frame_count % self.kankaku== 0:
                self.shoot(player_x,player_y)

        # 弾の更新
        bullets_to_remove = set()
        for bullet in self.bullets:
            if bullet.bunretu and bullet.y > bullet.bunnretutaim:
                
                num_bullets = 5  # 放つ弾の数
                speed = 1  # 弾の速度（任意の値で調整可能）

                for i in range(num_bullets):
                    angle = math.radians(i * (360 / num_bullets))  # 360度を弾の数で割った角度
                    dx = math.cos(angle) * speed
                    dy = math.sin(angle) * speed
                    self.bullets.append(Bullet(bullet.x ,bullet.y, self.img7,dx,dy))
                
                bullets_to_remove.add(bullet)
                

            else:
                bullet.update()
        self.bullets = [bullet for bullet in self.bullets if bullet.is_on_screen()]
        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)

    def shoot(self, player_x,player_y):
        if self.stage==1:
            if pyxel.frame_count %  100== 0:
                self.zikinerai(player_x,player_y)
        
        elif self.stage==2:
            if pyxel.frame_count %  500== 0:
                for i in range(-1, 5):
                    self.bullets.append(Bullet(self.x ,self.y, self.img2,(i-2)*0.2,1))
        
        elif self.stage==12 or self.stage==14:
            if pyxel.frame_count %  100== 0:
                self.zikinerai(player_x,player_y)
            
        
        elif self.stage==22 :
            if pyxel.frame_count %  20== 0:
                
                self.bullets.append(Bullet(self.x ,self.y, self.img2,random.uniform(-2, 2),random.uniform(0.2, 0.5)))
        

        elif self.stage==3  :
           if pyxel.frame_count %  50== 0:
                num_bullets = 5  # 放つ弾の数
                speed = 1  # 弾の速度（任意の値で調整可能）

                for i in range(num_bullets):
                    angle = math.radians(i * (180 / num_bullets))  # 360度を弾の数で割った角度
                    dx = math.cos(angle) * speed
                    dy = math.sin(angle) * speed
                    self.bullets.append(Bullet(self.x, self.y, self.img4, dx, dy,bunretu=True))
        
        elif self.stage==24 :
            if pyxel.frame_count %  200== 0:
                num_bullets = 5  # 放つ弾の数
                speed = 1  # 弾の速度（任意の値で調整可能）

                for i in range(num_bullets):
                    angle = math.radians(i * (180 / num_bullets))  # 360度を弾の数で割った角度
                    dx = math.cos(angle) * speed
                    dy = math.sin(angle) * speed
                    self.bullets.append(Bullet(self.x, self.y, self.img4, dx, dy,bunretu=True))

        elif  self.stage==4:
            if pyxel.frame_count %  100== 0:
                for i in range(-1, 2):
                    self.bullets.append(Bullet(self.x ,self.y, self.img2,random.uniform(-2, 2),random.uniform(0.2, 1.5)))
                    self.bullets.append(Bullet(self.x ,self.y, self.img3,random.uniform(-2, 2),random.uniform(0.2, 1.5)))
                    self.bullets.append(Bullet(self.x ,self.y, self.img4,random.uniform(-2, 2),random.uniform(0.2, 1.5)))
                    self.bullets.append(Bullet(self.x ,self.y, self.img5,random.uniform(-2, 2),random.uniform(0.2, 1.5)))
                    self.bullets.append(Bullet(self.x ,self.y, self.img6,random.uniform(-2, 2),random.uniform(0.2, 1.5)))
                    self.bullets.append(Bullet(self.x ,self.y, self.img7,random.uniform(-2, 2),random.uniform(0.2, 1.5)))
                    self.bullets.append(Bullet(self.x ,self.y, self.img8,random.uniform(-2, 2),random.uniform(0.2, 1.5)))
                    self.bullets.append(Bullet(self.x ,self.y, self.img9,random.uniform(-2, 2),random.uniform(0.2, 1.5)))

       

    def draw(self):
        # ボスを描画
        if self.y<500 and (self.stage==1 or self.stage==2 or self.stage==3 or self.stage==4):
            pyxel.rect(300, 30, self.hp/self.bosshpx, 10, 4)
        
            
            # ヒット時は白色
            
            
       
            
            # 通常時の色
        if self.stage<10:
            pyxel.blt(self.x-self.img.width/2, self.y-self.img.height/2, self.img, 0, 0, self.img.width, self.img.height,self.bosstouka)
        
        if self.stage==14:
            pyxel.blt(self.x-self.img.width/2, self.y-self.img.height/2, self.img, 0, 0, self.img.width, self.img.height,self.bosstouka)
        
        if self.stage==24:
            pyxel.blt(self.x-self.img.width/2, self.y-self.img.height/2, self.img, 0, 0, self.img.width, self.img.height,self.bosstouka)
        # 弾を描画
        if self.hit_timer > 0  :
            pyxel.rect(self.x-self.w/2, self.y-self.h/2, self.w, self.h, 7)  

         
        for bullet in self.bullets:
            bullet.draw()

    def zikinerai(self,player_x,player_y):
            gx = player_x - self.x
            gy = player_y - self.y
            magnitude = math.sqrt(gx ** 2 + gy ** 2)

            if magnitude != 0:
                gx /= magnitude
                gy /= magnitude
            else:
                gx, gy = 0, 0

        
            speed = 1.0  # 弾の速度を設定

        
            gx *= speed  # 弾の移動成分を計算
            gy *= speed
            
            for i in range(-1, 3):# ボスのgを発射
                dx =   i * 0.02
                ##self.bullets.append(Bullet(  self.bulletx + self.w // 2,                self.bullety + self.h,               dx=dx,               dy=0.5           ))
                self.bullets.append(Bullet(
                    self.x,
                    self.y,
                    self.img2,
                    gx,
                    gy
                ))
            dx = (player_x - (self.bulletx + self.w // 2)) / 100
            self.bullets.append(Bullet(self.bulletx + self.w // 2,self.bullety + self.h,self.img2, dx=dx,dy=0.5
        ))    
   