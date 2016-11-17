#Import and instantiate game object
import twoms as ms
game = ms.msGame()
#Begin game loop
gameOver = False
while not gameOver:
    #Take input and verify
    guess = ''
    while not ms.verify(guess):
        guess = input("Enter guess: ").lower().strip()
    #Messy parsing user input -> game-usable data
    tguess = tuple(guess.replace(' ',',').split(','))
    tguess = (tguess[0],int(tguess[1]), int(tguess[2]))
    print(tguess)
    #Pass guess to game object.
    #game.play returns a tuple with the following components:
    #   [0] binary T/F indicating if game is over
    #   [1] List of lists representing board object
    gameOver = game.play(tguess)[0]
    if game.winCheck():
        gameOver = True
