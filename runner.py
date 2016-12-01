""" runner.py
A script to play a number of minesweeper games 
"""

import ms
import random

def _pair_range(len_outter, len_inner):
    """Produces all pairs 0..len_outter - 1, 0..len_inner - 1"""
    for ii in range(len_outter):
        for jj in range(len_inner):
            yield ii, jj

class Player:

    def __init__(self, given_mines=None):
        self.changed = True
        self.game_over = 0
        self.cleared = set()
        if given_mines is not None:
            self.game = ms.MsGame(given_mines)
        else:
            self.game = ms.MsGame()
        self.board = self.game.get_board()

    def clear(self, square):
        """Submits clearing guess to game object"""
        #print("square :", square)
        if square in self.cleared:
            raise ms.BadGuessError("newrunner: 22")
        val = self.game.play(('c',square[0],square[1]))
        self.cleared.add(square)
        return val
    
    
    def flag(self, square):
        """Flag (if not flagged) or unflag (if flagged) given square"""
        val = self.game.play(('f',square[0],square[1]))
        return val
    
    
    def retreive(self, square, board):
        """find character at tuple"""
        return self.board[square[0]][square[1]]
    
    
    def solve(self, square):
        """Submits solving guess to game object.
        """
        print("Solving:  ", square)
        val = self.game.play(('s', square[0], square[1]))
        return val

    def cleanup(self):
        self.game.prettyprint()

    def run_game(self):
        """Runs the game"""
        first_guess()
        if not self.game_over:
            self.later_guesses()
        self.cleanup()

    def first_guess(self):
        """The first guess is always to clear 5,5. if this guess does not
        result in an opening, we guess randomly until we get an opening or
        we lose
        """
        self.game_over = self.clear((5,5))[0]
        self.game.prettyprint()
        with open("mines.txt",'a') as output:
            output.write(str(self.game.mines) + '\n')
        #print(self.game.mines)
        self.board = self.game.get_board()
        shown = set()
        for row in self.board:
            shown = shown.union(set(row))
        print("shown: ",shown)
        x = random.randint(0,9)
        y = random.randint(0,9)
        while '0' not in shown and not self.game_over:
            while ( (x,y) in self.game.flagged.union( self.cleared ) 
                or (self.board[x][y] != '-') ):
                x = random.randint(0,9)
                y = random.randint(0,9)
            print("x, y", x, y)
            self.game_over = self.clear((x,y))[0]
            self.game.prettyprint()
            self.board = self.game.get_board()
            for row in self.board:
                shown = shown.union(set(row))
            print("shown: ",shown)

    def later_guesses(self):
        self.game.prettyprint()
        print("--------------------")
        while not self.game_over:
            self.game.prettyprint()
            if not self.changed:
                print("hung")
                break
            self.changed = False
            """Finds all nonzero cleared squares and inspects surrounding squares"""
            for (ii,jj) in _pair_range(10, 10):
            #for ii in range(10):
            #    for jj in range(10):
                character = self.retreive((ii,jj), self.board)
                if character in ['X','*','-','0']:
                    continue
                else:
                    number = int(character)
                    around = self.game.get_around((ii,jj))
                    around.remove( (ii,jj) )
                    hidden = []
                    flagCount = 0
                    for a in around:
                        sym = self.retreive(a,self.board)
                        if sym == '-':
                            hidden.append(a)
                        elif sym == '*':
                            flagCount += 1
                    """If there are only as many squares touching 'a' as there are
                    mines around 'a', we can flag everything"""
                    if len(hidden) + flagCount == number and len(hidden) > 0:
                        for h in hidden:
                            self.game_over = self.flag(h)[0]
                            self.board = self.game.get_board()
                        self.changed = True
            """Finds all nonzero cleared squares and inspects surrounding squares"""
            for (ii,jj) in _pair_range(10, 10):
            #for ii in range(10):
            #    for jj in range(10):
                character = self.retreive((ii,jj), self.board)
                if character in ['*','0','-']:
                    continue
                number = int(character)
                around = self.game.get_around( (ii,jj))
                around.remove( (ii,jj) )
                flagCount = 0
                hiddenCount = 0
                for a in around:
                    sym = self.retreive(a,self.board)
                    if sym == '*':
                        flagCount += 1
                    if sym == '-':
                        hiddenCount += 1
                """If all surrounding mines are flagged, and there are unchecked squares,
                check everythin"""
                if flagCount == number and hiddenCount != 0:
                    if self.game_over:
                        break
                    self.game_over = self.solve((ii,jj))[0]
                    self.board = self.game.get_board()
                    self.changed = True
        if self.game_over == -1:
            self.game.prettyprint()
            print("Lost")
        elif self.game_over == 1:
            self.game.prettyprint()
            print("Won")
