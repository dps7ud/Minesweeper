"""Minesweeper.py
Class: MsGame - object holding all game related information
"""

import random
import re

def pair_range(len_out, len_in):
    """Produces all pairs 0..len_out - 1, 0..len_in - 1"""
    for ii in range(len_out):
        for jj in range(len_in):
            yeild ii,jj

class MsGame:
    """Fields:
        board: List of lists holding all apperance information 
                    (flagged squares, cleared squares etc.)
        gameOver: binary indicating if game is over (True) or can be played (False)
        mines: list of tuples indicating positions of mines
        squares: list of tuples of valid board squares 
                    (useful for not picking out of bounds squares)
    Methods:
        __init__(): populates self.squares and prints initial blank board
        prettyprint(): prints board for user consumption
        getCount(tuple): counts mines touching the square indicated by passed tuple
        lose(): ends game in loss
        isFirst(): Checks if board is fresh (returns True) or not (returns False)
        winCheck(): Checks if user has won game (currently requires all mines to be flagged)
        clear(tuple): Recursive function that attempts to clear square indicated 
                    by passed tuple. Autoclears zeros and ends game if square is mined
        play(Tuple[str,int,int]): handles all other logic for guessing 
            (flagging v. clearing, adjusts gameOver etc.). Tuple contains
            guess type, x and y coords of guess.
    """

    board = [['-'] * 10 for xx in range(10)]
    gameOver = False
    mines = []
    squares = []

    def __init__(self):
        for ii, jj in pair_range(10, 10):
            self.squares.append( (ii,jj) )
        self.prettyprint()

    def prettyprint(self):
        """For printing board to user"""
        print('XX' + "0123456789")
        #print('XX==========')
        for ii in range(len(MsGame.board)):
            print(str(ii) + ':',end='')
            for ch in MsGame.board[ii]:
                print(ch,end='')
            print('')
            
    def getCount(self,tup):
        #accepts tuple inicating square to count
        #returns number of neighbours in mines list (counts self)
        lst = []
        l = [-1,0,1]
        for ii in l:
            for jj in l:
                lst.append((tup[0] + ii, tup[1] + jj))
        return len(set(lst).intersection(set(MsGame.mines)))
#note: board = [['-'] * 10] * 10 gives 10 copies of the same list (bad) instead...
    def lose(self):
        for mine in MsGame.mines:
            MsGame.board[mine[0]][mine[1]] = 'X'
        self.prettyprint()
        print("Game Over")
        MsGame.gameOver = -1
    def isFirst(self):
        for row in MsGame.board:
            for item in row:
                if item != '-':
                    return False
        return True
    def winCheck(self):
        dashes = 0
        bangs = 0
        for row in MsGame.board:
            for square in row:
                if square == '-':
                    dashes += 1
                if square == '*':
                    bangs += 1
        return bangs + dashes == 10
    def clear(self,tup):
        l = [-1,0,1]
        lst = []
        num = self.getCount(tup)
        MsGame.board[tup[0]][tup[1]] = str(num)
        if num == 0:
            for ii in l:
                for jj in l:
                    lst.append((tup[0] + ii, tup[1] + jj))
            lst = list(set(lst).intersection(set(MsGame.squares)))
            lst.remove(tup)
            #print(tup)
            #print(lst)
            #input()
            for element in lst:
                if MsGame.board[element[0]][element[1]] == '-':
                    self.clear(element)
    def play(self,tup):
        # instructions = """Flag squares using the following syntax: \'f 0,9\'
        # Check squares using the following syntax: \'c 9,0\'"""
        # start = "The first guess must be a checking guess (not a flagging guess)"
        # print(instructions)
        # print(start)
        #prettyprint()
        tguess = (tup[1],tup[2])
        if self.isFirst():
            if tup[0] != 'c':
                return (gameOver, board)
            for ii in range(10):
                x = random.randint(0,9)
                y = random.randint(0,9)
                while (x,y) in MsGame.mines or (x,y) == tguess:
                    x = random.randint(0,9)
                    y = random.randint(0,9)
                MsGame.mines.append((x,y))
            print(MsGame.mines)
            self.clear((tup[1],tup[2]))
            self.prettyprint()
            if self.winCheck():
                print("1Game over, you win!")
                MsGame.gameOver = 1
            return ( (MsGame.gameOver, MsGame.board) )
        if not MsGame.gameOver:            
            if tup[0] == 'c':#Clearing guess
                if MsGame.board[tguess[0]][tguess[1]] != '-':
                    print("Pick a different square")
                    return (MsGame.gameOver, MsGame.board)
                if tguess in MsGame.mines:
                    self.lose()
                    return (MsGame.gameOver, MsGame.board)
                #Not a mine
                self.clear(tguess)                
            elif tup[0] == 'f':# Flagging guess
                if MsGame.board[tguess[0]][tguess[1]] == '*':
                    MsGame.board[tguess[0]][tguess[1]] = '-'
                    #print(MsGame.board[tguess[0]][tguess[1]])
                    
                elif MsGame.board[tguess[0]][tguess[1]] == '-':
                    MsGame.board[tguess[0]][tguess[1]] = '*'
                if MsGame.board[tguess[0]][tguess[1]] not in ['*','-']:
                    print("Pick a different square")                
                #return (MsGame.gameOver, MsGame.board)
            elif tup[0] == 's':
                num = MsGame.board[tguess[0]][tguess[1]]
                if num in ['X','*','-']:
                    print("One of X*-")
                    return (MsGame.gameOver, MsGame.board)
                adds = [-1,0,1]
                lst = []
                for a in adds:
                    for b in adds:
                        lst.append( (tguess[0] + a, tguess[1] + b) )
                lst.remove(tguess)
                smines = []
                surround = list(set(MsGame.squares).intersection(set(lst)))
                for s in surround:
                    if MsGame.board[s[0]][s[1]] == '*':
                        smines.append(s)
                if int(num) != len(smines):
                    print("174: mines surrounding != number in square")
                    return (MsGame.gameOver,MsGame.board)
                if set(smines).intersection(set(MsGame.mines)) != set(smines):
                    self.lose()
                    return (MsGame.gameOver,MsGame.board)
                surround = set(surround).difference(set(MsGame.mines))
                print("surround" + str(surround))
                for sq in surround:
                    self.clear(sq)
            self.prettyprint()
            if self.winCheck():
                print("2Game over, you win!")
                MsGame.gameOver = 1
            return ( (MsGame.gameOver, MsGame.board) )

