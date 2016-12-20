import ms_Player as msp
import unittest

class PlayerTest(unittest.TestCase):

    def test_seed_42(self):
        """Winnable with modification"""
        game = msp.Player(seed=42)
        game.run_game()
        self.assertEqual(game.game_over, 1)

    def test_seed_98(self):
        """Win"""
        game = msp.Player(seed=98)
        game.run_game()
        self.assertEqual(game.game_over, 1)

    def test_seed_60(self):
        """Win"""
        game = msp.Player(seed=60)
        game.run_game()
        self.assertEqual(game.game_over, 1)

    def test_pattern_1_1(self):
        """Want to find pattern at edge"""
        mines = [(8,2),(8,4),(8,7),(8,9)]
        player = msp.Player(given_mines=mines)
        player.run_game()
        self.assertEqual(player.game.win_check(), True)
        

if __name__ == '__main__':
    unittest.main()
