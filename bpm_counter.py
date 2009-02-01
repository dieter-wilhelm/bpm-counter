#!/usr/bin/env python

# Copyright (C) 2009  H. Dieter Wilhelm
# Author: H. Dieter Wilhelm <dieter@duenenhof-wilhelm.de>
# Created: 2009-01
# Version: 1.0

# This code is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 3, or (at your
# option) any later version.
#
# This python script is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# Permission is granted to distribute copies of this pyhton script
# provided the copyright notice and this permission are preserved in
# all copies.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, you can either send email to this
# program's maintainer or write to: The Free Software Foundation,
# Inc.; 675 Massachusetts Avenue; Cambridge, MA 02139, USA.

# --- TODO ---
# check under Windows (cygwin?)
# (command line option for) choice of precision
# PrintStatus() not working properly
# Adjust accuracy during run?
# give acceleration information?

# --- command line help ---

import sys

if len( sys.argv) > 1:
    print """Display the frequency of keystrokes in 1/min (bpm).

    usage: blabla.""", sys.argv[ 0]
    exit ( 1)

# --- helper functions ---

import math

def mean( A):
    """Mean of the list A."""
    l = float( len( A))
    return sum( A) / l

def variance( A):
    """Variance (n-1) of the list A.
Return 0 if len( A) < 1.
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

def standardDeviation( A):
    """Standard deviation of the list A."""
    return math.sqrt( variance( A))
    
def movingAverage( A, n = 5):
    """List A's mean of the last n members.

