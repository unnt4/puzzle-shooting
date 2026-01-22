# main.py
import random
import pyxel
import sys

import PyxelUniversalFont as puf

from stage import Stage

from player import Player
from boss import Boss
from zakoteki import Zakoteki
from grid import Grid
from atarieffect import Effect

class App:
    def __init__(self):
        # 初期設定
        self.writer = puf.Writer("misaki_gothic2.ttf")
        self.screen_width = 900
        self.screen_height = 700
        pyxel.init(self.screen_width, self.screen_height, title="GAME01", fps=160)
        
        # ゲームの状態管理 stage_selectとかmain_gameとか
        self.state = 'stage_select'  

        
        self.stage = Stage()

        
        self.game_initialized = False
        
       
        self.paused = False
        
        # Pyxelの実行開始
        pyxel.run(self.update, self.draw)
        
    def reset_game(self,stage):
        
        print(sys.version)
        self.bombimg = pyxel.Image(46, 39)
        self.bombimg.load(x=0, y=0, filename="player_img/bakudan.png")
        # 画像の読み込み

        self.bosshp=1000
        self.img = pyxel.Image(800, 700)
        self.img2 = pyxel.Image(152, 112)
        self.stagec=stage
        
        self.img.load(x=0, y=0, filename="backgroundimage/yosuga.jpeg")
        if stage==2:
            self.bosshp=2000
            self.img.load(x=0, y=0, filename="backgroundimage/カビ.png")
        
        if stage==3:
            self.bosshp=6000
            self.img.load(x=0, y=0, filename="backgroundimage/宇宙 - コピー.png")


        if stage==4:
            self.bosshp=8000
            self.img.load(x=0, y=0, filename="backgroundimage/宇宙.png")
        
        self.img2.load(x=0, y=0, filename="backgroundimage/雲.png")
        
        self.Bosses=[]

        self.zakotekispown=0
        self.zakotekiborder=8000
        # グリッドの設定
        self.grid_size = 6
        self.cell_size = 53
        self.margin_x = (self.screen_width - self.grid_size * self.cell_size+200) // 2
        self.margin_y = self.screen_height - self.grid_size * self.cell_size

        self.forstage=False

        # クラスの初期化 
        self.player = Player(self.screen_width, self.margin_x, self.margin_y, self.margin_x, self.margin_y, self.screen_height)
        #ボスの種類
        if stage==1:
            self.zakotekispown=200
            self.Bosses.append(Boss(300, 1060,50,50, 1000,stage))
        elif stage==2:
            self.zakotekispown=300
            self.Bosses.append(Boss(500, 1030,30,30, self.bosshp,stage))
            self.Bosses.append(Boss(470, 1060,50,50, 500,stage+10))
            self.Bosses.append(Boss(535, 1060,50,50, 500,stage+20))
        
        elif stage==3:
            self.zakotekispown=100
            self.Bosses.append(Boss(500, 1030,100,100, self.bosshp,stage))
        
        elif stage==4:
            self.forstage=True
            self.zakotekiborder=12000
            self.zakotekispown=2000
            self.Bosses.append(Boss(500, 1030,100,100, self.bosshp,stage))
            self.Bosses.append(Boss(350, 1100,100,100, self.bosshp/2,stage+10))
            self.Bosses.append(Boss(650, 1100,100,100, self.bosshp/2,stage+20))
        
        self.zakoteki=Zakoteki(100,100,stage)
        self.grid = Grid(self.grid_size, self.cell_size, self.margin_x, self.margin_y)
        
        # その他の初期化
        self.zakotekicount=0
        self.zakotekis = []
        self.effects=[]
        self.coin = 0
        self.bomb = 3
        self.bombframe = 0
        self.bombkouka = 0
        self.comboframe = 0
        self.game_over = False
        self.game_clear=False
        self.game_clear2 = False
        self.clearframe = 400
        self.clearframe2= 500
        self.y = 0  # 背景スクロール用の変数
        self.y2 = -self.img.height
        self.selected_circle = None
        self.mouse_start_pos = None
        self.game_initialized = True  # ゲームが初期化されたことを示す
        
        self.zakotekispownhantei=True
        
        
        
        
        
        pyxel.mouse(True)
        
    def update(self):
        if self.state == 'stage_select':
            self.stage.update()
            if self.stage.stage >0:
                self.reset_game(self.stage.stage)
                self.state = 'main_game'
        elif self.state == 'main_game':

            if pyxel.btnp(pyxel.KEY_P):
                self.paused = not self.paused  # ポーズ状態を切り替え
            if  self.paused:
                if pyxel.btnp(pyxel.KEY_R):
                    self.paused = not self.paused
                    self.reset_game(self.stage.stage)
                if pyxel.btnp(pyxel.KEY_S):
                    self.paused = not self.paused
                    self.stage.stage = 0
                    self.state = 'stage_select'
            if not self.game_initialized:
                self.reset_game(self.stage.stage)
            if not self.paused:
                if not self.game_over and not self.game_clear:
                    self.player.update(0,0)

                    
                    for boss in self.Bosses:
                        boss.update(self.player.x,self.player.y)
                    for zakoteki in self.zakotekis:
                        zakoteki.update(self.player.x,self.player.y)
                    self.grid.update()



                    if self.zakotekicount>self.zakotekiborder:
                        
                        for boss in self.Bosses:
                            if boss.y>900:
                                boss.y-=900

                    # ゲームクリアの判定
                    bosses_to_remove = set()
                    for boss in self.Bosses:
                        if boss.hp <= 0 and boss.syometu>0:
                            if pyxel.frame_count%30==0:
                                self.effects.append(Effect(boss.x+random.uniform(-50, 50),boss.y+random.uniform(-50, 50),gaiz=True))

                            
                            boss.syometu-=1
                        elif boss.syometu==0:
                            boss.bullets.clear()
                            bosses_to_remove.add(boss)

                    for boss in bosses_to_remove:
                        self.Bosses.remove(boss)
                    

                    if not self.Bosses:   
                        self.clearframe2 -= 1



                    
                        

        


                    
                            




                
                        
                    if self.game_clear2 == True:
                        self.clearframe2 -= 1
                    
                    if self.clearframe2<0:
                        self.stage.clear_stage[self.stage.stage-1]=1
                        self.stage.stage=0
                        
                        self.state ='stage_select'
                        self.game_clear = True

                    # コンボ数で強化
                    if self.grid.combo>= 1:
                        self.player.muteki_timer=30


                    if self.grid.combo2 >= 2:
                        self.player.randoma()
                    if self.grid.combo2 >= 4:
                        self.player.randoma()
                    if self.grid.combo2 >= 8:
                        if self.bomb < 3:
                            self.bomb += 1

                    # ボムの使用
                    if pyxel.btnp(pyxel.KEY_R):
                        self.reset_game(self.stage.stage)
                    
                    if pyxel.btnp(pyxel.KEY_S):
                        self.stage.stage=0
                        
                        self.state ='stage_select'


                    if pyxel.btnp(pyxel.KEY_O):
                        self.zakotekiborder-=40000
                    

                    if pyxel.btn(pyxel.KEY_X):
                        if self.bomb > 0 and self.bombframe == 0 :

                        
                            self.zakotekis.clear()
                            self.bomb -= 1
                            self.bombframe = 200
                            

                    if self.bombframe > 0:
                        self.bombframe -= 1
                        for boss in self.Bosses:
                            boss.bullets.clear()
                    if self.zakotekispown:
                        if pyxel.frame_count % 400 ==0 and self.forstage and self.zakotekicount+len(self.zakotekis) <= self.zakotekiborder:
                            self.zakotekis.append(Zakoteki(random.uniform(300, 700),-10,1))
                            self.zakotekis.append(Zakoteki(random.uniform(300, 700),-10,2))
                            

                        if pyxel.frame_count % self.zakotekispown== 0 and 0<self.zakotekiborder:
                            self.zakotekis.append(Zakoteki(random.uniform(300, 700),-10,self.stagec))#雑魚的アペンド！！！！！！！！！！！
                            
                            if self.zakotekicount > self.zakotekiborder/2:
                                
                                self.zakotekis.append(Zakoteki(random.uniform(300, 500),-10,self.stagec))

                        
                        if pyxel.frame_count % 600== 0 and 0<self.zakotekiborder:
                            x=random.uniform(300, 700)
                            for i in range(random.randint(3, 6)):
                                self.zakotekis.append(Zakoteki(x+i*40,-10,self.stagec,gorudo=True))#雑魚的アペンド！！！！！！！！！！！
                        if self.zakotekiborder>=0:
                            self.zakotekiborder-=1
                        else:
                            self.zakotekispownhantei=False
                    
                    
                    
                    # 衝突判定
                    self.check_collisions()
                    # ドロップの操作とマッチング
                    self.handle_input()

                    # 背景のスクロールを更新
                    self.y += 1
                    self.y2 += 1
                    if self.y > self.img.height:
                        self.y = -self.img.height
                    if self.y2 > self.img.height:
                        self.y2 = -self.img.height

                else:
                    if pyxel.btnp(pyxel.KEY_R):
                        
                        self.reset_game(self.stage.stage)
                    
                    if pyxel.btnp(pyxel.KEY_S):
                        
                        self.stage.stage=0
                        
                        self.state ='stage_select'
                    
    def draw(self):
        if self.state == 'stage_select':
            self.stage.draw()
        elif self.state == 'main_game':
            self.draw_main_game()
            if self.paused:
                pyxel.rect(0, 0, self.screen_width, self.screen_height, 7)  # 半透明の黒い背景
                self.writer.draw(self.screen_width // 2 - 100, self.screen_height // 2 - 25, "PAUSED", 50, 10) # PAUSED文字
                self.writer.draw(self.screen_width // 2 - 150, self.screen_height // 2 + 50, "Press 'P' to resume", 30, 3) # resume文字
                self.writer.draw(self.screen_width // 2 - 150, self.screen_height // 2 + 100, "Press 'R' to restart", 30, 3) # restart文字
                self.writer.draw(self.screen_width // 2 - 150, self.screen_height // 2 + 150, "Press 'S' to stage select", 30, 3) # stage select文字
            
    def draw_main_game(self):
        # 背景の描画
        pyxel.cls(0)
        
        # 背景画像の描画
        pyxel.blt(150, self.y, self.img, 0, 0, self.img.width, self.img.height)
        pyxel.blt(150, self.y2, self.img, 0, 0, self.img.width, self.img.height)
        
        pyxel.blt(700, self.y, self.img2, 0, 0, self.img2.width, self.img2.height, 0)
        pyxel.blt(300, self.y + 200, self.img2, 0, 0, self.img2.width, self.img2.height, 0)
        pyxel.blt(500, self.y2, self.img2, 0, 0, self.img2.width, self.img2.height, 0)

        if self.paused:
            pyxel.rect(0, 0, self.screen_width, self.screen_height, 1)

        
        
        # グリッドの描画
        self.grid.draw(selected_circle=self.selected_circle)
        
        
        # コンボ数の表示
       
            


        
        
        
        if not self.game_over and not self.game_clear:
            # プレイヤーを描画
            
    
            # ボスを描画
            

            

            
            self.player.draw()

            

            for boss in self.Bosses:
                boss.draw()
            
            

            for zakoteki in self.zakotekis:
                zakoteki.draw()
            effects_to_remove = set()
            for effect in self.effects:
                effect.draw()

                if effect.framecount<=0:
                    effects_to_remove.add(effect)

            for effect in effects_to_remove:
                self.effects.remove(effect)

    
            # ボスのHPを表示
             # ボスのHPバーを描画
        if self.bombframe > 0:
            if pyxel.frame_count%2==1:
                pyxel.rect(0, 0, self.screen_width, self.screen_height, 7)

        

        self.writer.draw(5, 40, f"COMBO: {self.grid.combo}", 30, 6)


        self.writer.draw(5, 610, f"LIFE: {self.player.zanki}", 30, 8)


        self.writer.draw(5, 100, f"ボスまで: {self.zakotekiborder/160}", 30, 6)


        self.writer.draw(5, 150, f"tamairyoku: {self.player.state[0]}", 15, 8)
        self.writer.draw(5, 200, f"tamalevel: {self.player.state[1]}", 15, 8)
        self.writer.draw(5, 250, f"engo: {self.player.state[2]}", 15, 8)
        
        # ボムの数の表示
        self.writer.draw(5, 550, f"BOMB: {str(self.bomb)}", 30, 6)
        zahyou=80
        for  j in range(self.bomb):
            pyxel.blt(zahyou, 540, self.bombimg, 0, 0, self.bombimg.width, self.bombimg.height,0)
            zahyou+=50
       
        if self.clearframe2<500:
                
            self.writer.draw(400, 350, "YOU WIN!", 50, 10)
            self.writer.draw(5, 40, f"COMBO: {self.grid.combo}", 30, 0)
        elif self.game_over:                  
            pyxel.rect(0, 330, 900, 250, 7)
            self.writer.draw(400, 350, "GAME OVER", 50, 10)
            self.writer.draw(300, 420, "Press 'R' to restart", 50, 3)
            self.writer.draw(270, 490, "Press 'S' to stage select", 50, 2)

    def handle_input(self):
        # グリッド上のドロップの交換を処理

        if not self.grid.is_checking:
            if pyxel.btnp(pyxel.KEY_SPACE):
                grid_x = int((self.player.x - self.margin_x) / self.cell_size)
                grid_y = int((self.player.y - self.margin_y) / self.cell_size)
                if 0 <= grid_x < self.grid.grid_size and 0 <= grid_y < self.grid.grid_size:
                    self.mouse_start_pos = (grid_x, grid_y)
                    self.selected_circle = (grid_x, grid_y)
            elif pyxel.btn(pyxel.KEY_SPACE):
                if self.mouse_start_pos is not None:
                    grid_x = int((self.player.x - self.margin_x) / self.cell_size)
                    grid_y = int((self.player.y - self.margin_y) / self.cell_size)
                    start_x, start_y = self.mouse_start_pos
                    if 0 <= grid_x < self.grid.grid_size and 0 <= grid_y < self.grid.grid_size:
                        if max(abs(grid_x - start_x), abs(grid_y - start_y)) == 1:
                            self.grid.swap_drops((start_x, start_y), (grid_x, grid_y))
                            self.mouse_start_pos = (grid_x, grid_y)
                            self.selected_circle = (grid_x, grid_y)
            elif pyxel.btnr(pyxel.KEY_SPACE):
                self.mouse_start_pos = None
                self.selected_circle = None
                self.grid.is_checking = True  # マッチのチェックを開始

    def check_collisions(self):
        PLAYER_WIDTH = 8
        PLAYER_HEIGHT = 8
        player_left = self.player.x - PLAYER_WIDTH / 2
        player_right = self.player.x + PLAYER_WIDTH / 2
        player_top = self.player.y - PLAYER_HEIGHT / 2
        player_bottom = self.player.y + PLAYER_HEIGHT / 2
        # プレイヤーの弾がボスに当たったか確認
        bullets_to_remove = set()
        
        zakotekis_to_remove = set()

        zakotekis_to_remove2 = set()
        
        for bullet in self.player.bullets:
            bullet_left = bullet.x - bullet.w / 2
            bullet_right = bullet.x + bullet.w / 2
            bullet_top = bullet.y - bullet.h / 2
            bullet_bottom = bullet.y + bullet.h / 2
            
            for zakoteki in self.zakotekis:
               
                
                
                

                if (zakoteki.x + zakoteki.w / 2 > bullet_left and
                    zakoteki.x - zakoteki.w / 2 < bullet_right and
                    zakoteki.y + zakoteki.h / 2 > bullet_top and
                    zakoteki.y - zakoteki.h / 2 < bullet_bottom):
                    zakoteki.hp-=bullet.damage
                    if zakoteki.hp<1:
                        zakotekis_to_remove.add(zakoteki)
                    self.effects.append(Effect(bullet.x,bullet.y))
                    zakoteki.hit_timer = 10
                    bullets_to_remove.add(bullet)
                    


                
                    

                if zakoteki.y>1000:
                    zakotekis_to_remove2.add(zakoteki)
                        
            

        

      
            for boss in self.Bosses:

                if (boss.x - boss.w / 2 < bullet.x + bullet.w / 2 and
                    boss.x + boss.w / 2 > bullet.x - bullet.w / 2 and
                    boss.y < bullet.y + bullet.h and
                    boss.y + boss.h > bullet.y - bullet.h and boss.hp > 0):

                    self.effects.append(Effect(bullet.x,bullet.y))
                
                    boss.hit_timer = 10
                    bullets_to_remove.add(bullet)
                    boss.hp -= bullet.damage
            
    
        for zakoteki in self.zakotekis:
        # プレイヤーの境界を計算
           

        # 雑魚敵の境界を計算
            #zakoteki_left = zakoteki.x - zakoteki.w / 2
            #zakoteki_right = zakoteki.x + zakoteki.w / 2
            #zakoteki_top = zakoteki.y - zakoteki.h / 2
            #zakoteki_bottom = zakoteki.y + zakoteki.h / 2

        # 衝突判定
            

            if (player_left < zakoteki.x + zakoteki.w / 2 and
                player_right > zakoteki.x - zakoteki.w / 2 and
                player_top < zakoteki.y + zakoteki.h / 2 and
                player_bottom > zakoteki.y - zakoteki.h / 2 and
                self.player.muteki_timer == 0):
            # 衝突が検出された場合
                self.player.zanki -= self.player.tamairyoku
                self.player.muteki_timer = 240  # 無敵時間の設定
                zakotekis_to_remove.add(zakoteki)
                if self.player.zanki <= 0:
                    self.game_over = True
                    break
            
            for bullet in zakoteki.bullets:
                bullet_left = bullet.x - bullet.w / 2
                bullet_right = bullet.x + bullet.w / 2
                bullet_top = bullet.y - bullet.h / 2
                bullet_bottom = bullet.y + bullet.h / 2

                if (player_left < bullet_right and
                    player_right > bullet_left and
                    player_top < bullet_bottom and
                    player_bottom > bullet_top and
                    self.player.muteki_timer == 0):  # 無敵時間が終了しているか確認
                # 弾に当たった場合
                
                    self.player.zanki -= 1  # プレイヤーの残機を減らす
                    self.player.muteki_timer = 240  # 無敵時間を設定
                    zakotekis_to_remove.add(zakoteki)  # 雑魚敵を削除（必要であれば）
                    if self.player.zanki <= 0:
                        self.game_over = True  # ゲームオーバー
                        break
                
                

        for bullet in bullets_to_remove:
            self.player.bullets.remove(bullet)
        
        for zakoteki in zakotekis_to_remove:
            
            self.zakotekis.remove(zakoteki)

        for zakoteki in zakotekis_to_remove2:
            self.zakotekis.remove(zakoteki)

        
            

        
       
        

        # ボスの弾がプレイヤーに当たったか確認
        PLAYER_WIDTH = 8
        PLAYER_HEIGHT = 8

        player_left = self.player.x - PLAYER_WIDTH / 2
        player_right = self.player.x + PLAYER_WIDTH / 2
        player_top = self.player.y - PLAYER_HEIGHT / 2
        player_bottom = self.player.y + PLAYER_HEIGHT / 2
        for boss in self.Bosses:
            for bullet in boss.bullets:
           
               

                bullet_left = bullet.x - bullet.w / 2
                bullet_right = bullet.x + bullet.w / 2
                bullet_top = bullet.y - bullet.h / 2
                bullet_bottom = bullet.y + bullet.h / 2
                if (player_left < bullet_right and
                    player_right > bullet_left and
                    player_top < bullet_bottom and
                    player_bottom > bullet_top and
                    self.player.muteki_timer==0):
                    self.player.zanki -=1
                    self.player.muteki_timer=240
                    if self.player.zanki<=0:

                        
                        self.game_over = True
                        break
     
    
# アプリケーションの起動
App()