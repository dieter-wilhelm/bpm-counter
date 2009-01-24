#!/usr/bin/env python

# TODO:
# moving average as current average?
# restart key with status of last measurement
# dismiss pauses/unregular typing  
# documentation string, command line -h/--help option

import math

def mean( A):
    """Mean of the list A."""
    l = float( len( A))
    return sum( A) / l

def var( A):
    """Variance (n-1) of the list A.
Returns 0 if len( A) < 1.
    """
    m = mean( A)
    l = float( len( A))
    v = 0
    for x in A:
       v = v + ( x - m)**2
    if l > 1:
        return v / ( l - 1)
    else:
        return 0.

def stddev( A):
    """Standard deviation of the list A."""
    return math.sqrt( var( A))
    
#from time import *
import time
 # time.clock() is the CPU time!
 # time.time() is the Wall (real world) time!
import string


class StopWatch:
    """Ahhh, well."""
    ts = []                     # the times


# --- interface stuff ---

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
    stdscr.addstr(0, 1, "beat : 1")
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
            t2 = t              # t2 is current time t1 the time before
            ts.append( t2 - t1)
            stdscr.addstr( 0, 1, "No of beats: " + str( i)) # beats
        #        s = time.strftime( "%S", time.gmtime( t - t0))
            stdscr.addstr( 1, 1, "Running for " + str( round( t2 - t0, 1)) + " s")
            b =  60*i / ( t - t0)
            stdscr.addstr( 2, 1, "Overall beats per minute: " + string.rjust( str( round( b, 1)), 5) + " bpm")
            stdscr.addstr( 3, 1, "Current beats per minute: " + string.rjust( str( round( 60 / ( t2 - t1), 1)), 5) + " bpm")
            if i > 1:
                d = stddev( ts) * 60
                stdscr.addstr( 4, 1, "Overall stddev: " + string.rjust( str( round( d, 1)), 4) + " bpm")
                stdscr.addstr( 5, 1, "Relative dev: " + string.rjust( str( round(d / b * 100, 1)), 4) + " %")
            t1 = t2
        elif c == ord( 'q') : break  # Exit the while()
finally:
    # the end, reversing the keyboard stuff
    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()                 # restore everything
    print "beats counted:", i
    if t != t0:
        print "Overall:", str( round( 60*i / ( t - t0), 1)), "bpm"
        print "Standard deviation", str( round( stddev( ts) * 60, 2)), "bpm"
