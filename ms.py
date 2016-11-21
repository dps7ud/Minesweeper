"""Minesweeper.py
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
        board: List of lists holding all apperance information 
                    (flagged squares, cleared squares etc.)
        gameOver: binary indicating if game is over (True) or can be played (False)
        mines: list of tuples indicating positions of mines
        squares: list of tuples of valid board squares 
                    (useful for not picking out of bounds squares)
        before_first_guess: bool indicating if the first guess has been made
    Methods:
        __init__(): populates self.squares and possibly other options
        prettyprint(): prints board for user consumption
        get_count(tuple): counts mines touching the square indicated by passed tuple
        lose(): ends game in loss
        isFirst(): Checks if board is fresh (returns True) or not (returns False)
        winCheck(): Checks if user has won game (currently requires all mines to be flagged)
        clear(tuple): Recursive function that attempts to clear square indicated 
                    by passed tuple. Autoclears zeros and ends game if square is mined
        play(Tuple[str,int,int]): handles all other logic for guessing 
            (flagging v. clearing, adjusts gameOver etc.). Tuple contains
            guess type, x and y coords of guess.
        FLAGGED: static value of star (*). Indicates squares that have been flagged.
        DEFAULT: static value of dash (-). Indicates squares that has not been cleared or flagged.
    """

    FLAGGED = '*'
    DEFAULT = '-'

    def __init__(self, given_mines=None):
        self.flagged = set()
        self.game_over = 0
        self.mines = []
        self.num_mines = 0
        self.before_first_guess = True
        self.board = [[ '-' ] * 10 for xx in range(10)]
        self.squares = []
        if given_mines is not None:
            self.num_mines = len(list(set(self.mines)))
            self.mines = given_mines
        for ii, jj in _pair_range(10, 10):
            self.squares.append( (ii,jj) )

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
            
    def get_around(self, square):
        """ Returns a list of squares adjacent to the input square."""
        l = [-1,0,1]
        around = []
        for a in l:
            for b in l:
                if 0 > square[0] + a or 9 < square[0] + a \
                or 0 > square[1] + b or 9 < square[1] + b:
                    continue
                around.append( (square[0] + a, square[1] + b) ) 
        return around


    def prettyprint(self):
        """For printing board to user"""
        print('XX' + "0123456789")
        for ii in range(len(self.board)):
            print(str(ii) + ':',end='')
            for ch in self.board[ii]:
                print(ch,end='')
            print('')
            
    def get_count(self,square):
        """accepts tuple inicating target square
        returns number of neighbours in mines list (counts self)
        """
        lst = []
        l = [-1,0,1]
        for ii, jj in itertools.product(l, repeat=2):
            lst.append((square[0] + ii, square[1] + jj))
        return len(set(lst).intersection(set(self.mines)))

    def lose(self):
        """call to lose game"""
        for mine in self.mines:
            self.board[mine[0]][mine[1]] = 'X'
        self.game_over = -1

    def isFirst(self):
        """returns true iff called before the first guess
        TODO: repace with bool
        """
        for row in self.board:
            for item in row:
                if item != self.DEFAULT:
                    return False
        return True

    def winCheck(self):
        """return true iff game has been won"""
        dashes = 0
        bangs = 0
        for row in self.board:
            for square in row:
                if square == self.DEFAULT:
                    dashes += 1
                if square == self.FLAGGED:
                    bangs += 1
        return bangs + dashes == self.num_mines

    def clear(self,tup):
        """Clear indicated square. If square holds zero, 
        recursively call on neighbors to find space.
        """
        l = [-1,0,1]
        lst = []
        num = self.get_count(tup)
        self.board[tup[0]][tup[1]] = str(num)
        if num == 0:
            for ii in l:
                for jj in l:
                    lst.append((tup[0] + ii, tup[1] + jj))
            lst = list(set(lst).intersection(set(self.squares)))
            lst.remove(tup)
            for element in lst:
                if self.board[element[0]][element[1]] == self.DEFAULT:
                    self.clear(element)

    def get_board(self):
        """returns board state"""
        return self.board

    def play(self,tup):
        """ Handles guesses of all (flagging, solveing, clearing) types.
        Bad things here:
            Checks if any given guess is the first (bad).
            'tguess' and 'tup' both needed?
            Returns board status on every call
            Is massive and poorly documented
            Performs setup
            Performs checks using 'board' rather than 'flagged'
            Does a lot of I/O
        """
        tguess = (tup[1],tup[2])
        if self.isFirst():
            """Need to call out first guess so that we don't find a mine"""
            if tup[0] != 'c':
                return (self.game_over, self.board)
            self.setup_mines(tguess)
            if tguess in self.mines:
                self.lose()
                return (self.game_over, self.board)
            self.clear((tup[1],tup[2]))
            if self.winCheck():
                self.game_over = 1
            return ( (self.game_over, self.board) )
        if not self.game_over:            
            """c -> clearing guess"""
            if tup[0] == 'c':
                if self.board[tguess[0]][tguess[1]] != self.DEFAULT:
                    raise BadGuessError("Square targeted flagged or already cleared")
                if tguess in self.mines:
                    self.lose()
                    return (self.game_over, self.board)
                #Not a mine so clear it
                self.clear(tguess)                

            elif tup[0] == 'f':
                """f -> flag guess"""
                if self.board[tguess[0]][tguess[1]] not in [self.FLAGGED,self.DEFAULT]:
                    raise BadGuessError("Targeted square has been cleared")
                elif tguess in self.flagged:
                    self.board[tguess[0]][tguess[1]] = self.DEFAULT
                    self.flagged.remove(tguess)
                elif tguess not in self.flagged:
                    self.flagged.add(tguess)
                    self.board[tguess[0]][tguess[1]] = self.FLAGGED

            elif tup[0] == 's':
                """s -> solve guess"""
                num = self.board[tguess[0]][tguess[1]]
                # If the square is still covered, is flagged or is zero throw the BadGuessError
                if num in ['0','X',self.FLAGGED,self.DEFAULT]:
                    raise BadGuessError("Targeted square cannot be solved")
                # If the square doesn't have enough flagged squares
                if int(num) != len(set(self.get_around(tguess)).intersection(set(self.flagged))):
                    raise BadGuessError("Targeted square cannot be solved")
                adds = [-1,0,1]
                lst = []
                for a in adds:
                    for b in adds:
                        lst.append( (tguess[0] + a, tguess[1] + b) )
                lst.remove(tguess)
                #TODO: list comprehension 
                smines = []
                surround = list(set(self.squares).intersection(set(lst)))
                for s in surround:
                    if self.board[s[0]][s[1]] == self.FLAGGED:
                        smines.append(s)
                if int(num) != len(smines):
                    return (self.game_over,self.board)
                if set(smines).intersection(set(self.mines)) != set(smines):
                    self.lose()
                    return (self.game_over,self.board)
                surround = set(surround).difference(set(self.mines))
                for sq in surround:
                    self.clear(sq)
            if self.winCheck():
                self.game_over = 1
            return ( (self.game_over, self.board) )
