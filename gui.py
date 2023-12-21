from game_engine import Game

import pygame
pygame.init()
pygame.display.set_caption('Морський бій')
myfont = pygame.font.SysFont('fresansttf', 80)
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
BLUE = (50, 150, 200)
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
def draw_grid(player, left=0, top=0, search=False):
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
def draw_ships(player, left=0, top=0):
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

game = Game(HUMAN1, HUMAN2)

# pygame loop
animating = True
pausing = False
while animating:

    # відслідковування інтеракцій користувача
    for event in pygame.event.get():

        # користувач закриває вікно pygame
        if event.type == pygame.QUIT:
            animating = False

        # користувач натискає на поле (робить постріл)
        if event.type == pygame.MOUSEBUTTONDOWN and not game.over:
            x,y = pygame.mouse.get_pos()

            if game.player1_turn and x - 2*SQ_SIZE < SQ_SIZE * 10 and y - 2*SQ_SIZE < SQ_SIZE * 10:
                row = y // SQ_SIZE - 2
                col = x // SQ_SIZE - 2
                index = row * 10 + col
                game.make_move(index)

            elif not game.player1_turn and x > WIDTH - SQ_SIZE * 10 - SQ_SIZE and y + SQ_SIZE > SQ_SIZE * 10 + V_MARGIN:
                row = (y - SQ_SIZE * 10 - V_MARGIN) // SQ_SIZE - 1
                col = (x - SQ_SIZE * 10 - H_MARGIN)// SQ_SIZE - 1
                index = row * 10 + col
                game.make_move(index)

        # користувач нажимає кнопку на клавіатурі
        if event.type == pygame.KEYDOWN:

            # Esc для закриття анімації
            if event.key == pygame.K_ESCAPE:
                animating = False

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

        # поля для пошуку
        draw_grid(game.player1, left=2*SQ_SIZE, top=2*SQ_SIZE, search=True)
        draw_grid(game.player2, search=True, left=(WIDTH - H_MARGIN) // 2 + H_MARGIN, top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN)

        # поля для кораблів
        draw_grid(game.player1, left=2*SQ_SIZE, top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN)   # player1
        draw_grid(game.player2, left=(WIDTH - H_MARGIN) // 2 + H_MARGIN, top=2*SQ_SIZE)   # player2

        # позначення для сітки
        draw_markers(game.player1)
        draw_markers(game.player2, left=(WIDTH - H_MARGIN) // 2 + H_MARGIN)   # player2
        draw_markers(game.player1, top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN - SQ_SIZE)   # player1
        draw_markers(game.player2, top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN - SQ_SIZE, left=(WIDTH - H_MARGIN) // 2 + H_MARGIN)

        # кораблі
        draw_ships(game.player1, left=SQ_SIZE*2, top=(HEIGHT - V_MARGIN) // 2 + V_MARGIN)    # player1
        draw_ships(game.player2, left=(WIDTH - H_MARGIN) // 2 + H_MARGIN, top=SQ_SIZE*2)   # player2

        # ходи комп'ютера
        if not game.over and game.computer_turn:
            if game.player1_turn:
                game.hunt_with_parity()
            else:
                game.hunt_with_parity()

        # повідомлення після завершення гри
        if game.over:
            text = f'Гравець {str(game.result)} переміг!'
            textbox = myfont.render(text, False, GREY, WHITE)
            SCREEN.blit(textbox, (WIDTH//2 - 300 + SQ_SIZE*2, HEIGHT//2 - SQ_SIZE // 2))

        # оновлення зображення
        pygame.time.wait(500)
        pygame.display.flip()