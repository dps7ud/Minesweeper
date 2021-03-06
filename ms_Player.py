""" runner.py
A script to play a number of minesweeper games 
"""

import minesweeper as ms
import random

def _pair_range(len_outter, len_inner):
    """Produces all pairs 0..len_outter - 1, 0..len_inner - 1"""
    for ii in range(len_outter):
        for jj in range(len_inner):
            yield ii, jj

class Player:
    """Methods:
       clear(square) -- attempts to clear given square
       flag(square) -- attempts to flag given square
       flag_all(square) -- Flag everything possible
       retreive(square) -- gets the character at the given square
       solve(square) -- attempts to solve given square
       solve_all(square) -- solve everything possible
       cleanup() -- runs various cleanup processes. May later include 
           scorekeeping or other stats
       run_game() -- call to play one game to completion
       first_guess() -- guesses ('c',5,5) and random clearing guesses 
           until an 'opening' is found
       later_guesses() -- keeps guessing until end of game.

       Fields:
       changed: True whenever progress has been made. Used to detect if game
            requires patters or guessing.
       game_over: indicates if game is over or not
       verbose: indicates if data to stdout is wanted
    """
    def __init__(self, given_mines=None, seed=None, verbose=False):
        """Initializer, takes optional mine arguments"""
        self.changed = True
        self.game_over = 0
        self.verbose = verbose
        random.seed(seed)
        if given_mines is not None:
            self.game = ms.MsGame(given_mines)
        else:
            self.game = ms.MsGame()

    def ambigious(self):
        """For games where progress cannot otherwise be made,
        a series of other checks will be made:
        if all mines are flagged, clear everything else
        """
        #Game hung, implement strats later
        if self.verbose:
            self.game.prettyprint()
            print("hung")
        if len(self.game.flagged) == self.game.num_mines:
            to_clear = self.game.squares.difference( self.game.flagged.union(self.game.cleared) )
            for square in to_clear:
                self.game_over = self.clear(square)
                self.changed = True
        else:
            #For now, make a random choice
            not_cleared = self.game.squares.difference(self.game.cleared.union(self.game.flagged))
            rand_guess = random.sample(not_cleared, 1)[0]
            self.game_over = self.clear(rand_guess)
            self.changed = True

    def clear(self, square):
        """Submits clearing guess to game object"""
        val = self.game.clear(square)
        return val
 
    def flag(self, square):
        """Flag (if not flagged) or unflag (if flagged) given square"""
        val = self.game.flag(square)
        return val
 
    def flag_all(self):
        """Finds all nonzero cleared squares and inspects surrounding squares"""
        for square in self.game.cleared:
            character = self.retreive(square)
            if character != '0':
                number = int(character)
                around = self.game.squares_around(square)
                around.remove(square)
                hidden = set()
                flagCount = 0
                for a in around:
                    sym = self.retreive(a)
                    if sym == '-':
                        hidden.add(a)
                    elif sym == '*':
                        flagCount += 1
                """If there are only as many squares touching 'a' as there are
                mines around 'a', we can flag everything"""
                if len(hidden) + flagCount == number and len(hidden) > 0:
                    for h in hidden:
                        self.game_over = self.flag(h)
                    self.changed = True

    def retreive(self, square):
        """find character at tuple"""
        return self.game.board[ square[0] ][ square[1] ]
    
    def solve(self, square):
        """Submits solving guess to game object"""
        val = self.game.solve(square)
        return val

    def cleanup(self):
        """If verbose, print info"""
        if self.verbose:
            self.game.prettyprint()
            if self.game_over == -1:
                print("Lost")
            elif self.game_over == 1:
                print("Won")
        pass

    def run_game(self):
        """Runs the game"""
        self.first_guess()
        if not self.game_over:
            self.later_guesses()
        self.cleanup()

    def first_guess(self):
        """The first guess is always to clear 5,5. if this guess does not
        result in an opening, we guess randomly until we get an opening or
        we lose
        """
        self.game_over = self.game.first_guess( ('c',5,5) )
        shown = set()
        for row in self.game.board:
            shown = shown.union(set(row))
        x = random.randint(0,9)
        y = random.randint(0,9)
        while '0' not in shown and not self.game_over:
            while ( (x,y) in self.game.flagged.union( self.game.cleared ) 
                or (self.game.board[x][y] != '-') ):
                x = random.randint(0,9)
                y = random.randint(0,9)
            self.game_over = self.clear((x,y))
            for row in self.game.board:
                shown = shown.union(set(row))

    def solve_all(self):
        """For (non-zero) cleared squares, if all nearby 
        mines are flagged, solve the input square"""
        #Look at COPY of cleared since the origional is mutated
        cleared_freeze = self.game.cleared.copy()
        for square in cleared_freeze:
            character = self.retreive(square)
            if character != '0':
                number = int(character)
                around = self.game.squares_around(square)
                around.remove(square)
                flag_count = len(around.intersection(self.game.flagged))
                hidden_count = len(around) - flag_count
                hidden_count -= len(around.intersection(self.game.cleared))
                """If all surrounding mines are flagged, and there are unchecked squares,
                check everything"""
                if flag_count == number and hidden_count != 0:
                    self.game_over = self.solve(square)
                    self.changed = True

    def later_guesses(self):
        """Main loop"""
        while not self.game_over:
            if not self.changed:
                self.ambigious()
                if not self.changed:
                    break 
                continue
                #TODO: Sloppy. Find a better way.
            self.changed = False
            self.flag_all()
            self.solve_all()
