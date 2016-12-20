import ms_Player as msp


class ScoreKeeper:

    def __init__(self, seed_by_number=False):
        self.seed_by_number = seed_by_number
        self.scores = [0, 0, 0]

    def play(self, number_games=100):
        for ii in range(number_games):
            if self.seed_by_number:
                p = msp.Player(seed=ii)
            else:
                p = msp.Player()
            p.first_guess()
            p.later_guesses()
            self.scores[p.game_over + 1] += 1
    def results(self):
        print(self.scores)


if __name__ == '__main__':
    num = 500
    sk = ScoreKeeper(seed_by_number=True)
    sk.play()
    sk.results()
    sk = ScoreKeeper()
    sk.play()
    sk.results()
