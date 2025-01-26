import random
import tkinter as tk
from tkinter import messagebox

GRID_SIZE = 4
INIT_NUMBER_COUNT = 2
PROB_OF_FOUR = 0.3
ANIMATION_SPEED = 5  # 像素/帧
TILE_SIZE = 90
PADDING = 10


class Game2048:
    """
    root: tkinter.Tk
    """
    def __init__(self, root):
        self.root = root
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.score = 0
        self.moves_made = 0
        self.animations = []
        self.setup_gui()
        self.add_new_tile()
        self.add_new_tile()
        self.update_grid()

    def setup_gui(self):
        self.root.title("2048 Game")
        self.root.geometry(
            f"{TILE_SIZE*GRID_SIZE + PADDING*(GRID_SIZE+1)}x{TILE_SIZE*GRID_SIZE + PADDING*(GRID_SIZE+1) + 60}"
        )
        self.root.resizable(False, False)

        # Score display
        self.score_label = tk.Label(self.root, text="Score: 0", font=("Arial", 14))
        self.score_label.pack(pady=10)

        # Game canvas
        self.canvas = tk.Canvas(
            self.root,
            width=TILE_SIZE * GRID_SIZE + PADDING * (GRID_SIZE + 1),
            height=TILE_SIZE * GRID_SIZE + PADDING * (GRID_SIZE + 1),
        )
        self.canvas.pack()

        # 绘制背景网格
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x = PADDING + c * (TILE_SIZE + PADDING)
                y = PADDING + r * (TILE_SIZE + PADDING)
                self.canvas.create_rectangle(
                    x,
                    y,
                    x + TILE_SIZE,
                    y + TILE_SIZE,
                    fill="#cdc1b4",
                    outline="#bbada0",
                    width=2,
                )

        # Bind keyboard events
        self.root.bind("<Up>", lambda event: self.move(1))
        self.root.bind("<Down>", lambda event: self.move(2))
        self.root.bind("<Left>", lambda event: self.move(3))
        self.root.bind("<Right>", lambda event: self.move(4))
        self.root.bind("q", lambda event: self.root.destroy())

    def add_new_tile(self):
        empty_cells = [
            (r, c)
            for r in range(GRID_SIZE)
            for c in range(GRID_SIZE)
            if self.grid[r][c] == 0
        ]
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.grid[row][col] = 2 if random.random() > PROB_OF_FOUR else 4
            # 添加新方块时的动画
            self.animate_appear(row, col)

    def animate_appear(self, row, col):
        x = PADDING + col * (TILE_SIZE + PADDING)
        y = PADDING + row * (TILE_SIZE + PADDING)
        tile = self.create_tile(x, y, self.grid[row][col], scale=0.1)

        def scale_up(step=0):
            if step < 10:
                scale = 0.1 + 0.373 * step
                self.canvas.scale(
                    tile[0], x + TILE_SIZE / 2, y + TILE_SIZE / 2, scale, scale
                )
                self.root.after(5, scale_up, step + 1)

        scale_up()

    def create_tile(self, x, y, value, scale=1.0):
        colors = {
            0: "#cdc1b4",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
            4096: "#3c3a32",
            8192: "#3c3a99",
        }
        tile = self.canvas.create_rectangle(
            x,
            y,
            x + TILE_SIZE,
            y + TILE_SIZE,
            fill=colors.get(value, "#3c3a32"),
            outline="#bbada0",
            width=2,
        )
        text = self.canvas.create_text(
            x + TILE_SIZE / 2,
            y + TILE_SIZE / 2,
            text=str(value) if value != 0 else "",
            font=("Arial", 24, "bold"),
            fill="#776e65" if value < 8 else "#f9f6f2",
        )
        if scale != 1.0:
            self.canvas.scale(tile, x + TILE_SIZE / 2, y + TILE_SIZE / 2, scale, scale)
            self.canvas.scale(text, x + TILE_SIZE / 2, y + TILE_SIZE / 2, scale, scale)
        return (tile, text)

    def move(self, direction):
        if self.animations:
            return  # 动画进行中时忽略输入

        original_grid = [row[:] for row in self.grid]
        moved = False

        # 处理移动逻辑（同原代码）
        if direction == 1:  # Up
            for col in range(GRID_SIZE):
                column = [self.grid[r][col] for r in range(GRID_SIZE)]
                new_column = self.move_row(column, 1)
                for r in range(GRID_SIZE):
                    self.grid[r][col] = new_column[r]

        elif direction == 2:  # Down
            for col in range(GRID_SIZE):
                column = [self.grid[r][col] for r in range(GRID_SIZE)]
                new_column = self.move_row(column, -1)
                for r in range(GRID_SIZE):
                    self.grid[r][col] = new_column[r]

        elif direction == 3:  # Left
            for r in range(GRID_SIZE):
                self.grid[r] = self.move_row(self.grid[r], 1)

        elif direction == 4:  # Right:
            for r in range(GRID_SIZE):
                self.grid[r] = self.move_row(self.grid[r], -1)

        if original_grid != self.grid:
            moved = True
            self.prepare_animations(original_grid, direction)
            self.animate_move()
            self.moves_made += 1

            if self.is_game_over():
                messagebox.showinfo(
                    "Game Over", f"Game Over!\nFinal Score: {self.score}"
                )
                self.root.destroy()

        return moved

    def prepare_animations(self, original_grid, direction):
        # 分析移动差异并创建动画队列
        self.animations = []
        move_vectors = {
            1: (0, -1),  # Up
            2: (0, 1),  # Down
            3: (-1, 0),  # Left
            4: (1, 0),  # Right
        }
        dx, dy = move_vectors[direction]
        
        # 记录合并的方块
        merged_tiles = set()

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if original_grid[r][c] != 0:
                    # 查找当前方块的新位置
                    new_r, new_c = r, c
                    while True:
                        next_r = new_r + dy
                        next_c = new_c + dx
                        if 0 <= next_r < GRID_SIZE and 0 <= next_c < GRID_SIZE:
                            if self.grid[next_r][next_c] == 0:
                                new_r, new_c = next_r, next_c
                            else:
                                # 检查是否合并
                                if (self.grid[next_r][next_c] == original_grid[r][c] and
                                    (next_r, next_c) not in merged_tiles):
                                    merged_tiles.add((next_r, next_c))
                                    # 添加合并动画
                                    self.animations.append({
                                        "type": "merge",
                                        "tiles": [
                                            *self.canvas.find_withtag(f"tile_{r}_{c}"),
                                            *self.canvas.find_withtag(f"tile_{next_r}_{next_c}")
                                        ],
                                        "position": (
                                            PADDING + next_c * (TILE_SIZE + PADDING),
                                            PADDING + next_r * (TILE_SIZE + PADDING)
                                        ),
                                        "value": self.grid[next_r][next_c] * 2
                                    })
                                    break
                                break
                        else:
                            break

                    # 计算移动距离
                    start_x = PADDING + c * (TILE_SIZE + PADDING)
                    start_y = PADDING + r * (TILE_SIZE + PADDING)
                    end_x = PADDING + new_c * (TILE_SIZE + PADDING)
                    end_y = PADDING + new_r * (TILE_SIZE + PADDING)

                    if (start_x, start_y) != (end_x, end_y):
                        self.animations.append(
                            {
                                "type": "move",
                                "start": (start_x, start_y),
                                "end": (end_x, end_y),
                                "tiles": self.canvas.find_withtag(f"tile_{r}_{c}"),
                            }
                        )

    def animate_move(self):
        if not self.animations:
            self.finalize_move()
            return

        animation = self.animations.pop(0)
        tiles = animation["tiles"]

        if animation["type"] == "move":
            start_x, start_y = animation["start"]
            end_x, end_y = animation["end"]
            dx = (end_x - start_x) / ANIMATION_SPEED
            dy = (end_y - start_y) / ANIMATION_SPEED

            def move_step(step=0):
                if step < ANIMATION_SPEED:
                    for tile in tiles:
                        self.canvas.move(tile, dx, dy)
                    self.root.after(5, move_step, step + 1)
                else:
                    # 确保最终位置准确
                    for tile in tiles:
                        self.canvas.moveto(tile, end_x, end_y)
                    self.animate_move()

            move_step()
        elif animation["type"] == "merge":
            # Handle merge animation
            x, y = animation["position"]
            value = animation["value"]

            # Remove old tiles
            for tile in tiles:
                self.canvas.delete(tile)

            # Create new merged tile
            self.create_tile(x, y, value)
            self.animate_move()

    def finalize_move(self):
        self.canvas.delete("all")
        # 重新绘制背景网格
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x = PADDING + c * (TILE_SIZE + PADDING)
                y = PADDING + r * (TILE_SIZE + PADDING)
                self.canvas.create_rectangle(
                    x,
                    y,
                    x + TILE_SIZE,
                    y + TILE_SIZE,
                    fill="#cdc1b4",
                    outline="#bbada0",
                    width=2,
                )
        # 更新显示
        self.update_grid()
        self.add_new_tile()
        self.score_label.config(text=f"Score: {self.score}")

    def update_grid(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] != 0:
                    x = PADDING + c * (TILE_SIZE + PADDING)
                    y = PADDING + r * (TILE_SIZE + PADDING)
                    self.create_tile(x, y, self.grid[r][c])

    # 以下方法保持原样（move_row, is_game_over等）
    def move_row(self, row, direction):
        if direction == 1:  # Left
            row_values = [x for x in row if x != 0]
            new_row = []
            i = 0
            while i < len(row_values):
                if i + 1 < len(row_values) and row_values[i] == row_values[i + 1]:
                    new_row.append(row_values[i] * 2)
                    self.score += row_values[i] * 2
                    i += 2
                else:
                    new_row.append(row_values[i])
                    i += 1
            new_row.extend([0] * (GRID_SIZE - len(new_row)))

        elif direction == -1:  # Right
            row_values = [x for x in row if x != 0]
            new_row = []
            i = len(row_values) - 1
            while i >= 0:
                if i - 1 >= 0 and row_values[i] == row_values[i - 1]:
                    new_row.insert(0, row_values[i] * 2)
                    self.score += row_values[i] * 2
                    i -= 2
                else:
                    new_row.insert(0, row_values[i])
                    i -= 1
            new_row = [0] * (GRID_SIZE - len(new_row)) + new_row

        return new_row

    def is_game_over(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.grid[r][c] == 0:
                    return False
                if r < GRID_SIZE - 1 and self.grid[r][c] == self.grid[r + 1][c]:
                    return False
                if c < GRID_SIZE - 1 and self.grid[r][c] == self.grid[r][c + 1]:
                    return False
        return True


if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
