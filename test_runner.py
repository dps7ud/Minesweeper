import newrunner as nr

with open('mines.txt','r') as input_file:
    k = input_file.readline()
#lst = eval(k)
#p = nr.Player(lst)
p = nr.Player()
p.first_guess()
p.later_guesses()
