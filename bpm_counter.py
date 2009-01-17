#!/usr/bin/env python
from time import *

import curses
stdscr = curses.initscr()
curses.noecho()                 # do not show the keys
curses.cbreak()                 # react to keys without Carriage return
stdscr.keypad(1)                # return nice keyboard 

t0 = clock()
while 1:
    c = stdscr.getch()
    if c == ord('n'): t=clock();break
    elif c == ord('q'): break  # Exit the while()

print "clock:", t - t0

print "otto was here  !"

sleep(10)

# while 1:
#     c = stdscr.getch()
#     if c == ord('q'): break

# the end, reversing the keyboard stuff
curses.nocbreak(); stdscr.keypad(0); curses.echo()
curses.endwin()                 # restore everything
