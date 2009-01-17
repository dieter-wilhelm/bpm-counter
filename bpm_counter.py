#!/usr/bin/env python

# TODO: 
# restore terminal -> exception?
# standard deviation checking

#from time import *
import time

import curses
stdscr = curses.initscr()      # this is the screen exactly the terminal size
curses.noecho()                # do not show the keys
curses.cbreak()                # react to keys without Carriage return
stdscr.keypad(1)               # return nice keyboard shortcuts

ts = []
#t0 = time.clock()               # time.clock() is the CPU time!

t0 = time.time()          # time.time() is the Wall (real world) time!
# (y,x) co-ordinates!
stdscr.addstr(10,1,time.strftime("%Y-%m-%d",time.localtime())+
              " Type 'q' to quit, 'n' to count.")

c = stdscr.getch()
t0 = time.time()          # time.time() is the Wall (real world) time!
i = 0
while 1 :
    c = stdscr.getch()
    if c == ord( 'n'):
        i = i + 1
        t = time.time()
        ts.append( t)
        stdscr.addstr( 0, 1, "beats: " + str( i)) # beats
#        s = time.strftime( "%S", time.gmtime( t - t0))
        stdscr.addstr( 1, 1, "running " + str(t - t0) + " s")
        stdscr.addstr( 2, 1, "beats per second " + str( 60*i / ( t - t0)) + " bpm")
    elif c == ord( 'q') : break  # Exit the while()

# use exceptions for restoring terminal stat!
# the end, reversing the keyboard stuff
curses.nocbreak(); stdscr.keypad(0); curses.echo()
curses.endwin()                 # restore everything

print "beats counted:", i
print "beats per minute", str( 60*i / ( t - t0))
print "standard deviation", str( 60*i / ( t - t0))
