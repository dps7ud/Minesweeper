"""ms.py
Class: MsGame - object holding all game related information
Class: BadGuessError - error that is called for any guess made at an improper time
"""

import itertools
import random
import re


def _pair_range(len_outter, len_inner):
    """Produces all pairs 0..len_outter - 1, 0..len_inner - 1"""
    for ii in range(len_outter):
        for jj in range(len_inner):
            yield ii, jj

class BadGuessError(Exception):
    pass


class MsGame:
    """Fields:
        before_first_guess -- bool indicating if the first guess has been made
        board -- List of lists holding all apperance information 
                    (flagged squares, cleared squares etc.)
        cleared -- set of tuples indicating squares that have been cleared
        flagged -- set of tuples indicating squares that have been flagged
        game_over -- int indicating if game is over (win:1 lose:-1) or can be played (0)
        mines -- list of tuples indicating positions of mines
        num_mines -- integer indicating number of mines present
        squares -- list of tuples of valid board squares 
                    (useful for not picking out of bounds squares)
        FLAGGED -- static value of star (*).
        DEFAULT -- static value of dash (-).

    Methods:
        __init__(given_mines) -- Initialize MsGame class
        get_around(square) -- returns all squares surrounding the given square
        get_board() -- returns current board state
        get_count( tuple(x, y) ) -- counts mines touching the square indicated by passed tuple
        clear( tuple(x, y) ) -- Recursive function that attempts to clear square indicated 
                    by passed tuple. Autoclears zeros and ends game if square is mined.
        first_guess( tuple(str, int, int) ) -- makes first guess
        flag( tuple(x, y) ) -- Attempts to flag or unflag passed tuple
        lose() -- ends game in loss
        play( tuple(str,int,int) ) -- handles all other logic for guessing 
            (flagging v. clearing, adjusts game_over etc.). Tuple contains
            guess type, x and y coords of guess.
        prettyprint() -- prints board for user consumption
        setup_mines() -- sets up mines after first guess in the case that 
            no list of mines was passed
        solve( tuple(x, y) ) -- Attempts to solve given square as MS minesweeper two click
        win_check() -- Checks if user has won game
    """

    FLAGGED = '*'
    DEFAULT = '-'

    def __init__(self, given_mines=None):
        """Populates self.squares and possibly other options. Initializes all instance
            variables.
        """
        self.before_first_guess = True
        self.board = [[ '-' ] * 10 for xx in range(10)]
        self.cleared = set()
        self.flagged = set()
        self.game_over = 0
        self.mines = []
        self.num_mines = 0
        self.squares = set()

        if given_mines is not None:
            self.num_mines = len(self.mines)
            self.mines = list(given_mines)
        for ii, jj in _pair_range(10, 10):
            self.squares.add( (ii,jj) )

    def get_around(self, square):
        """ Returns a set of squares adjacent to the input square,
        including the input square.
        """
        adds = (-1,0,1)
        around = set()
        for aa, bb in itertools.product(adds, repeat=2):
                around.add( (square[0] + aa, square[1] + bb) ) 
        around = around.intersection(self.squares)
        return around

    def get_board(self):
        """returns board state"""
        return self.board

    def get_count(self,square):
        """accepts tuple inicating target square
        returns number of neighbours in self.mines (counts self)
        """
        around = self.get_around(square)
        return len(around.intersection(self.mines))

    def clear(self, tuple_guess):
        """Clear indicated square. If square holds zero, 
        recursively call on neighbors to find space.
        """
        if tuple_guess in self.flagged.union(self.cleared):
            raise BadGuessError("Targeted square is flagged or already cleared")
        if tuple_guess in self.mines:
            self.lose()
            return self.game_over
        self.cleared.add(tuple_guess)
        #Not a mine so clear it
        num = self.get_count(tuple_guess)
        self.board[tuple_guess[0]][tuple_guess[1]] = str(num)
        if num == 0:
            to_clear = self.get_around(tuple_guess)
            to_clear.remove(tuple_guess)
            for element in to_clear:
                if element not in self.cleared:
                    self.clear(element)
                    
    def first_guess(self, guess):
        """Makes first guess and sets up mines after guess is made
        TODO: merge with clear()
        """
        if guess[0] != 'c':
            raise BadGuessError("First guess must be to clear")
        tuple_guess = (guess[1],guess[2])
        #Since guess[0] == 'c' we know the board will be changed
        self.before_first_guess = False
        self.setup_mines(tuple_guess)
        #Following check required for games with constructed mines
        if tuple_guess in self.mines:
            self.lose()
            return self.game_over
        self.clear(tuple_guess)
        if self.win_check():
            self.game_over = 1
        return self.game_over

    def flag(self, tuple_guess):
        """Attempts to flag or unflag passed tuple"""
        if tuple_guess in self.cleared:
            raise BadGuessError("Targeted square has been cleared")
        elif tuple_guess in self.flagged:
            self.board[tuple_guess[0]][tuple_guess[1]] = self.DEFAULT
            self.flagged.remove(tuple_guess)
        elif tuple_guess not in self.flagged:
            self.flagged.add(tuple_guess)
            self.board[tuple_guess[0]][tuple_guess[1]] = self.FLAGGED

    def lose(self):
        """Call to lose game"""
        for mine in self.mines:
            self.board[mine[0]][mine[1]] = 'X'
        self.game_over = -1

    def play(self, tup):
        """ Sorts guesses of all (flagging, solveing, clearing) types
        TODO: Remove in favor of calling clear/flag/solve directly
        """
        tuple_guess = (tup[1],tup[2])
        if not self.game_over:            
            if tup[0] == 'c':
                self.clear(tuple_guess)
            elif tup[0] == 'f':
                self.flag(tuple_guess)
            elif tup[0] == 's':
                self.solve(tuple_guess)
            if self.win_check():
                self.game_over = 1
        return self.game_over

    def prettyprint(self):
        """For printing board to user"""
        print('XX' + "0123456789")
        for ii in range(len(self.board)):
            print(str(ii) + ':',end='')
            for ch in self.board[ii]:
                print(ch,end='')
            print('')

    def setup_mines(self, guessed_square):
        if not self.mines:
            self.num_mines = 10
            for ii in range(self.num_mines):
                x = random.randint(0,9)
                y = random.randint(0,9)
                while (x,y) in self.mines or (x,y) == guessed_square:
                    x = random.randint(0,9)
                    y = random.randint(0,9)
                self.mines.append((x,y))
        else:
            return

    def solve(self, tuple_guess):
        """Attempts to 'solve' passed guess as MS minesweeper two click. Fails if
        square has not been cleared or holds 0, or if an incorrect number of 
        squares have been flagged.
        """
        num = self.board[tuple_guess[0]][tuple_guess[1]]
        expected_mines = self.get_around(tuple_guess).intersection(self.flagged)
        if num in {'0', 'X', self.FLAGGED, self.DEFAULT}:
            raise BadGuessError("Targeted square cannot be solved")
        if int(num) != len(expected_mines):
            raise BadGuessError("Targeted square cannot be solved")
        if expected_mines.intersection(set(self.mines)) != expected_mines:
            self.lose()
            return self.game_over
        to_clear = self.get_around(tuple_guess)
        to_clear.remove(tuple_guess)
        to_clear = to_clear.difference(self.mines)
        for sq in to_clear:
            if sq not in self.cleared:
                self.clear(sq)

    def win_check(self):
        """Return true iff game has been won
        TODO: Refactor
        """
        dashes = len(self.squares) - ( len(self.flagged) + len(self.cleared) )
        bangs = len(self.flagged)
        return bangs + dashes == self.num_mines

