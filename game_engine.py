import random
import numpy as np

class Ship:
    def __init__(self, size):
        self.row = random.randint(0, 9)
        self.col = np.random.randint(0, 9)
        self.size = size
        self.orientation = random.choice(['h', 'v'])
        self.indexes = self.compute_indexes()

    def compute_indexes(self):
        start_index = self.row * 10 + self.col
        if self.orientation == 'h':
            return [start_index + i for i in range(self.size)]
        elif self.orientation == 'v':
            return [start_index + i*10 for i in range(self.size)]


class Player:

    def __init__(self):
        self.ships = []
        self.search = ['U' for _ in range(100)] # 'U' for 'unknown'
        self.place_ships(sizes=[5, 4, 3, 3, 2])
        list_of_lists_of_indexes = [ship.indexes for ship in self.ships]
        self.indexes = [index for sublist in list_of_lists_of_indexes for index in sublist]

    def place_ships(self, sizes):
        for size in sizes:
            placed = False

            while not placed:

                # створення нового корабля
                ship = Ship(size)

                # перевірка можливості розташування
                placement_possible = True

                for i in ship.indexes:

                    # індекси мають бути < 100:
                    if i >= 100:
                        placement_possible = False
                        break

                    # кораблі не можуть переноситись на новий рядок
                    new_row = i // 10
                    new_col = i % 10
                    if new_row != ship.row and new_col != ship.col:
                        placement_possible = False
                        break

                    # кораблі не можуть перетинатися (накладатися одне на одного)
                    for other_ship in self.ships:
                        if i in other_ship.indexes:
                            placement_possible = False
                            break


                # розміщення корабля
                if placement_possible:
                    self.ships.append(ship)
                    placed = True


