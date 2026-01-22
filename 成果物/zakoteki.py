import pyxel
import random
import math
from bullet import Bullet

class Zakoteki:
    def __init__(self, x, y, stage,gorudo=False):
        self.img = pyxel.Image(42, 31)
        self.img.load(x=0, y=0, filename="zakoteki/1zakoteki.png")
        if stage == 2:
            self.img = pyxel.Image(60, 60)
            self.img.load(x=0, y=0, filename="zakoteki/2zakoteki.png")
        
        if stage == 3:
            self.img = pyxel.Image(70, 82)
            self.img.load(x=0, y=0, filename="zakoteki/3zakoteki.png")
        
        if stage == 4:
            self.img = pyxel.Image(190, 178)
            self.img.load(x=0, y=0, filename="zakoteki/4zakoteki.png")

        self.img2 = pyxel.Image(32, 32)
        self.img2.load(x=0, y=0, filename="zakoteki/bakuhatsu_01 (1).png")
        self.img3 = pyxel.Image(32, 32)
        self.img3.load(x=0, y=0, filename="zakoteki/kemuri_gray (1).png")

        self.img4 = pyxel.Image(32, 30)
        self.img4.load(x=0, y=0, filename="zakoteki/ボス弾赤.png")

        if gorudo:
            self.img = pyxel.Image(40, 40)
            self.img.load(x=0, y=0, filename="zakoteki/ゴルドー.jpg")
        

        self.gorudo=gorudo
        
        self.zakotekiframe = 200
        self.stage = stage
        self.x = x
        self.y = y
        self.w = self.img.width
        self.h = self.img.height
        self.sinda = False
        self.bulletx = x
        self.bullety = y
        self.hp = 3
        if stage == 4:
            self.hp = 100
        if self.gorudo:
            self.stage=1
            self.hp=90000
        self.direction = random.uniform(0.3, 2)
        self.directiony = random.uniform(0.3, 2)
        self.bullets = []
        self.hit_timer = 0
        self.kankaku = 200
        self.gaizi=True

    def update(self, player_x, player_y):
        if self.stage == 2:
            self.kankaku = 300
        elif self.stage == 3:
            self.kankaku = 30  # 玉レベル3でさらに速く
        elif self.stage == 4:
            self.kankaku = 300

        if self.hit_timer > 0:
            self.hit_timer -= 1
        if self.stage <= 2:
            self.y += 1

        elif self.stage == 3:
            self.y += 1
            speed = 0.4  # You can adjust the speed value to make it faster/slower
            if self.x < player_x:
                self.x += speed
            elif self.x > player_x:
                self.x -= speed

        elif self.stage == 4:
            if self.y<100:
                self.y += 1
            


            

        if self.sinda:
            self.zakotekiframe -= 1
            self.direction = 0
            self.directiony = 0

        if pyxel.frame_count % self.kankaku == 0 and not self.gorudo:
            self.shoot(player_x, player_y)

        for bullet in self.bullets:
            bullet.update()
        self.bullets = [bullet for bullet in self.bullets if bullet.is_on_screen()]

    def draw(self):
        # ボスを描画
        if self.hit_timer > 0:
            pyxel.rect(self.x - self.w / 2, self.y - self.h / 2, self.w, self.h, 7)
        else:
            pyxel.blt(self.x - self.img.width / 2, self.y - self.img.height / 2, self.img, 0, 0, self.img.width, self.img.height, 8)
        
        # 弾を描画
        for bullet in self.bullets:
            bullet.draw()

    def shoot(self, player_x, player_y):
        if self.stage == 1:
            self.bullets.append(Bullet(self.x, self.y, self.img4, 0, 2))

        if self.stage == 2:
            num_bullets = 8  # 放つ弾の数
            speed = 1  # 弾の速度（任意の値で調整可能）
        
            for i in range(num_bullets):
                angle = math.radians(i * (360 / num_bullets))  # 360度を弾の数で割った角度
                dx = math.cos(angle) * speed
                dy = math.sin(angle) * speed
                self.bullets.append(Bullet(self.x, self.y, self.img4, dx, dy))
        
        elif self.stage == 4 and self.gaizi:
            # 分裂弾の実装
            num_bullets = 5  # 初期弾の数
            split_angle = 30  # 分裂時の角度
            speed = 1.5  # 初期弾の速度

            for i in range(num_bullets):
                angle = math.radians(i * (360 / num_bullets))
                dx = math.cos(angle) * speed
                dy = math.sin(angle) * speed
                bullet = Bullet(self.x, self.y, self.img4, dx, dy)
                self.bullets.append(bullet)

                # 分裂弾を追加
                for j in range(-1, 2, 2):  # -1と1で分裂
                    split_dx = math.cos(angle + math.radians(j * split_angle)) * speed
                    split_dy = math.sin(angle + math.radians(j * split_angle)) * speed
                    self.bullets.append(Bullet(self.x, self.y, self.img4, split_dx, split_dy))