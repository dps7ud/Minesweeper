import ms_Player as msp

class ScoreKeeper:

    def __init__(self):
        self.scores = [0, 0, 0]

    def play(self, number_games=100):
        for ii in range(number_games):
            p = msp.Player()
            p.first_guess()
            p.later_guesses()
            if p.game_over == 1:
                self.scores[0] += 1
            elif p.game_over == -1:
                self.scores[1] += 1
            else:
                self.scores[2] += 1
   
    def results(self):
        print(self.scores)

if __name__ == '__main__':
    num = 500
    sk = ScoreKeeper()
    sk.play()
    sk.results()
