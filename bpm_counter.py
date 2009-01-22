#!/usr/bin/env python

# TODO: 
# standard deviation checking, dismiss pauses
# display of overall and current bpm 
# documentation string, command line -h/--help option

def stddev( A):
    """Guess what!"""
    def mean( A):
        """Guess what!"""
        l = float( len( A))
        return sum( A) / l
    m = mean( A)
    l = float( len( A))
    v = 0
    for x in A:
       v = v + ( x - m)**2
    return v / l

#from time import *
import time
# t = time.clock()         # time.clock() is the CPU time!
# t = time.time()          # time.time() is the Wall (real world) time!

import curses
stdscr = curses.initscr()      # this is the screen exactly the terminal size
curses.noecho()                # do not show the keys
curses.cbreak()                # react to keys without Carriage return
stdscr.keypad(1)               # return nice keyboard shortcuts

try:
    r = 40, 200                 # interesting beat range
    ts = []

    # addstr uses (y,x) co-ordinates!
    stdscr.addstr(10,1,time.strftime("%Y-%m-%d",time.localtime())+ \
                      " Type 'q' to quit, 'n' to count.")

    i = 0
    c = stdscr.getch()
    # beginning
    t = t0 = time.time()          # time.time() is the Wall (real world) time!
    t1 = t2 = time.time()
    if c == ord('q'):
        raise
    while 1 :
        c = stdscr.getch()
        if c == ord( 'n'):
            i = i + 1
            t = time.time()
            t2 = t
            ts.append( t2 - t1)
            stdscr.addstr( 0, 1, "beats: " + str( i)) # beats
        #        s = time.strftime( "%S", time.gmtime( t - t0))
            stdscr.addstr( 1, 1, "running " + str(t - t0) + " s")
            stdscr.addstr( 2, 1, "beats per second " + str( 60*i / ( t - t0)) + " bpm")
            t1 = t2
        elif c == ord( 'q') : break  # Exit the while()
finally:
    # the end, reversing the keyboard stuff
    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()                 # restore everything
    print "beats counted:", i
    if t != t0:
        print "Overall:", str( 60*i / ( t - t0)), "bpm"
        print "Standard deviation", str( stddev( ts) * 60), "bpm"
