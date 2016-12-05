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

if __name__ == '__main__':
    unittest.main()
