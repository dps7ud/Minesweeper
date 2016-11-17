""" Play minesweeper
Guess Format:
  c 0,9 - check the square at 0,9
  f 9,0 - flag the square at 9,0
  s 5,5 - solve the square at 5,5. This is equivalent to 
               the double press on microsoft minesweeper.
  The first guess must be of the "check" variety. 
"""

import re
import twoms as ms

def verify(guess_string):
    """ Verifies proper guess input"""
    guess_string = guess_string.strip()
    regex = '^(f|c|s)\s\d[,]\d$'
    return bool(re.findall(regex,guess_string))

game = ms.MsGame()
game_over = False
while not game_over:
    guess = ''
    while not verify(guess):
        guess = input("Enter guess: ").lower().strip()
    guess_to_pass = tuple(guess.replace(' ',',').split(','))
    guess_to_pass = (guess_to_pass[0],int(guess_to_pass[1]), int(guess_to_pass[2]))
    print(guess_to_pass)
    game_over = game.play(guess_to_pass)[0] or game.winCheck()
