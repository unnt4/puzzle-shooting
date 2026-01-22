import pyxel
import random
import math
from bullet import Bullet
from beam import Beam



class Player:
    def __init__(self,sw, x, y, margin_x, margin_y,screen_height):
        pyxel.load('player.pyxres')
        self.img = pyxel.Image(50, 200)
        self.img.load(x=0, y=0, filename="player_img/1011010501.png")
        self.img2 = pyxel.Image(11, 17)
        self.img2.load(x=0, y=0, filename="player_img/hinotama_orange (1).png")
        self.img3 = pyxel.Image(32, 32)
        self.img3.load(x=0, y=0, filename="player_img/shot02.png")
        self.img4 = pyxel.Image(32, 32)
        self.img4.load(x=0, y=0, filename="player_img/援護ビーム.png")
        self.img14 = pyxel.Image(90, 16)
        self.img14.load(x=0, y=0, filename="player_img/援護ビーム大 (2).png")
        self.img5 = pyxel.Image(30, 30)
        self.img5.load(x=0, y=0, filename="player_img/自機玉.png")
        self.img52 = pyxel.Image(128, 128)
        self.img52.load(x=0, y=0, filename="player_img/ボス弾緑.png")

        self.img6 = pyxel.Image(46, 39)
        self.img6.load(x=0, y=0, filename="player_img/mark_heart_red (1).png")

       
        
        
        
        
        self.screen_width=sw
        self.x = x
        self.y = y
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.screean_height=screen_height
        self.bullets = []
        self.beams = []
        
                    #威力　　　　　玉レベル　　　　　　　援護
        self.state=[0           ,0             ,0        ]
        self.statecolor = [[0,7,7,7,7,7,7,7], [0,7,7,7,7,7,7,7], [0,7,7,7,7,7,7,7]]
        self.kankaku=50
        self.tamairyoku=1
        self.engo=1                     #援護
        self.speed=2
        self.tugge_timer=0
     
        
        
        self.zanki=3
        self.muteki_timer=0
        self.huyasu_timer=0



        self.angle = 0  # 初期角度
        self.kaitenspeed = 0.02  # 回転速度
        self.radius = 50  # 回転の半径
        self.img_x=0
        self.img_y=0



        self.beam=True


        self.ally_positions = [(self.x, self.y)] * 7
        

        # 画像の新しい座標計算
        

    def update(self,boss_x,boss_y):


        self.angle += self.kaitenspeed


        # 玉レベル2でさらに速く
        if self.state[1] == 3:
            self.kankaku = 30  # 玉レベル3でさらに速く
        elif self.state[1]==4:
            self.kankaku =10
        

        angle_diff = (2 * math.pi) / max(1, self.state[2])

        for i in range(self.state[2]):
        # 各味方のための角度を計算
            ally_angle = self.angle + i * angle_diff
            ally_x = self.x + self.radius * math.cos(ally_angle)
            ally_y = self.y + self.radius * math.sin(ally_angle)
        
        # 味方の位置を保存
            self.ally_positions[i] = (ally_x, ally_y)

        if self.muteki_timer > 0:
            self.muteki_timer -= 1
        
        if self.tugge_timer > 0:
            self.tamairyoku=2
            self.tugge_timer -= 1
        else:
            self.tamairyoku=1
        # プレイヤーの入力と移動を処理
        if pyxel.btn(pyxel.KEY_LEFT):
                if self.margin_x<self.x:
                    self.x -= self.speed


        if pyxel.btn(pyxel.KEY_UP):
                if self.margin_y<self.y:
                    self.y -= self.speed


        if pyxel.btn(pyxel.KEY_DOWN):
            if self.screean_height-30>self.y:
                self.y += self.speed

        if pyxel.btn(pyxel.KEY_RIGHT):
            if (self.screen_width-self.margin_x+190)>self.x:
                self.x += self.speed

        if pyxel.btn(pyxel.KEY_M):
            self.muteki_timer=200000

        
        if pyxel.btn(pyxel.KEY_1):
            if pyxel.frame_count % 50== 0:
                if self.state[0]<=5:
                    self.state[0]+=1
                    self.statecolor[0][self.state[0]]=0

        if pyxel.btn(pyxel.KEY_2):
            if pyxel.frame_count % 50== 0:
                if self.state[1]<=5:
                    self.state[1]+=1
                    self.statecolor[1][self.state[1]]=0
                
            
        
        if pyxel.btn(pyxel.KEY_3):
            if pyxel.frame_count % 50== 0:
                if self.state[2]<=5:
                    self.state[2]+=1
                    
                    self.statecolor[2][self.state[2]] = 0
            
            

        # 弾の発射間隔
        if pyxel.frame_count % self.kankaku== 0:
            self.shoot()

        # 弾の更新
        for bullet in self.bullets:
            
           
            bullet.update2(self.x)
           

        # 画面外の弾を削除
        self.bullets = [bullet for bullet in self.bullets if bullet.is_on_screen()]

    def shoot(self):
        # 弾を発射
        if self.state[1]==0:
            
            self.bullets.append(Bullet(self.x, self.y-30, self.img3, dy=-1,damage=self.state[1]+1))
        elif self.state[1]==1:
            self.bullets.append(Bullet(self.x + 16, self.y-30,self.img3, dy=-1,damage=self.state[1]+1))

            self.bullets.append(Bullet(self.x-16, self.y-30, self.img3, dy=-1,damage=self.state[1]+1))
        elif self.state[1]==2:
            self.bullets.append(Bullet(self.x, self.y-30, self.img3,dx=0.25, dy=-1,damage=self.state[1]+1))
            self.bullets.append(Bullet(self.x, self.y-30, self.img3,dx=-0.25, dy=-1,damage=self.state[1]+1))
            self.bullets.append(Bullet(self.x + 10, self.y-30,self.img3, dy=-1,damage=self.state[1]+1))
            self.bullets.append(Bullet(self.x, self.y-30, self.img3, dy=-1,damage=self.state[1]+1))
            self.bullets.append(Bullet(self.x-10, self.y-30, self.img3, dy=-1,damage=self.state[1]+1))
        
        elif self.state[1]==3:
            self.bullets.append(Bullet(self.x, self.y-30, self.img3,dx=0.25, dy=-1,damage=self.state[1]+1))
            self.bullets.append(Bullet(self.x, self.y-30, self.img3,dx=-0.25, dy=-1,damage=self.state[1]+1))
            self.bullets.append(Bullet(self.x + 10, self.y-30,self.img3, dy=-1,damage=self.state[1]+1))
            self.bullets.append(Bullet(self.x, self.y-30, self.img3, dy=-1,damage=self.state[1]+1))
            self.bullets.append(Bullet(self.x-10, self.y-30, self.img3, dy=-1,damage=self.state[1]+1))
            
           
        
        elif self.state[1]==4:
            self.bullets.append(Bullet(self.x-15, self.y, self.img4, dy=-1,damage=self.state[1]+2,gaiz=True))
            
        
        elif self.state[1]==5:
            self.bullets.append(Bullet(self.x-16, self.y-20, self.img4, dy=-1,damage=self.state[1]+2,gaiz=True))
            self.bullets.append(Bullet(self.x+16, self.y-20, self.img4, dy=-1,damage=self.state[1]+2,chaiz=True))


        elif self.state[1]==6:
           self.bullets.append(Bullet(self.x+16, self.y-20, self.img14, dy=-1,damage=self.state[1]+6,gaiz=True))
        
           
           
       
           
        
        

        if self.state[2] > 0:
            for ally_x, ally_y in self.ally_positions[:self.state[2]]:
                self.bullets.append(Bullet(ally_x, ally_y, self.img5, dy=-2,damage=3))

           


        
        

    def draw(self):
        # プレイヤーを描画
        if self.muteki_timer > 0:
            
            pyxel.blt(self.x-self.img52.width/2, self.y-self.img52.height/2, self.img52, 0, 0, self.img52.width, self.img52.height,7)
        pyxel.blt(self.x-self.img.width/2, 75+self.y-self.img.height/2, self.img, 0, 148, self.img.width, self.img.height,7)
        
        
        if self.state[2] > 0:
            for ally_x, ally_y in self.ally_positions[:self.state[2]]:
                pyxel.blt(ally_x, ally_y, self.img2, 0, 0, self.img2.width, self.img2.height, 0)

        pyxel.rect(0, 0, 250, 800, 2)
        pyxel.rect(self.x-4, self.y-4, 8, 8, 0)
        # 弾を描画
        for bullet in self.bullets:
            bullet.draw()


        
        zahyou=10
        for  i in range(7):
            pyxel.circ(zahyou, 180, 8, self.statecolor[0][i])
            pyxel.circ(zahyou, 230, 8, self.statecolor[1][i])
            pyxel.circ(zahyou, 280, 8, self.statecolor[2][i])
            zahyou+=30



        zankizahyou=80
        for  j in range(self.zanki):
            pyxel.blt(zankizahyou, 605, self.img6, 0, 0, self.img6.width, self.img6.height,0)
            zankizahyou+=50
        


    def randoma(self):
        r = random.randint(0, 2)
        if self.state[r] <= 5:
            self.state[r] += 1
            self.statecolor[r][self.state[r]] = 0
        else:
            # 5を超えた要素を別の要素に割り当てる
            available_indices = [i for i in range(3) if self.state[i] <= 5]
            if available_indices:
                other_r = random.choice(available_indices)
                self.state[other_r] += 1
                self.statecolor[other_r][self.state[other_r]] = 0




