from game_engine import Game

import numpy as np

import pygame
pygame.init()
pygame.display.set_caption('Пісочниця для метода Монте-Карло')
markersfont = pygame.font.SysFont('fresansttf', 30)

# глобальні змінні
SQ_SIZE = 30
H_MARGIN = SQ_SIZE * 4
V_MARGIN = SQ_SIZE * 3

WIDTH = SQ_SIZE * 10 * 2 + H_MARGIN + SQ_SIZE * 2
HEIGHT = SQ_SIZE * 10 * 2 + V_MARGIN + SQ_SIZE * 2
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
INDENT = 10
HUMAN1 = False
HUMAN2 = False

# кольори
GREY = (40, 50, 60)
WHITE = (255, 250, 250)
GREEN = (0, 128, 0)
RED = (250, 50, 100)
ORANGE = (250, 140, 20)
COLORS = {'U': WHITE,
          'M': GREY,
          'H': ORANGE,
          'S': RED}


# функція нанесення позначок для клітинок сітки
def draw_markers(player, left=SQ_SIZE*2, top=SQ_SIZE):
    NUMBERS = [' ' + str(i) if i < 10 else str(i) for i in range(1, 11)]
    LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', ' I', 'J']

    for i in range(10):
        x = left + i % 10 * SQ_SIZE + SQ_SIZE // 4
        y = top + i // 10 * SQ_SIZE + SQ_SIZE // 4
        text = LETTERS[i]
        textbox = markersfont.render(text, False, GREY, WHITE)
        SCREEN.blit(textbox, (x, y))

    for i in range(10):
        x = left + i // 10 * SQ_SIZE + SQ_SIZE // 4 - SQ_SIZE
        y = top + i % 10 * SQ_SIZE + SQ_SIZE // 4 + SQ_SIZE
        text = NUMBERS[i]
        textbox = markersfont.render(text, False, GREY, WHITE)
        SCREEN.blit(textbox, (x, y))


# функція малювання сітки (поля)
def draw_grid(player, left=SQ_SIZE*2, top=SQ_SIZE*2, search=False):
    if search:
        for i in range(100):
            x = left + i % 10 * SQ_SIZE
            y = top + i // 10 * SQ_SIZE
            x += SQ_SIZE // 2
            y += SQ_SIZE // 2
            pygame.draw.circle(SCREEN, COLORS[player.search[i]], (x, y), radius=SQ_SIZE // 4)
        pass

    for i in range(100):
        x = left + i % 10 * SQ_SIZE
        y = top + i // 10 * SQ_SIZE
        square = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(SCREEN, GREY, square, width=2)


# функція нанесення кораблів на сітку (поле) для кораблів
def draw_ships(player, left=SQ_SIZE*2, top=SQ_SIZE*2):
    for ship in player.ships:
        x = left + ship.col * SQ_SIZE + INDENT // 1.25
        y = top + ship.row * SQ_SIZE + INDENT // 1.25

        if ship.orientation == "h":
            width = ship.size * SQ_SIZE - 1.5*INDENT
            height = SQ_SIZE - 1.5*INDENT
        else:
            width = SQ_SIZE - 1.5*INDENT
            height = ship.size * SQ_SIZE - 1.5*INDENT

        rectangle = pygame.Rect(x, y, width, height)
        pygame.draw.rect(SCREEN, GREEN, rectangle, border_radius=10)


# функція для зображення теплової карти
def draw_heat_map(game, left=0, top=0):
    game.gen_prob_map()
    board_y = top
    for i in range(10):
        board_x = left
        for j in range(10):
            if np.sum(game.PROB_MAP) and not game.over:
                size_factor = 255 * game.PROB_MAP[i][j] / np.amax(game.PROB_MAP)
                pygame.draw.rect(SCREEN, (size_factor, size_factor // 3 - size_factor // 5, (255 - size_factor) // 8),
                             pygame.Rect(board_x, board_y, SQ_SIZE, SQ_SIZE))
            else:
                pygame.draw.rect(SCREEN, (0, 0, 0), pygame.Rect(board_x, board_y, SQ_SIZE, SQ_SIZE))

            board_x += SQ_SIZE

        board_y += SQ_SIZE


fool_game = Game(HUMAN1, HUMAN2)

# pygame loop
animating = True
pausing = False
while animating:

    # відслідковування інтеракцій користувача
    for event in pygame.event.get():

        # користувач закриває вікно pygame
        if event.type == pygame.QUIT:
            animating = False

        # користувач нажимає кнопку на клавіатурі
        if event.type == pygame.KEYDOWN:

            # Space для паузи/відновлення анімації
            if event.key == pygame.K_SPACE:
                pausing = not pausing

            # Enter для перезапуску гри
            if event.key == pygame.K_RETURN:
                game = Game(HUMAN1, HUMAN2)
                
    # виконання програми
    if not pausing:
        # фон
        SCREEN.fill(WHITE)

        # поле для пошуку
        draw_grid(fool_game.player1, search=True)

        # поле для кораблів
        draw_grid(fool_game.player2, left=(WIDTH - H_MARGIN) // 2 + H_MARGIN)

        # позначення для сітки
        draw_markers(fool_game.player1)
        draw_markers(fool_game.player2, left=(WIDTH - H_MARGIN) // 2 + H_MARGIN)

        # кораблі
        draw_ships(fool_game.player2, left=(WIDTH - H_MARGIN) // 2 + H_MARGIN)

        # теплова карта
        draw_grid(fool_game.player1, left=(WIDTH - H_MARGIN) // 2 - H_MARGIN // 2, top=(HEIGHT - V_MARGIN) // 2 + H_MARGIN // 2 + SQ_SIZE)
        draw_heat_map(fool_game, left=(WIDTH - H_MARGIN) // 2 - H_MARGIN // 2, top=(HEIGHT - V_MARGIN) // 2 + H_MARGIN // 2 + SQ_SIZE)
        draw_markers(fool_game.player1, left=(WIDTH - H_MARGIN) // 2 - H_MARGIN // 2, top=(HEIGHT - V_MARGIN) // 2 + H_MARGIN // 2)

        # ходи комп'ютера
        if not fool_game.over and fool_game.computer_turn:
            if fool_game.player1_turn:
                fool_game.probabilistic_ai()
                fool_game.player1_turn = True


        # оновлення зображення
        pygame.time.wait(400)
        pygame.display.flip()