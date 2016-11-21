import ms
import unittest

class MineSweeperTest(unittest.TestCase):

    def test_first_turn_lose(self):
        game = ms.MsGame(given_mines=[(3,3)])
        val = game.play( ('c', 3, 3) )
        self.assertEqual(val[0], -1)


if __name__ == '__main__':
    unittest.main()
