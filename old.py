#CLI ms game
import random
import re

#Holds all squares for intersection with clearing functions
squares = []
for ii in range(10):
    for jj in range(10):
        squares.append( (ii,jj) )
#def clear(tup):
def verify(s):
    #Checks syntax of guesses
    s = s.strip()
    ex = '^(f|c)\s\d[,]\d$'
    return (len(re.findall(ex,s)) != 0)
def prettypg():
    #For printing board to user
    print('XX' + "0123456789")
    #print('XX==========')
    for ii in range(len(board)):
        print(str(ii) + ':',end='')
        for ch in board[ii]:
            print(ch,end='')
        print('')
def pg():
    #For printing in debugging
	for row in board:
		print(row)
def getCount(tup):
    #accepts tuple inicating square to count
    #returns number of neighbours in mines list (counts self)
    lst = []
    l = [-1,0,1]
    for ii in l:
        for jj in l:
            lst.append((tup[0] + ii, tup[1] + jj))
    return len(set(lst).intersection(set(mines)))
#note: board = [['-'] * 10] * 10 gives 10 copies of the same list (bad) instead...
def lose():
    for mine in mines:
        board[mine[0]][mine[1]] = '*'
    prettypg()
    print("Game Over")
    exit(0)
def winCheck():
    dashes = 0
    bangs = 0
    for row in board:
        for square in row:
            if square == '-':
                dashes += 1
            if square == '!':
                bangs += 1
    return bangs <= 10 and dashes == 0
def clear(tup):
    l = [-1,0,1]
    lst = []
    num = getCount(tup)
    board[tup[0]][tup[1]] = str(num)
    if num == 0:
        for ii in l:
            for jj in l:
                lst.append((tup[0] + ii, tup[1] + jj))
        lst = list(set(lst).intersection(set(squares)))
        lst.remove(tup)
        #prettypg()
        #print(tup)
        #print(lst)
        #input()
        for element in lst:
            if board[element[0]][element[1]] == '-':
                clear(element)
        
board = [['-'] * 10 for xx in range(10)]
instructions = """Flag squares using the following syntax: \'f 0,9\'
Check squares using the following syntax: \'c 9,0\'"""
start = "The first guess must be a checking guess (not a flagging guess)"
print(instructions)
print(start)
prettypg()

guess = ''
while not (verify(guess) and guess.startswith('c')):
    guess = input("Enter guess: ").lower().strip()
tguess = tuple([int(x) for x in guess[2:].split(',')])
mines = []
for ii in range(10):
    x = random.randint(0,9)
    y = random.randint(0,9)
    while (x,y) in mines or (x,y) == tguess:
        x = random.randint(0,9)
        y = random.randint(0,9)
    mines.append((x,y))
    #print(mines)
print(mines)
clear(tguess)
prettypg()

#TODO: Win conditions
gameOver = False
while not gameOver:
    guess = ''
    while not verify(guess):
        guess = input("Enter guess: ").lower().strip()
    tguess = tuple([int(x) for x in guess[2:].split(',')])
    
    if guess.startswith('c'):#Clearing guess
        if board[tguess[0]][tguess[1]] != '-':
            print("Pick a different square")
            continue
        if tguess in mines:
            lose()
        #Not a mine
        clear(tguess)
        num = getCount(tguess)
        board[tguess[0]][tguess[1]] = str(num)
        #TODO: implement autoclearing for zero squares
        
    else:# Flagging guess
        if board[tguess[0]][tguess[1]] == '!':
            board[tguess[0]][tguess[1]] = '-'
        if board[tguess[0]][tguess[1]] == '-':
            board[tguess[0]][tguess[1]] = '!'
        if board[tguess[0]][tguess[1]] not in ['!','-']:
            print("Pick a different square")
            continue
    prettypg()
    if winCheck():
        print("Game over, you win!")
        gameOver = True
