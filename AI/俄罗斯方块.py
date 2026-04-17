import pygame
import random

# 初始化
pygame.init()

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
COLORS = [
    (0, 255, 255),    # I - 青色
    (255, 255, 0),    # O - 黄色
    (128, 0, 128),    # T - 紫色
    (0, 255, 0),      # S - 绿色
    (255, 0, 0),      # Z - 红色
    (0, 0, 255),      # J - 蓝色
    (255, 165, 0)     # L - 橙色
]

# 方块形状定义
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]]   # L
]

# 游戏配置
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = GRID_WIDTH * BLOCK_SIZE + 200
SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE + 100

class Tetromino:
    def __init__(self):
        self.shape_index = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_index]
        self.color = COLORS[self.shape_index]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

class TetrisGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('俄罗斯方块')
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.fall_time = 0
        self.fall_speed = 500

    def check_collision(self, piece, offset_x=0, offset_y=0):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = piece.x + x + offset_x
                    new_y = piece.y + y + offset_y
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                        return True
                    if new_y >= 0 and self.grid[new_y][new_x]:
                        return True
        return False

    def merge_piece(self):
        for y, row in enumerate(self.current_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    grid_y = self.current_piece.y + y
                    grid_x = self.current_piece.x + x
                    if grid_y >= 0:
                        self.grid[grid_y][grid_x] = self.current_piece.color

    def clear_lines(self):
        lines_cleared = 0
        y = GRID_HEIGHT - 1
        while y >= 0:
            if all(self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
                lines_cleared += 1
            else:
                y -= 1
        if lines_cleared > 0:
            self.score += lines_cleared * 100

    def move(self, dx, dy):
        if not self.check_collision(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False

    def rotate_piece(self):
        old_shape = self.current_piece.shape
        self.current_piece.rotate()
        if self.check_collision(self.current_piece):
            self.current_piece.shape = old_shape

    def drop_piece(self):
        while not self.check_collision(self.current_piece, 0, 1):
            self.current_piece.y += 1

    def new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        if self.check_collision(self.current_piece):
            self.game_over = True

    def draw_grid(self):
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                rect = pygame.Rect(x * BLOCK_SIZE + 50, y * BLOCK_SIZE + 50,
                                 BLOCK_SIZE, BLOCK_SIZE)
                if self.grid[y][x]:
                    pygame.draw.rect(self.screen, self.grid[y][x], rect)
                pygame.draw.rect(self.screen, GRAY, rect, 1)

    def draw_piece(self, piece, offset_x=0, offset_y=0):
        for y, row in enumerate(piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect((piece.x + x + offset_x) * BLOCK_SIZE + 50,
                                     (piece.y + y + offset_y) * BLOCK_SIZE + 50,
                                     BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(self.screen, piece.color, rect)
                    pygame.draw.rect(self.screen, GRAY, rect, 1)

    def draw_next_piece(self):
        font = pygame.font.Font(None, 36)
        text = font.render('下一个:', True, WHITE)
        self.screen.blit(text, (GRID_WIDTH * BLOCK_SIZE + 70, 100))

        for y, row in enumerate(self.next_piece.shape):
            for x, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect(GRID_WIDTH * BLOCK_SIZE + 80 + x * BLOCK_SIZE,
                                     150 + y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(self.screen, self.next_piece.color, rect)
                    pygame.draw.rect(self.screen, GRAY, rect, 1)

    def draw_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f'分数: {self.score}', True, WHITE)
        self.screen.blit(text, (GRID_WIDTH * BLOCK_SIZE + 70, 300))

    def draw_paused(self):
        font = pygame.font.Font(None, 72)
        text = font.render('暂停', True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)

        font_small = pygame.font.Font(None, 36)
        continue_text = font_small.render('按 P 继续', True, WHITE)
        continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(continue_text, continue_rect)

    def draw_game_over(self):
        font = pygame.font.Font(None, 72)
        text = font.render('游戏结束', True, WHITE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)

        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render('按 R 重新开始', True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
        self.screen.blit(restart_text, restart_rect)

    def reset(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.score = 0
        self.game_over = False
        self.paused = False
        self.fall_time = 0

    def run(self):
        running = True
        while running:
            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            self.reset()
                    else:
                        if event.key == pygame.K_p:
                            self.paused = not self.paused
                        elif not self.paused:
                            if event.key == pygame.K_LEFT:
                                self.move(-1, 0)
                            elif event.key == pygame.K_RIGHT:
                                self.move(1, 0)
                            elif event.key == pygame.K_DOWN:
                                self.move(0, 1)
                            elif event.key == pygame.K_UP:
                                self.rotate_piece()
                            elif event.key == pygame.K_SPACE:
                                self.drop_piece()

            if not self.game_over and not self.paused:
                if self.fall_time >= self.fall_speed:
                    self.fall_time = 0
                    if not self.move(0, 1):
                        self.merge_piece()
                        self.clear_lines()
                        self.new_piece()

            self.screen.fill(BLACK)
            self.draw_grid()
            if not self.game_over:
                self.draw_piece(self.current_piece)
            self.draw_next_piece()
            self.draw_score()

            if self.paused:
                self.draw_paused()
            elif self.game_over:
                self.draw_game_over()

            pygame.display.flip()

        pygame.quit()

if __name__ == '__main__':
    game = TetrisGame()
    game.run()
