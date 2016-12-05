"""Contains unit tests for functionallity contained in ms.py"""
import minesweeper as ms
import unittest

class MineSweeperTest(unittest.TestCase):
    def test_first_turn_lose(self):
        game = ms.MsGame( given_mines=[(3,3)] )
        val = game.play( ('c', 3, 3) )
        self.assertEqual(val, -1)

    def test_flag_first_guess(self):
        init_board = [[ '-' ] * 10 for xx in range(10)]
        game = ms.MsGame()
        with self.assertRaises(ms.BadGuessError) as context:
            val = game.first_guess( ('f',2,2) )

    def test_solve_first_guess(self):
        board = [[ '-' ] * 10 for xx in range(10)]
        game = ms.MsGame()
        with self.assertRaises(ms.BadGuessError) as context:
            val = game.first_guess( ('s',2,2) )

    def test_incorrect_clear(self):
        game = ms.MsGame( given_mines=[(1,1)] )
        game.play( ('c',3,3) )
        with self.assertRaises(ms.BadGuessError) as context:
            game.play( ('c',4,4) )

    def test_incorrect_solve_01(self):
        game = ms.MsGame( given_mines=[(1,1)] )
        game.play( ('c',3,3) )
        with self.assertRaises(ms.BadGuessError) as context:
            game.play( ('s',4,4) )

    def test_incorrect_solve_02(self):
        game = ms.MsGame( given_mines=[(1,1)] )
        game.play( ('c',3,3) )
        with self.assertRaises(ms.BadGuessError) as context:
            game.play( ('s',1,1) )


if __name__ == '__main__':
    unittest.main()
