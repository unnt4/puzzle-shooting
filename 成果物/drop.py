import pyxel
class Drop:
    def __init__(self, x, y, color, margin_x, margin_y, cell_size):
        self.grid_x = x  
        self.grid_y = y
        self.margin_x = margin_x
        self.margin_y = margin_y
        self.cell_size = cell_size
        self.x = margin_x + x * cell_size + cell_size // 2  
        self.y = margin_y + y * cell_size + cell_size // 2
        self.target_y = self.y
        self.color = color
        self.falling = False  
        self.speed = 0  

    def update(self):
        if self.falling:
            self.y += self.speed
            if self.y < self.target_y:
                self.speed += 0.2  # 重力加速度
            else:
                self.y = self.target_y
                self.falling = False
                self.speed = 0

    def draw(self, is_selected):
        radius = int(self.cell_size * 0.5) if is_selected else int(self.cell_size * 0.4)
        pyxel.circ(self.x, self.y, radius, self.color)

