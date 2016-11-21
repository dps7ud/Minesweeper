"""Contains unit tests for functionallity contained in ms.py"""
import ms
import unittest

class MineSweeperTest(unittest.TestCase):


    def test_first_turn_lose(self):
        game = ms.MsGame(given_mines=[(3,3)])
        val = game.play( ('c', 3, 3) )
        self.assertEqual(val[0], -1)

    def test_flag_first_guess(self):
        board = [[ '-' ] * 10 for xx in range(10)]
        game = ms.MsGame()
        val = game.play( ('f',2,2) )
        self.assertEqual(val[1], board)
        self.assertEqual(val[0], 0)

if __name__ == '__main__':
    unittest.main()
