from game_engine import Game
import matplotlib.pyplot as plt
import numpy as np

n_games = 10000
num_shots = []

for i in np.arange(n_games):
    game = Game(human1=False, human2=False)
    while not game.over:
        if game.player1_turn:
            game.probabilistic_ai()
        else:
            game.probabilistic_ai()

    print(i)
    num_shots.append(game.n_shots // 2)

print(num_shots)
values = []

for i in np.arange(101):
    values.append(num_shots.count(i))


plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-light.mplstyle')
plt.title('Метод Монте-Карло')
plt.plot(range(101), values)
plt.savefig('monte_carlo.png')
plt.show()