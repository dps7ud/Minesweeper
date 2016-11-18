""" runner.py
A script to play a number of minesweeper games 
TODO: remove unwanted (nearly all) I/O from this file
      get rid of copy of board (called 'info').
"""

import twoms as ms
import random

game = ms.MsGame()
cleared = []
flagged = []


def clear(square):
    """Submits clearing guess to game object"""
    if square in cleared:
        print("Duplicate guess: " + str(square))
        return
    val = game.play(('c',square[0],square[1]))
    cleared.append(square)
    return val


info = clear((5,5))
board = info[1] 


def flag(square):
    """Marked the given square as flagged.
    #TODO: Doesn't work for unflagging
    """
    if square in flagged:
        print("squarele already flagged")
    val = game.play(('f',square[0],square[1]))
    flagged.append(square)
    return val


def solve(square):
    """Submits solving guess to game object.
    TODO: oneliner function
    """
    val = game.play(('s', square[0], square[1]))
    return val


def get_around(square):
    """ Returns a list of squares adjacent to the input square."""
    l = [-1,0,1]
    around = []
    for a in l:
        for b in l:
            if 0 > square[0] + a or 9 < square[0] + a or 0 > square[1] + b or 9 < square[1] + b:
                continue
            around.append( (square[0] + a, square[1] + b) ) 
    return around


def retreive(square, board):
    """find character at tuple"""
    return board[square[0]][square[1]]


"""The first guess is always to clear 5,5. if this guess does not
result in an opening, we guess randomly until we get an opening or
we lose
"""
while not info[0]:
    shown = set([])
    for row in board:
        shown = shown.union(set(row))
    if '0' in shown:
        break
    else:
        x = 0
        y = 0
        #TODO: Need all these conditions?
        while ( (x,y) in flagged + cleared ) or ( board[x][y] != '-'):
            x = random.randint(0,9)
            y = random.randint(0,9)
        info = clear((x,y))
lst = [ [] for x in range(8)]
changed = 1

""" If the algorithm below does not change anything, we must guess.
"""
while not info[0]:
    print(changed)
    if not changed:
        print("hung")
        break
    changed = 0
    """Finds all nonzero cleared squares and inspects surrounding squares"""
    for ii in range(10):
        for jj in range(10):
            c = retreive((ii,jj), board)
            if c in ['*','-','0']:
                continue
            else:
                n = int(c)
                around = get_around((ii,jj))
                around.remove( (ii,jj) )
                hidden = []
                flagCount = 0
                for a in around:
                    sym = retreive(a,board)
                    if sym == '-':
                        hidden.append(a)
                    elif sym == '*':
                        flagCount += 1
                """If there are only as many squares touching 'a' as there are
                mines around 'a', we can flag everything"""
                if len(hidden) + flagCount == n and len(hidden) > 0:
                    for h in hidden:
                        info = flag(h)
                        board = info[1]
                    changed = 2
    """Finds all nonzero cleared squares and inspects surrounding squares"""
    for ii in range(10):
        for jj in range(10):
            c = retreive((ii,jj), board)
            if c in ['*','0','-']:
                continue
            n = int(c)
            around = get_around( (ii,jj))
            around.remove( (ii,jj) )
            flagCount = 0
            hiddenCount = 0
            for a in around:
                sym = retreive(a,board)
                if sym == '*':
                    flagCount += 1
                if sym == '-':
                    hiddenCount += 1
            """If all surrounding mines are flagged, and there are unchecked squares,
            check everythin"""
            if flagCount == n and hiddenCount != 0:
                if info[0]:
                    break
                info = solve( (ii,jj))
                changed = 3
                board = info[1]
if info[0] == -1:
    print("Lost")
elif info[0] == 1:
    print("Won")
