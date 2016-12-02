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
        before_first_guess: bool indicating if the first guess has been made
        board: List of lists holding all apperance information 
                    (flagged squares, cleared squares etc.)
        flagged: set of tuples indicating squares that have been flagged
        game_over: int indicating if game is over (win:1 lose:-1) or can be played (0)
        mines: list of tuples indicating positions of mines
        num_mines: integer indicating number of mines present
        squares: list of tuples of valid board squares 
                    (useful for not picking out of bounds squares)
        FLAGGED: static value of star (*). Indicates squares that have been flagged.
        DEFAULT: static value of dash (-). Indicates squares that has not been cleared or flagged.
    Methods:
        __init__(): populates self.squares and possibly other options. Initializes all instance
            variables.
        get_around(square): returns all squares surrounding the given square
        get_board(): returns current board state
        get_count(tuple): counts mines touching the square indicated by passed tuple
        clear(tuple): Recursive function that attempts to clear square indicated 
                    by passed tuple. Autoclears zeros and ends game if square is mined
        first_guess( tuple(str, int, int) ): makes first guess
        lose(): ends game in loss
        play( tuple(str,int,int) ): handles all other logic for guessing 
            (flagging v. clearing, adjusts game_over etc.). Tuple contains
            guess type, x and y coords of guess.
        prettyprint(): prints board for user consumption
        setup_mines(): sets up mines after first guess in the case that 
            no list of mines was passed
        win_check(): Checks if user has won game (currently requires all mines to be flagged)
    """

    FLAGGED = '*'
    DEFAULT = '-'

    def __init__(self, given_mines=None):
        self.before_first_guess = True
        self.board = [[ '-' ] * 10 for xx in range(10)]
        self.flagged = set()
        self.cleared = set()
        self.game_over = 0
        self.mines = []
        self.num_mines = 0
        self.squares = set()

        if given_mines is not None:
            self.num_mines = len(list(set(self.mines)))
            self.mines = given_mines
        for ii, jj in _pair_range(10, 10):
            self.squares.add( (ii,jj) )

    def get_around(self, square):
        """ Returns a set of squares adjacent to the input square,
        including the input square.
        """
        l = (-1,0,1)
        around = set()
        for aa in l:
            for bb in l:
                around.add( (square[0] + aa, square[1] + bb) ) 
        around = around.intersection(self.squares)
        return around

    def get_board(self):
        """returns board state"""
        return self.board

    def get_count(self,square):
        """accepts tuple inicating target square
        returns number of neighbours in mines list (counts self)
        """
        lst = []
        l = [-1,0,1]
        for ii, jj in itertools.product(l, repeat=2):
            lst.append((square[0] + ii, square[1] + jj))
        return len(set(lst).intersection(set(self.mines)))

    def clear(self, tguess):
        """Clear indicated square. If square holds zero, 
        recursively call on neighbors to find space.
        """
        if self.board[tguess[0]][tguess[1]] != self.DEFAULT:
            raise BadGuessError("Targeted square is flagged or already cleared")
        if tguess in self.mines:
            self.lose()
            return self.game_over
        self.cleared.add(tguess)

        #Not a mine so clear it
        to_clear = self.get_around(tguess)
        num = self.get_count(tguess)
        self.board[tguess[0]][tguess[1]] = str(num)
        if num == 0:
            to_clear = list(set(to_clear).intersection(self.squares))
            to_clear.remove(tguess)
            for element in to_clear:
                if element not in self.cleared:
                    self.clear(element)
                    
    def first_guess(self, tup):
        """Makes first guess of any game"""
        if tup[0] != 'c':
            return self.game_over
        tguess = (tup[1],tup[2])
        #Since tup[0] == 'c' we know the board will be changed
        self.before_first_guess = False
        self.setup_mines(tguess)
        #Following check required for games with constructed mines
        if tguess in self.mines:
            self.lose()
            return self.game_over
        self.clear(tguess)
        if self.win_check():
            self.game_over = 1
        return self.game_over

    def lose(self):
        """call to lose game"""
        for mine in self.mines:
            self.board[mine[0]][mine[1]] = 'X'
        self.game_over = -1

    def play(self, tup):
        """ Handles guesses of all (flagging, solveing, clearing) types.
        Bad things here:
            'tguess' and 'tup' both needed?
            Is massive and poorly documented
            Performs checks using 'board' rather than 'flagged'
        """
        tguess = (tup[1],tup[2])
        if not self.game_over:            
            """c -> clearing guess"""
            if tup[0] == 'c':
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
                if int(num) != len(self.get_around(tguess).intersection(self.flagged)):
                    raise BadGuessError("Targeted square cannot be solved")
                adds = [-1,0,1]
                lst = []
                for a in adds:
                    for b in adds:
                        lst.append( (tguess[0] + a, tguess[1] + b) )
                lst.remove(tguess)
                #TODO: list comprehension 
                smines = []
                surround = list(self.squares.intersection(set(lst)))
                for s in surround:
                    if self.board[s[0]][s[1]] == self.FLAGGED:
                        smines.append(s)
                #Duplicate test to above
                if int(num) != len(smines):
                    return self.game_over
                if set(smines).intersection(set(self.mines)) != set(smines):
                    self.lose()
                    return self.game_over
                surround = set(surround).difference(set(self.mines))
                for sq in surround:
                    if sq not in self.cleared:
                        self.clear(sq)
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

    def win_check(self):
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

