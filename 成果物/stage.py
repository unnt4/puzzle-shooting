# stage.py
import PyxelUniversalFont as puf
import pyxel

class Stage:
    def __init__(self):
        self.img = pyxel.Image(900, 700)
        self.img.load(x=0, y=0, filename="背景.png")
        
        self.writer = puf.Writer("misaki_gothic2.ttf")
        self.stage = 0
        self.clear_stage = [0, 0, 0, 0, 0]
        self.STAGE_NAMES = ["ステージ 1", "ステージ 2", "ステージ 3", "ステージ 4"]
       
        self.current_stage_index = 0
        self.hover_stage_index = -1  # マウスが重なっているステージのインデックス

    def update(self):
        if pyxel.btnp(pyxel.KEY_UP):
            self.current_stage_index = (self.current_stage_index - 1) % len(self.STAGE_NAMES)
        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.current_stage_index = (self.current_stage_index + 1) % len(self.STAGE_NAMES)
        # Enterキーで選択されたステージを表示
        if pyxel.btnp(pyxel.KEY_RETURN):
            self.stage = self.current_stage_index+1 # ステージ 1 を選択
            # 必要に応じて選択されたステージのインデックスを保持する
            

    def draw(self):
        pyxel.cls(2)  # 背景を黒に
        pyxel.blt(0, 0, self.img, 0, 0, self.img.width, self.img.height)
        
        # 各ステージ名を表示
        for i, stage_name in enumerate(self.STAGE_NAMES):
            x = 100
            y = 30 + i * 125
            if i == self.current_stage_index:
                color = 8  # 選択中のステージは赤
            else:
                color = 6  # それ以外はグレー
            pyxel.rect(x - 5, y - 2, 700, 80, 1)  # ステージ名の背景を描画
            self.writer.draw(x, y, f"{stage_name}", 30, color)
            pyxel.text(x, y, stage_name, color)  # ステージ名を描画

            if 1 == self.clear_stage[i]:
                self.writer.draw(x+300, y, f"CLEAR", 30, 3)
            