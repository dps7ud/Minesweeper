import scorekeeper as sk
import ms_Player as msp

class Diagnostic(sk.ScoreKeeper):

    def play(self, number_games=100):
        for ii in range(number_games):
            if self.seed_by_number:
                p = msp.Player(seed=ii)
            else:
                p = msp.Player()
            p.first_guess()
            p.later_guesses()
            if p.game_over == 0:
                p.game.prettyprint()
                print("=====")
            self.scores[p.game_over + 1] += 1


keeper = Diagnostic(seed_by_number=True)
keeper.play()
