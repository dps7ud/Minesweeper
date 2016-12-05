Minesweeper CLI Game
====================

This repository holds a command line version of Minesweeper in some state of (un)completion. 
I've decided that making everything here less horrible is enough of a project that 
I would like to keep track of it here. 
The code will be committed as it currently lives on my disk and we'll see how far I get
before I hate myself too much to continue.
I'll include a brief to-do list here since it seems overkill to raise issues.

Cleanup:
--------

- [x] Commit everything
- [x] Put in good comments
- [x] Take out bad comments
- [x] Read PEP8 again and everything in this repository
- [x] Try not to cry 
- [x] Stop using debug.py to test things and write a real goddamn test suite
- [x] Refactor runner.py into a class rather than a script
- [x] Refactor communication between 'ms' module and runner/debug 
- [x] Rewrite entire 'play' method
- [ ] Rename pretty much everything
- [ ] Stop keeping track of board data in two places (runner and ms)

Features:
---------

- [x] Refactor I/O to importing classes (minesweeper module)
- [ ] Allow MsGame to accept a specific random seed to get reproducible tests
- [ ] Finish games that are a tossup
- [ ] Refactor gameover mechanics
- [ ] Variable board size, number of mines and number of runs for runner
- [ ] Implement pattern matching for common patterns (1-2-1, 1-1, 1-2)
- [ ] Silent mode
- [ ] Keep stats
- [ ] Optomize clearing strategy
- [ ] Optomize guessing strategy
- [ ] Add more dimensions
