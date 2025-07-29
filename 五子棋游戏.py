import tkinter as tk
from tkinter import messagebox

class GomokuGame:
    def __init__(self, root):
        self.root = root
        self.root.title("五子棋")
        self.root.resizable(False, False)
        
        # 游戏参数
        self.board_size = 15  # 15x15的棋盘
        self.cell_size = 40   # 每个格子的大小
        self.board_width = self.board_size * self.cell_size
        self.board_height = self.board_size * self.cell_size
        
        # 游戏状态
        self.game_started = False
        self.record = []  # 记录已下棋子的位置和颜色，格式：[(x, y, color), ...]
        
        # 创建开始界面
        self.create_start_screen()
    
    def create_start_screen(self):
        """创建开始界面"""
        # 清除现有界面
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 创建开始界面
        frame = tk.Frame(self.root)
        frame.pack(padx=50, pady=50)
        
        title_label = tk.Label(frame, text="五子棋", font=("SimHei", 24, "bold"))
        title_label.pack(pady=30)
        
        start_button = tk.Button(frame, text="开始游戏", font=("SimHei", 16), 
                                width=15, command=self.start_game)
        start_button.pack(pady=10)
        
        quit_button = tk.Button(frame, text="退出游戏", font=("SimHei", 16), 
                               width=15, command=self.root.quit)
        quit_button.pack(pady=10)
    
    def start_game(self):
        """开始游戏，创建游戏界面"""
        # 清除现有界面
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # 创建菜单栏
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="重新开始", command=self.restart_game)
        file_menu.add_command(label="返回主菜单", command=self.create_start_screen)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.root.quit)
        menu_bar.add_cascade(label="游戏", menu=file_menu)
        self.root.config(menu=menu_bar)
        
        # 创建棋盘
        self.canvas = tk.Canvas(self.root, width=self.board_width, 
                               height=self.board_height, bg="#F5DEB3")
        self.canvas.pack(padx=10, pady=10)
        
        # 绘制棋盘网格
        for i in range(self.board_size):
            # 横线
            self.canvas.create_line(
                self.cell_size/2, i * self.cell_size + self.cell_size/2,
                self.board_width - self.cell_size/2, i * self.cell_size + self.cell_size/2,
                width=1
            )
            # 竖线
            self.canvas.create_line(
                i * self.cell_size + self.cell_size/2, self.cell_size/2,
                i * self.cell_size + self.cell_size/2, self.board_height - self.cell_size/2,
                width=1
            )
        
        # 绘制五个星位
        star_points = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
        for x, y in star_points:
            self.canvas.create_oval(
                x * self.cell_size + self.cell_size/2 - 4,
                y * self.cell_size + self.cell_size/2 - 4,
                x * self.cell_size + self.cell_size/2 + 4,
                y * self.cell_size + self.cell_size/2 + 4,
                fill="black"
            )
        
        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self.callback1)  # 左键 - 黑棋
        self.canvas.bind("<Button-3>", self.callback2)  # 右键 - 白棋
        
        # 更新游戏状态
        self.game_started = True
        self.record = []
    
    def restart_game(self):
        """重新开始游戏"""
        self.start_game()
    
    def callback1(self, event):
        """左键点击事件处理 - 黑棋"""
        if not self.game_started:
            return
        
        # 计算点击位置对应的棋盘坐标
        x = int((event.x - self.cell_size/2) / self.cell_size + 0.5)
        y = int((event.y - self.cell_size/2) / self.cell_size + 0.5)
        
        # 检查坐标是否在棋盘范围内
        if 0 <= x < self.board_size and 0 <= y < self.board_size:
            # 检查是否已经有棋子
            if not self.is_position_occupied(x, y):
                # 记录并绘制黑子
                self.record.append((x, y, "black"))
                self.draw_stone(x, y, "black")
                
                # 检查是否获胜
                if self.check_win(x, y, "black"):
                    self.game_started = False
                    messagebox.showinfo("游戏结束", "黑方获胜！")
    
    def callback2(self, event):
        """右键点击事件处理 - 白棋"""
        if not self.game_started:
            return
        
        # 计算点击位置对应的棋盘坐标
        x = int((event.x - self.cell_size/2) / self.cell_size + 0.5)
        y = int((event.y - self.cell_size/2) / self.cell_size + 0.5)
        
        # 检查坐标是否在棋盘范围内
        if 0 <= x < self.board_size and 0 <= y < self.board_size:
            # 检查是否已经有棋子
            if not self.is_position_occupied(x, y):
                # 记录并绘制白子
                self.record.append((x, y, "white"))
                self.draw_stone(x, y, "white")
                
                # 检查是否获胜
                if self.check_win(x, y, "white"):
                    self.game_started = False
                    messagebox.showinfo("游戏结束", "白方获胜！")
    
    def is_position_occupied(self, x, y):
        """检查指定位置是否已经有棋子"""
        for pos in self.record:
            if pos[0] == x and pos[1] == y:
                return True
        return False
    
    def draw_stone(self, x, y, color):
        """在指定位置绘制棋子"""
        center_x = x * self.cell_size + self.cell_size/2
        center_y = y * self.cell_size + self.cell_size/2
        
        radius = self.cell_size/2 - 2
        self.canvas.create_oval(
            center_x - radius, center_y - radius,
            center_x + radius, center_y + radius,
            fill=color, outline="black"
        )
    
    def check_win(self, x, y, color):
        """检查指定位置的棋子是否形成五子连珠"""
        directions = [
            (1, 0),   # 水平方向
            (0, 1),   # 垂直方向
            (1, 1),   # 对角线方向
            (1, -1)   # 反对角线方向
        ]
        
        for dx, dy in directions:
            count = 1  # 当前位置已经有一个棋子
            
            # 向正方向检查
            for i in range(1, 5):
                nx = x + dx * i
                ny = y + dy * i
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if self.get_stone_color(nx, ny) == color:
                        count += 1
                    else:
                        break
                else:
                    break
            
            # 向反方向检查
            for i in range(1, 5):
                nx = x - dx * i
                ny = y - dy * i
                if 0 <= nx < self.board_size and 0 <= ny < self.board_size:
                    if self.get_stone_color(nx, ny) == color:
                        count += 1
                    else:
                        break
                else:
                    break
            
            # 判断是否五子连珠
            if count >= 5:
                return True
        
        return False
    
    def get_stone_color(self, x, y):
        """获取指定位置棋子的颜色，如果没有棋子则返回None"""
        for pos in self.record:
            if pos[0] == x and pos[1] == y:
                return pos[2]
        return None

if __name__ == "__main__":
    root = tk.Tk()
    # 设置中文字体
    root.option_add("*Font", "SimHei 10")
    game = GomokuGame(root)
    root.mainloop()    