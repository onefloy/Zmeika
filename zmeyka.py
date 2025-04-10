import pygame
import time
import random

# Инициализация pygame
pygame.init()

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BRIGHT_RED = (181, 18, 0)
DARK_GREEN = (0, 200, 0)
GRAY = (100, 100, 100)

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Змейка')

# Настройки игры
clock = pygame.time.Clock()
BLOCK_SIZE = 20
FPS = 15

# Шрифты
font = pygame.font.SysFont('arial', 30)
big_font = pygame.font.SysFont('arial', 50)

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.length = 3
        self.positions = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
        self.score = 0
        
        # Создаем начальное тело змейки
        for i in range(1, self.length):
            if self.direction == pygame.K_UP:
                self.positions.append((WIDTH // 2, HEIGHT // 2 + i * BLOCK_SIZE))
            elif self.direction == pygame.K_DOWN:
                self.positions.append((WIDTH // 2, HEIGHT // 2 - i * BLOCK_SIZE))
            elif self.direction == pygame.K_LEFT:
                self.positions.append((WIDTH // 2 + i * BLOCK_SIZE, HEIGHT // 2))
            elif self.direction == pygame.K_RIGHT:
                self.positions.append((WIDTH // 2 - i * BLOCK_SIZE, HEIGHT // 2))
    
    def get_head_position(self):
        return self.positions[0]
    
    def move(self):
        head = self.get_head_position()
        x, y = head
        
        if self.direction == pygame.K_UP:
            y -= BLOCK_SIZE
        elif self.direction == pygame.K_DOWN:
            y += BLOCK_SIZE
        elif self.direction == pygame.K_LEFT:
            x -= BLOCK_SIZE
        elif self.direction == pygame.K_RIGHT:
            x += BLOCK_SIZE
            
        # Проверка на выход за границы (телепортация)
        if x >= WIDTH:
            x = 0
        elif x < 0:
            x = WIDTH - BLOCK_SIZE
        if y >= HEIGHT:
            y = 0
        elif y < 0:
            y = HEIGHT - BLOCK_SIZE
            
        self.positions.insert(0, (x, y))
        if len(self.positions) > self.length:
            self.positions.pop()
    
    def draw(self, surface):
        for i, p in enumerate(self.positions):
            color = DARK_GREEN if i == 0 else GREEN  # Голова темнее
            rect = pygame.Rect((p[0], p[1]), (BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)
    
    def check_collision(self):
        head = self.get_head_position()
        return head in self.positions[1:]

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()
    
    def randomize_position(self):
        self.position = (
            random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE,
            random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        )
    
    def draw(self, surface):
        rect = pygame.Rect((self.position[0], self.position[1]), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(surface, BRIGHT_RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    while True:
        screen.fill(BLACK)
        draw_text('ЗМЕЙКА', big_font, GREEN, screen, WIDTH // 2, HEIGHT // 4)
        draw_text('Нажмите любую клавишу для начала игры', font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
        draw_text('Управление: стрелки', font, GRAY, screen, WIDTH // 2, HEIGHT * 3 // 4)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                return

def game_loop():
    snake = Snake()
    food = Food()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    # Запрет движения в противоположном направлении
                    if (event.key == pygame.K_UP and snake.direction != pygame.K_DOWN) or \
                       (event.key == pygame.K_DOWN and snake.direction != pygame.K_UP) or \
                       (event.key == pygame.K_LEFT and snake.direction != pygame.K_RIGHT) or \
                       (event.key == pygame.K_RIGHT and snake.direction != pygame.K_LEFT):
                        snake.direction = event.key
        
        snake.move()
        
        # Проверка на съедение еды
        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()
            # Убедимся, что еда не появилась в теле змейки
            while food.position in snake.positions:
                food.randomize_position()
        
        # Проверка на столкновение с собой
        if snake.check_collision():
            running = False
        
        # Отрисовка
        screen.fill(BLACK)
        snake.draw(screen)
        food.draw(screen)
        
        # Отрисовка счета
        draw_text(f'Очки: {snake.score}', font, WHITE, screen, WIDTH // 2, 20)
        
        pygame.display.update()
        clock.tick(FPS)
    
    # Экран окончания игры
    screen.fill(BLACK)
    draw_text('Игра окончена!', big_font, BRIGHT_RED, screen, WIDTH // 2, HEIGHT // 3)
    draw_text(f'Ваш счет: {snake.score}', font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
    draw_text('Нажмите любую клавишу для возврата в меню', font, GRAY, screen, WIDTH // 2, HEIGHT * 2 // 3)
    pygame.display.update()
    
    # Ожидание нажатия клавиши
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                waiting = False

# Основной цикл игры
while True:
    main_menu()
    game_loop()