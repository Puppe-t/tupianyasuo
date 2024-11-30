import pygame
import random

# 初始化颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# 定义方块形状
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

COLORS = [CYAN, YELLOW, MAGENTA, ORANGE, BLUE, GREEN, RED]

class Tetris:
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.current_piece = None
        self.current_x = 0
        self.current_y = 0
        self.current_color = None
        self.score = 0
        self.game_over = False
        self.new_piece()

    def new_piece(self):
        # 随机选择新方块
        shape_idx = random.randint(0, len(SHAPES) - 1)
        self.current_piece = SHAPES[shape_idx]
        self.current_color = COLORS[shape_idx]
        self.current_x = self.width // 2 - len(self.current_piece[0]) // 2
        self.current_y = 0
        
        if self.check_collision():
            self.game_over = True

    def rotate(self):
        # 旋转当前方块
        rows = len(self.current_piece)
        cols = len(self.current_piece[0])
        rotated = [[self.current_piece[cols-j-1][i] for j in range(cols)] for i in range(rows)]
        
        old_piece = self.current_piece
        self.current_piece = rotated
        if self.check_collision():
            self.current_piece = old_piece

    def check_collision(self):
        # 检查碰撞
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[0])):
                if self.current_piece[y][x]:
                    if (self.current_y + y >= self.height or
                        self.current_x + x < 0 or
                        self.current_x + x >= self.width or
                        self.grid[self.current_y + y][self.current_x + x]):
                        return True
        return False

    def merge(self):
        # 将当前方块合并到网格中
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[0])):
                if self.current_piece[y][x]:
                    self.grid[self.current_y + y][self.current_x + x] = self.current_color

    def clear_lines(self):
        # 清除完整的行
        lines_cleared = 0
        y = self.height - 1
        while y >= 0:
            if all(self.grid[y]):
                lines_cleared += 1
                for y2 in range(y, 0, -1):
                    self.grid[y2] = self.grid[y2-1][:]
                self.grid[0] = [0] * self.width
            else:
                y -= 1
        self.score += lines_cleared * 100

    def move(self, dx, dy):
        # 移动当前方块
        self.current_x += dx
        self.current_y += dy
        if self.check_collision():
            self.current_x -= dx
            self.current_y -= dy
            if dy > 0:
                self.merge()
                self.clear_lines()
                self.new_piece()
            return False
        return True

def main():
    pygame.init()
    
    # 设置游戏窗口
    BLOCK_SIZE = 30
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("俄罗斯方块")
    
    clock = pygame.time.Clock()
    game = Tetris()
    
    fall_time = 0
    fall_speed = 50  # 值越小，下落越快
    
    while not game.game_over:
        fall_time += clock.get_rawtime()
        clock.tick()
        
        # 自动下落
        if fall_time >= fall_speed:
            game.move(0, 1)
            fall_time = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.move(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate()
                elif event.key == pygame.K_SPACE:
                    while game.move(0, 1):
                        pass
        
        # 绘制游戏界面
        screen.fill(BLACK)
        
        # 绘制网格
        for y in range(game.height):
            for x in range(game.width):
                if game.grid[y][x]:
                    pygame.draw.rect(screen, game.grid[y][x],
                                   [x * BLOCK_SIZE + 300, y * BLOCK_SIZE + 50,
                                    BLOCK_SIZE-1, BLOCK_SIZE-1])
        
        # 绘制当前方块
        if game.current_piece:
            for y in range(len(game.current_piece)):
                for x in range(len(game.current_piece[0])):
                    if game.current_piece[y][x]:
                        pygame.draw.rect(screen, game.current_color,
                                       [(game.current_x + x) * BLOCK_SIZE + 300,
                                        (game.current_y + y) * BLOCK_SIZE + 50,
                                        BLOCK_SIZE-1, BLOCK_SIZE-1])
        
        # 显示分数
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"分数: {game.score}", True, WHITE)
        screen.blit(score_text, (50, 50))
        
        pygame.display.update()
    
    # 游戏结束显示
    font = pygame.font.Font(None, 48)
    game_over_text = font.render("游戏结束!", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))
    pygame.display.update()
    
    # 等待几秒后退出
    pygame.time.wait(2000)
    pygame.quit()

if __name__ == "__main__":
    main()
