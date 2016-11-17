"""Minesweeper.py
Classes:
    msGame - object holding all game related information
"""
import random
import re

#Contains minesweeper game class and a function to varify inputs (move latter?)

def verify(s):
    #Checks syntax of guesses
    s = s.strip()
    ex = '^(f|c|s)\s\d[,]\d$'
    return (len(re.findall(ex,s)) != 0)
class msGame:
    """Fields:
        gameOver: binary indicating if game is over (True) or can be played (False)
        squares: list of tuples of valid board squares 
            (useful for not picking out of bounds squares)
        mines: list of tuples indicating positions of mines
        board: List of lists holding all apperance information 
            (flagged squares, cleared squares etc.)
    Methods:
        __init__(): populates self.squares and prints initial blank board
        verify(str): verifies syntax of string (user guesses) --unused?
        prettypg(): prints board for user consumption
        pg(): print board for debugging (unused)
        getCount(tuple): counts mines touching the square indicated by passed tuple
        lose(): ends game in loss
        isFirst(): Checks if board is fresh (returns True) or not (returns False)
        winCheck(): Checks if user has won game (currently requires all mines to be flagged)
        clear(tuple): Recursive function that attempts to clear square indicated by passed tuple. Autoclears zeros and ends game if square is mined
        play(Tuple[str,int,int]): handles all other logic for guessing 
            (flagging v. clearing, adjusts gameOver etc.). Tuple contains
            guess type, x and y coords of guess.
    """
    gameOver = False
    squares = []
    mines = []
    board = [['-'] * 10 for xx in range(10)]
    def __init__(self):
        for ii in range(10):
            for jj in range(10):
                self.squares.append( (ii,jj) )
        self.prettypg()
    def verify(self,s):
        #Checks syntax of guesses
        s = s.strip()
        ex = '^(f|c)\s\d[,]\d$'
        return (len(re.findall(ex,s)) != 0)
    def prettypg(self):
        #For printing board to user
        print('XX' + "0123456789")
        #print('XX==========')
        for ii in range(len(msGame.board)):
            print(str(ii) + ':',end='')
            for ch in msGame.board[ii]:
                print(ch,end='')
            print('')
    def pg():
        #For printing in debugging
        for row in msGame.board:
            print(row)
    def getCount(self,tup):
        #accepts tuple inicating square to count
        #returns number of neighbours in mines list (counts self)
        lst = []
        l = [-1,0,1]
        for ii in l:
            for jj in l:
                lst.append((tup[0] + ii, tup[1] + jj))
        return len(set(lst).intersection(set(msGame.mines)))
#note: board = [['-'] * 10] * 10 gives 10 copies of the same list (bad) instead...
    def lose(self):
        for mine in msGame.mines:
            msGame.board[mine[0]][mine[1]] = 'X'
        self.prettypg()
        print("Game Over")
        msGame.gameOver = -1
    def isFirst(self):
        for row in msGame.board:
            for item in row:
                if item != '-':
                    return False
        return True
    def winCheck(self):
        dashes = 0
        bangs = 0
        for row in msGame.board:
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
        msGame.board[tup[0]][tup[1]] = str(num)
        if num == 0:
            for ii in l:
                for jj in l:
                    lst.append((tup[0] + ii, tup[1] + jj))
            lst = list(set(lst).intersection(set(msGame.squares)))
            lst.remove(tup)
            #prettypg()
            #print(tup)
            #print(lst)
            #input()
            for element in lst:
                if msGame.board[element[0]][element[1]] == '-':
                    self.clear(element)
    def play(self,tup):
        # instructions = """Flag squares using the following syntax: \'f 0,9\'
        # Check squares using the following syntax: \'c 9,0\'"""
        # start = "The first guess must be a checking guess (not a flagging guess)"
        # print(instructions)
        # print(start)
        #prettypg()

        # guess = ''
        # while not (verify(guess) and guess.startswith('c')):
            # guess = input("Enter guess: ").lower().strip()
        tguess = (tup[1],tup[2])
        if self.isFirst():
            if tup[0] != 'c':
                return (gameOver, board)
            for ii in range(10):
                x = random.randint(0,9)
                y = random.randint(0,9)
                while (x,y) in msGame.mines or (x,y) == tguess:
                    x = random.randint(0,9)
                    y = random.randint(0,9)
                msGame.mines.append((x,y))
            print(msGame.mines)
            self.clear((tup[1],tup[2]))
            self.prettypg()
            if self.winCheck():
                print("1Game over, you win!")
                msGame.gameOver = 1
            return ( (msGame.gameOver, msGame.board) )
        if not msGame.gameOver:            
            if tup[0] == 'c':#Clearing guess
                if msGame.board[tguess[0]][tguess[1]] != '-':
                    print("Pick a different square")
                    return (msGame.gameOver, msGame.board)
                if tguess in msGame.mines:
                    self.lose()
                    return (msGame.gameOver, msGame.board)
                #Not a mine
                self.clear(tguess)                
            elif tup[0] == 'f':# Flagging guess
                if msGame.board[tguess[0]][tguess[1]] == '*':
                    msGame.board[tguess[0]][tguess[1]] = '-'
                    #print(msGame.board[tguess[0]][tguess[1]])
                    
                elif msGame.board[tguess[0]][tguess[1]] == '-':
                    msGame.board[tguess[0]][tguess[1]] = '*'
                if msGame.board[tguess[0]][tguess[1]] not in ['*','-']:
                    print("Pick a different square")                
                #return (msGame.gameOver, msGame.board)
            elif tup[0] == 's':
                num = msGame.board[tguess[0]][tguess[1]]
                if num in ['X','*','-']:
                    print("One of X*-")
                    return (msGame.gameOver, msGame.board)
                adds = [-1,0,1]
                lst = []
                for a in adds:
                    for b in adds:
                        lst.append( (tguess[0] + a, tguess[1] + b) )
                lst.remove(tguess)
                smines = []
                surround = list(set(msGame.squares).intersection(set(lst)))
                for s in surround:
                    if msGame.board[s[0]][s[1]] == '*':
                        smines.append(s)
                if int(num) != len(smines):
                    print("174: mines surrounding != number in square")
                    return (msGame.gameOver,msGame.board)
                if set(smines).intersection(set(msGame.mines)) != set(smines):
                    self.lose()
                    return (msGame.gameOver,msGame.board)
                surround = set(surround).difference(set(msGame.mines))
                print("surround" + str(surround))
                for sq in surround:
                    self.clear(sq)
            self.prettypg()
            if self.winCheck():
                print("2Game over, you win!")
                msGame.gameOver = 1
            return ( (msGame.gameOver, msGame.board) )

