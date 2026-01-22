# grid.py
import random
from drop import Drop

class Grid:
    def __init__(self, grid_size, cell_size, margin_x, margin_y):
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.drops = [[Drop(i, j, random.choice([8, 9, 10, 11,12,13]),
                             self.margin_x, self.margin_y, self.cell_size)
                       for j in range(self.grid_size)] for i in range(self.grid_size)]
        self.is_checking = False
        self.combo = 0
        self.combo2=0
        self.comboframe=0

    def update(self):
        # ドロップの更新
        self.combo2=0
        all_stopped = True
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.drops[i][j].update()
                if self.drops[i][j].falling:
                    all_stopped = False
        if all_stopped and self.is_checking:
            self.check_matches()

    def draw(self, selected_circle=None):
        # グリッドの描画
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                drop = self.drops[i][j]
                is_selected = selected_circle == (i, j)
                if drop.color is not None:
                    drop.draw(is_selected)
       

    def swap_drops(self, circle1, circle2):
        x1, y1 = circle1
        x2, y2 = circle2
        self.drops[x1][y1], self.drops[x2][y2] = self.drops[x2][y2], self.drops[x1][y1]
        # グリッド上の位置を更新
        self.drops[x1][y1].grid_x, self.drops[x1][y1].grid_y = x1, y1
        self.drops[x2][y2].grid_x, self.drops[x2][y2].grid_y = x2, y2
        # 描画位置を更新
        self.drops[x1][y1].x = self.margin_x + x1 * self.cell_size + self.cell_size // 2
        self.drops[x1][y1].y = self.margin_y + y1 * self.cell_size + self.cell_size // 2
        self.drops[x2][y2].x = self.margin_x + x2 * self.cell_size + self.cell_size // 2
        self.drops[x2][y2].y = self.margin_y + y2 * self.cell_size + self.cell_size // 2

    def check_matches(self):
        
        matches = []
        # 縦方向のマッチを探す
        for i in range(self.grid_size):
            count = 1
            for j in range(1, self.grid_size):
                if self.drops[i][j].color == self.drops[i][j-1].color:
                    count += 1
                else:
                    if count >= 3:
                        self.combo += 1
                        for k in range(j - count, j):
                            matches.append((i, k))
                    count = 1
            if count >= 3:
                self.combo += 1
                for k in range(self.grid_size - count, self.grid_size):
                    matches.append((i, k))
        # 横方向のマッチを探す
        for j in range(self.grid_size):
            count = 1
            for i in range(1, self.grid_size):
                if self.drops[i][j].color == self.drops[i-1][j].color:
                    count += 1
                else:
                    if count >= 3:
                        self.combo += 1
                        for k in range(i - count, i):
                            matches.append((k, j))
                    count = 1
            if count >= 3:
                self.combo += 1
                for k in range(self.grid_size - count, self.grid_size):
                    matches.append((k, j))
                    
        # マッチしたドロップを消去
        if matches:
            for x, y in matches:
                self.drops[x][y].color = None  # 消えた状態を示す
            self.drop_down()
        else:
            # マッチがなければチェックを終了
            self.combo2=self.combo
            self.combo=0
            self.is_checking = False

        


    def drop_down(self):
        # 上から下に向かってチェック
        for i in range(self.grid_size):
            for j in range(self.grid_size - 1, -1, -1):
                if self.drops[i][j].color is None:
                    # 上のドロップを下に移動
                    for k in range(j - 1, -1, -1):
                        if self.drops[i][k].color is not None:
                            self.drops[i][j].color = self.drops[i][k].color
                            self.drops[i][k].color = None
                            self.drops[i][j].falling = True
                            self.drops[i][j].speed = 0
                            self.drops[i][j].y = self.margin_y + k * self.cell_size + self.cell_size // 2
                            self.drops[i][j].target_y = self.margin_y + j * self.cell_size + self.cell_size // 2
                            break
                    else:
                        # 上にドロップがない場合は新しいドロップを生成
                        self.drops[i][j] = Drop(i, j, random.choice([8, 9, 10, 11]),
                                                self.margin_x, self.margin_y, self.cell_size)
                        self.drops[i][j].falling = True
                        self.drops[i][j].speed = 0
                        self.drops[i][j].y = self.margin_y - self.cell_size // 2  # 画面外から開始
                        self.drops[i][j].target_y = self.margin_y + j * self.cell_size + self.cell_size // 2