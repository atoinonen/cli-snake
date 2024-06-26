import curses
import random
import time
from curses.textpad import rectangle

def clamp(bottom: int, number: int, top: int):
    if number < bottom:
        return bottom
    if number > top:
        return top
    return number

def draw():
    snake = '🐍'
    apple = '🍎'
    snake_head = '🐲'
    snake_body = '🔥'

def main(stdscr: curses.window):
    curses.curs_set(0)

    height = 40
    width = 40

    rectangle(stdscr, 0,1, 1+height+1, 1+2*width+1)

    row = 20
    col = 20

    row = clamp(1, row, height+1)
    col = clamp(1, col, width+1)
    stdscr.addch(row, 2*col, '🐍')
    #stdscr.refresh()
    #stdscr.nodelay(True)
    
    apple = '🍎'
    last = ord('d')

    apple_row = random.randint(1, height+1)
    apple_col = random.randint(1, width)

    stdscr.addch(apple_row, 2*apple_col, apple)

    while True:
        stdscr.timeout(500)
        #time.sleep(0.5)
        c = stdscr.getch()
        #curses.flushinp()

        stdscr.addstr(row, 2*col, "  ")
        
        if c == -1 or c not in [ord('w'), ord('s'), ord('a'), ord('d'), ord('q')]:
            c = last

        if c == ord('w'):
            row = row - 1
        elif c == ord('s'):
            row = row + 1
        elif c == ord('a'):
            col = col - 1
        elif c == ord('d'):
            col = col + 1
        elif c == ord('q'):
            break
        
        last = c

        row = clamp(1, row, height+1)
        col = clamp(1, col, width)

        stdscr.addstr(0, 90, "row: {:02}".format(row))
        stdscr.addstr(1, 90, "col: {:02}".format(col))
        stdscr.addstr(2, 90, "xy: {}".format(stdscr.getyx()))
        
        stdscr.addch(row, 2*col, '🐍')

        #stdscr.refresh()


curses.wrapper(main)