If len( A) < n, return the mean of less than n elements."""
    return mean( A[ -n:]) 

# --- class definitions ---
    
#from time import *
import time
 # time.clock() is the CPU time!
 # time.time() is the Wall (real world) time!
import string

class StopWatch():
    """Container of points in time measured in s."""
    def __init__( self):
        """bla"""
        self.times = []
        
    def ClockIn( self):
        """Adding the current time."""
        t = time.time()
        self.times.append( t)
        return t
    
    def Times (self):
        """Return the time list."""
        return self.times
        

class FrequencyCounter( StopWatch):
    """Frequencies are counted in 1/min."""
    tolerance = 0.3             # max deviation of time differences
    def __init__( self):
        """so what?"""
        StopWatch.__init__( self)
        self.frequencies = []
        self.t_min = 0             # smallest time diff
        self.t_max = 0             # biggest time diff
        
    def TriggerCounter( self):
        """Starting the stopWatch for the first time."""
        self.ClockIn()
        
    def Count( self):
        """Clocking in and counting in 1/min."""
        tt = self.ClockIn()        # the latest time
        t  = self.times[-2:-1][ 0] # the previous time
        diff = tt - t
        #  exception: we need a triggered time list!
        l = len( self.times)
        if l < 2:
            raise IndexError('Counter must first be triggered')        
        if l == 2:
            tol = FrequencyCounter.tolerance
            self.t_min = ( 1 - tol) * diff
            self.t_max = ( 1 + tol) * diff
        if diff > self.t_max or diff < self.t_min:
            return 1             # count not accurate enough
        else:
            self.frequencies.append( 60 / diff )
            return 0

    def Frequencies( self):
        """Return frequency list."""
        return self.frequencies

    def Times( self):
        """Return time list."""
        return self.times

    def PrintStatus( self):
        """"""
        b = len( self.frequencies)
        k = len( self.times)
        print "Keystrokes:", k
        print "Beats counted:", b
        bpm =  round( mean( self.frequencies),1)
        std = round( standardDeviation( self.frequencies), 2)
        print "Mean:", str( round( bpm, 1)), "bpm"
        print "Standard deviation", str( std), "bpm"
        bpm =  movingAverage( self.frequencies)
        print "Moving Average:", str( bpm), "bpm"
        
#from time import *
import time
 # time.clock() is the CPU time!
 # time.time() is the Wall (real world) time!
import string

# --- interface stuff ---
import curses

def endCurses():
    """"""
    curses.nocbreak(); stdscr.keypad( 0); curses.echo(); curses.curs_set( 1)
    curses.endwin()                 # restore everything


def tui ( n):                   # text user interface
    """Text User Interphase."""
    stdscr.erase()              # remove vestiges from previous run
    try:
        Fc = FrequencyCounter()
    # addstr uses (y,x) co-ordinates!
        stdscr.addstr(1,1, "Run " + str( n) + " waiting.", curses.A_BOLD)
        stdscr.addstr(2,1, "Type 'q' to quit, SPACE to count or 'r' to restart.", curses.A_DIM)
        stdscr.addstr(3, 1, "Keystrokes: 0", curses.A_BOLD)

        c = stdscr.getch()
        while not c == ord(' '):        # intercept wrong keys
            if c == ord('q'):
                return 1
            c = stdscr.getch()
            
        Fc.TriggerCounter()
        t0 = time.time()          # time.time() is the Wall (real world) time!
        stdscr.addstr(1, 1, "Run " + str( n) + " active.      ", curses.A_BOLD)
        stdscr.addstr(4, 1, "Keystrokes: 1", curses.A_BOLD)
        stdscr.addstr(5, 1, "Beats counted: 0", curses.A_DIM)
        while 1:
            c = stdscr.getch()
            if c == ord(' '):
                if Fc.Count():
                    curses.flash()  # not accurate enough
                # Status
                td = round( time.time() - t0, 1)
                stdscr.addstr(1, 1, "Run " + str( n) + " active for " + str( td) + " s.", curses.A_BOLD)
                # Keystrokes
                l = len( Fc.Times())
                stdscr.addstr(4, 1, "Keystrokes: " +  str( l), curses.A_BOLD)
                # Beats counted
                b = len( Fc.Frequencies())
                stdscr.addstr(5, 1, "Beats counted: " +  str( b), curses.A_DIM)
                # Mean
                bpm = round( mean( Fc.Frequencies()), 1)
                stdscr.addstr(6, 1, "Mean: " +  string.rjust( str( bpm), 5) + " bpm", curses.A_BOLD)
                # Moving average
                bpm = round( movingAverage( Fc.Frequencies()), 1)
                stdscr.addstr(7, 1, "Moving average: " +  string.rjust( str( bpm), 5) + " bpm", curses.A_DIM)
                # Standard & relative deviation
                std = round( standardDeviation( Fc.Frequencies()), 1)
                dev = round( 100 * std/bpm, 1) # relative deviation in percent
                stdscr.addstr(8, 1, "Relative Deviation: " +  string.rjust( str( dev), 5) + " %", curses.A_BOLD)
                stdscr.addstr(9, 1, "Standard Deviation: " +  string.rjust( str( std), 5) + " bpm", curses.A_DIM)

            elif c == ord('r'):
                return 0
                
            elif c == ord('q'):
                endCurses()
                Fc.PrintStatus()
                return 1
                
    except KeyboardInterrupt:
        c = stdscr.getch()      # discarding C-c
        stdscr.addstr( 9, 1, "Do you really want to quit?  Print y", curses.A_BOLD)
        c = stdscr.getch()
        if c == ord('y'):
            endCurses()
            return 1
        else:
            stdscr.addstr( 9, 1, "                                           ")
            return 0
    
# ----------------------------------------------------------------------
# run interphase loop ------------------------------

stdscr = curses.initscr()      # this is a screen exactly the terminal size
curses.noecho()                # do not show the keys
curses.cbreak()                # react to keys without Carriage return
curses.curs_set( 0)            # 0: switch off cursor
stdscr.keypad( 1)              # return nice keyboard shortcuts

try:                      # force restoration of terminal
    i = 1                 # run counter
    while not tui( i):
        i = i + 1
finally:
    # reversing the terminal stuff
    endCurses()

exit()  #######################################################################

try:
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
        raise IOError( "nothing to do")
    while 1 :
        c = stdscr.getch()
        if c == ord( 'n'):
            i = i + 1
            t = time.time()
            t2 = t              # t2 is current time t1 the time before
            ts.append( t2 - t1)
            stdscr.addstr( 0, 1, "No of beats: " + str( i),curses.A_BOLD) # beats
        #        s = time.strftime( "%S", time.gmtime( t - t0))
            stdscr.addstr( 1, 1, "Running for " + str( round( t2 - t0, 1)) + " s",curses.A_DIM)
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
 