class Game:

    def __init__(self, human1, human2):
        self.human1 = human1
        self.human2 = human2
        self.player1 = Player()
        self.player2 = Player()
        self.player1_turn = True
        self.computer_turn = True if not self.human1 else False
        self.over = False
        self.result = None
        self.n_shots = 0
        self.PROB_MAP = np.zeros((10, 10))


    def make_move(self, i):
        player = self.player1 if self.player1_turn else self.player2
        opponent = self.player2 if self.player1_turn else self.player1
        hit = False

        # встановлення промаху 'M' чи влучання 'H'
        if i in opponent.indexes:
            player.search[i] = 'H'
            hit = True

            # перевірка чи не затоплений корабель ('S')
            for ship in opponent.ships:
                sunk = True
                for i in ship.indexes:
                    if player.search[i] == 'U':
                        sunk = False
                if sunk:
                    for i in ship.indexes:
                        player.search[i] = 'S'
        else:
            player.search[i] = 'M'

        # перевірка чи не закінчена гра
        game_over = True
        for i in opponent.indexes:
            if player.search[i] == 'U':
                game_over = False

        self.over = game_over
        self.result = 1 if self.player1_turn else 2

        if not hit:
            self.player1_turn = not self.player1_turn

            # зміна між чергою ходів людини та бота
            if (self.human1 and not self.human2) or (not self.human1 and self.human2):
                self.computer_turn = not self.computer_turn

        # +1 до здійснених пострілів
        self.n_shots += 1


    def random_ai(self):
        search = self.player1.search if self.player1_turn else self.player2.search
        unknown = [i for i, square in enumerate(search) if square == 'U']

        if len(unknown) > 0:
            random_index = random.choice(unknown)
            self.make_move(random_index)

    def hunt(self):
        search = self.player1.search if self.player1_turn else self.player2.search
        unknown = [i for i, square in enumerate(search) if square == 'U']
        hits = [i for i, square in enumerate(search) if square == 'H']

        # пошук у сусідніх клітинках при влучанні
        unknown_with_neighboring_hits1 = []
        unknown_with_neighboring_hits2 = []
        for u in unknown:
            if u+1 in hits or u-1 in hits or u-10 in hits or u+10 in hits:
                unknown_with_neighboring_hits1.append(u)
            if u+2 in hits or u-2 in hits or u-20 in hits or u+20 in hits:
                unknown_with_neighboring_hits2.append(u)

        # обрання невідомої клітинки 'U' коли було влучання і після чого промах
        # (повертаємось через 1 клітинку назад по фіксованій вісі)
        for u in unknown:
            if u in unknown_with_neighboring_hits1 and u in unknown_with_neighboring_hits2:
                self.make_move(u)
                return

        # pick 'U' squares that has a level-1 and level-2 neighbours marked as 'H'
        if len(unknown_with_neighboring_hits1) > 0:
            self.make_move(random.choice(unknown_with_neighboring_hits1))
            return

        # рандомний постріл
        self.random_ai()

        # +1 до здійснених пострілів
        self.n_shots += 1


    def hunt_with_parity(self):
        search = self.player1.search if self.player1_turn else self.player2.search
        unknown = [i for i, square in enumerate(search) if square == 'U']
        hits = [i for i, square in enumerate(search) if square == 'H']

        unknown_with_neighboring_hits1 = []
        unknown_with_neighboring_hits2 = []
        for u in unknown:
            if u+1 in hits or u-1 in hits or u-10 in hits or u+10 in hits:
                unknown_with_neighboring_hits1.append(u)
            if u+2 in hits or u-2 in hits or u-20 in hits or u+20 in hits:
                unknown_with_neighboring_hits2.append(u)

        for u in unknown:
            if u in unknown_with_neighboring_hits1 and u in unknown_with_neighboring_hits2:
                self.make_move(u)
                pass

        if len(unknown_with_neighboring_hits1) > 0:
            self.make_move(random.choice(unknown_with_neighboring_hits1))
            return

        # паттерн шахматної дошки (parity)
        checker_board = []
        for u in unknown:
            row = u // 10
            col = u % 10
            if (row + col) % 2 == 0:
                checker_board.append(u)
        if len(checker_board) > 0:
            self.make_move(random.choice(checker_board))
            return

        self.random_ai()


    def gen_prob_map(self):
        search = self.player1.search if self.player1_turn else self.player2.search
        prob_map = np.zeros([10, 10])
        ships = [5, 4, 3, 3, 2]

        for ship in ships:
            ship_map = ['1' if search[i] == 'H' else '0' for i in np.arange(100)]
            shot_map = ['1' if search[i] != 'U' else '0' for i in np.arange(100)]
            sunk_ship_coordinates = [i for i in np.arange(100) if search[i] == 'S' ]

            ship_map = np.resize(ship_map, (10, 10))
            shot_map = np.resize(shot_map, (10, 10))

            use_size = ship - 1

            # перевірка де на дошці поміститься корабель
            for i in np.arange(100):
                row = i // 10
                col = i % 10
                if shot_map[row][col] != '1':
                    # отримання потенційного знаходження кінців корабля
                    endpoints = []
                    # +1 до всіх ендпоінтів для компенсації індексації пайтона
                    if row - use_size >= 0:
                        endpoints.append(((row - use_size, col), (row + 1, col + 1)))
                    if row + use_size <= 9:
                        endpoints.append(((row, col), (row + use_size + 1, col + 1)))
                    if col - use_size >= 0:
                        endpoints.append(((row, col - use_size), (row + 1, col + 1)))
                    if col + use_size <= 9:
                        endpoints.append(((row, col), (row + 1, col + use_size + 1)))

                    for (start_row, start_col), (end_row, end_col) in endpoints:
                        if np.all(shot_map[start_row:end_row, start_col:end_col] == '0'):
                            prob_map[start_row:end_row, start_col:end_col] += 1

                # підвищення ймовірності знаходження корабля у клітинках, сусідніх для клітинки з влученням
                if shot_map[row][col] == '1' and \
                        ship_map[row][col] == '1' and \
                        (row*10 + col) not in sunk_ship_coordinates:  # un-weight влучення на затоплених кораблях

                    if (row + 1 <= 9) and (shot_map[row + 1][col] == '0'):
                        if (row - 1 >= 0) and \
                                ((row - 1)*10 + col) not in sunk_ship_coordinates and \
                                (shot_map[row - 1][col] == ship_map[row - 1][col] == '1'):
                            prob_map[row + 1][col] += 15
                        else:
                            prob_map[row + 1][col] += 10

                    if (row - 1 >= 0) and (shot_map[row - 1][col] == '0'):
                        if (row + 1 <= 9) and \
                                ((row + 1)*10 + col) not in sunk_ship_coordinates and \
                                (shot_map[row + 1][col] == ship_map[row + 1][col] == '1'):
                            prob_map[row - 1][col] += 15
                        else:
                            prob_map[row - 1][col] += 10

                    if (col + 1 <= 9) and (shot_map[row][col + 1] == '0'):
                        if (col - 1 >= 0) and \
                                (row*10 + col - 1) not in sunk_ship_coordinates and \
                                (shot_map[row][col - 1] == ship_map[row][col - 1] == '1'):
                            prob_map[row][col + 1] += 15
                        else:
                            prob_map[row][col + 1] += 10

                    if (col - 1 >= 0) and (shot_map[row][col - 1] == '0'):
                        if (col + 1 <= 9) and \
                                (row*10 + col + 1) not in sunk_ship_coordinates and \
                                (shot_map[row][col + 1] == ship_map[row][col + 1] == '1'):
                            prob_map[row][col - 1] += 15
                        else:
                            prob_map[row][col - 1] += 10

                # занулення ймовірностей до клітинок з промахом
                elif shot_map[row][col] == '1' and ship_map[row][col] != '1':
                    prob_map[row][col] = 0

        self.PROB_MAP = prob_map


    def probabilistic_ai(self):
        self.gen_prob_map()

        # отримання row i col для найбільшого елементу в PROB_MAP
        max_indices = np.where(self.PROB_MAP == np.amax(self.PROB_MAP))
        guess_row, guess_col = max_indices[0][0], max_indices[1][0]

        self.make_move(guess_row * 10 + guess_col)