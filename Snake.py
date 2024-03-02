import pygame
import random
import sys
import os

CELL_SIZE = 40
GRID_WIDTH, GRID_HEIGHT = 11, 11
WIDTH, HEIGHT = CELL_SIZE * GRID_WIDTH, CELL_SIZE * GRID_HEIGHT
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
DARK_GRAY = (128, 128, 128)
FONT_SIZE = 30
FONT_COLOR = BLACK
MENU_FONT_SIZE = 40
MENU_FONT_COLOR = WHITE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

APPLE_SPRITE = pygame.image.load(os.path.join("data", "apple.png"))
APPLE_SPRITE = pygame.transform.scale(APPLE_SPRITE, (CELL_SIZE, CELL_SIZE))
GOLDEN_APPLE_SPRITE = pygame.image.load(os.path.join("data", "golden_apple.png"))
GOLDEN_APPLE_SPRITE = pygame.transform.scale(GOLDEN_APPLE_SPRITE, (CELL_SIZE, CELL_SIZE))


class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [[5, 5]]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.speed = 3

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = [((cur[0] + x) % GRID_WIDTH), (cur[1] + y) % GRID_HEIGHT]
        if len(self.positions) > 2 and new in self.positions[2:]:
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

    def reset(self):
        self.length = 1
        self.positions = [[5, 5]]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.speed = 3

    def draw(self, surface):
        for i, p in enumerate(self.positions):
            r = pygame.Rect((p[0] * CELL_SIZE, p[1] * CELL_SIZE), (CELL_SIZE, CELL_SIZE))
            if i == 0:
                pygame.draw.rect(surface, GREEN, r)
            else:
                pygame.draw.rect(surface, BLACK, r)
                pygame.draw.rect(surface, GRAY, r, 1)
            if i == 0:
                if self.direction == UP:
                    pygame.draw.line(surface, WHITE, (r.centerx, r.centery), (r.centerx, r.centery - CELL_SIZE // 2), 4)
                elif self.direction == DOWN:
                    pygame.draw.line(surface, WHITE, (r.centerx, r.centery), (r.centerx, r.centery + CELL_SIZE // 2), 4)
                elif self.direction == LEFT:
                    pygame.draw.line(surface, WHITE, (r.centerx, r.centery), (r.centerx - CELL_SIZE // 2, r.centery), 4)
                elif self.direction == RIGHT:
                    pygame.draw.line(surface, WHITE, (r.centerx, r.centery), (r.centerx + CELL_SIZE // 2, r.centery), 4)


class Food:
    def __init__(self):
        self.position = [0, 0]
        self.sprite = APPLE_SPRITE
        self.randomize_position()

    def randomize_position(self):
        self.position = [random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)]
        if random.randint(1, 100) <= 5:
            self.sprite = GOLDEN_APPLE_SPRITE
        else:
            self.sprite = APPLE_SPRITE

    def draw(self, surface):
        r = pygame.Rect((self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE), (CELL_SIZE, CELL_SIZE))
        surface.blit(self.sprite, r)


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT + FONT_SIZE))
        pygame.display.set_caption("Snake")
        self.snake = Snake()
        self.food = Food()
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.menu_font = pygame.font.SysFont(None, MENU_FONT_SIZE)
        self.clock = pygame.time.Clock()

    def run(self):
        running = True
        while running:
            self.clock.tick(10)
            running = self.snake.move()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.snake.turn(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.turn(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.turn(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.turn(RIGHT)
                    elif event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                        self.restart_game()

            self.check_collision()

            self.surface.fill(WHITE)
            self.draw_score()
            self.snake.draw(self.surface)
            self.food.draw(self.surface)
            self.check_end()
            pygame.display.update()

    def check_collision(self):
        if self.snake.get_head_position() == self.food.position:
            if self.food.sprite == GOLDEN_APPLE_SPRITE:
                self.snake.length += 3
            else:
                self.snake.length += 1
            self.food.randomize_position()

    def check_end(self):
        pos = self.snake.get_head_position().copy()
        if self.snake.direction == UP:
            pos[1] -= 1
        elif self.snake.direction == DOWN:
            pos[1] += 1
        elif self.snake.direction == LEFT:
            pos[0] -= 1
        elif self.snake.direction == RIGHT:
            pos[0] += 1
        if pos in self.snake.positions[1:]:
            self.display_message("Длина змеи: {}".format(self.snake.length))
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        self.snake.reset()
                        self.food.randomize_position()
                        return

    def draw_score(self):
        score_text = self.font.render("Счёт: {}".format(self.snake.length), True, FONT_COLOR)
        self.surface.blit(score_text, (10, HEIGHT))

    def display_message(self, message):
        text = self.font.render(message, True, FONT_COLOR)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.surface.blit(text, text_rect)
        pygame.display.update()

    def restart_game(self):
        self.snake.reset()
        self.food.randomize_position()

    def return_to_main_menu(self):
        self.surface.fill(BLACK)
        title_text = self.menu_font.render("Snake", True, MENU_FONT_COLOR)
        title_text_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.surface.blit(title_text, title_text_rect)

        start_button = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, FONT_SIZE)
        pygame.draw.rect(self.surface, DARK_GRAY, start_button)
        start_text = self.menu_font.render("Начать игру", True, MENU_FONT_COLOR)
        self.surface.blit(start_text, start_button.topleft)

        quit_button = pygame.Rect(WIDTH // 4, HEIGHT // 2 + FONT_SIZE, WIDTH // 2, FONT_SIZE)
        pygame.draw.rect(self.surface, DARK_GRAY, quit_button)
        quit_text = self.menu_font.render("Выйти", True, MENU_FONT_COLOR)
        self.surface.blit(quit_text, quit_button.topleft)

        pygame.display.update()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if start_button.collidepoint(mouse_pos):
                        self.restart_game()
                        return
                    elif quit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.return_to_main_menu()
    game.run()
