import curses
import random
import time
import queue
from curses.textpad import rectangle

HEIGHT = 40
WIDTH = 40


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

    rectangle(stdscr, 0,1, 1+HEIGHT, 1+2*WIDTH+1)
    

    apple = '🍎'
    last = ord('d')
    #snake_size = 1
    snake_ate = False
    snakeq = queue.Queue()
    row = 20
    col = 20

    row = clamp(1, row, HEIGHT)
    col = clamp(1, col, WIDTH)
    snakeq.put((row,col))
    stdscr.addch(row, 2*col, '🐍')
    #stdscr.refresh()
    #stdscr.nodelay(True)
    
    apple_row = random.randint(1, HEIGHT)
    apple_col = random.randint(1, WIDTH)

    stdscr.addch(apple_row, 2*apple_col, apple)

    stdscr.timeout(500)

    while True:
        #time.sleep(0.5)
        c = stdscr.getch()
        #curses.flushinp()

        if snake_ate:
            snake_ate = False
            #snake_location = list(snakeq.queue)
            while True:
                apple_row = random.randint(1, HEIGHT)
                apple_col = random.randint(1, WIDTH)
                if (apple_row, apple_col) not in snakeq.queue:
                    break
            stdscr.addch(apple_row, 2*apple_col, apple)
        else:
            row_del, col_del = snakeq.get()
            stdscr.addstr(row_del, 2*col_del, "  ")
        
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

        row = clamp(1, row, HEIGHT)
        col = clamp(1, col, WIDTH)

        if row == apple_row and col == apple_col:
            snake_ate = True

        stdscr.addstr(0, 90, "row: {:02}".format(row))
        stdscr.addstr(1, 90, "col: {:02}".format(col))
        stdscr.addstr(2, 90, "xy: {}".format(stdscr.getyx()))

        
        snakeq.put((row, col))
        stdscr.addstr(3, 90, "snakeq: {}".format(snakeq.queue))
        for row, col in snakeq.queue:
            stdscr.addch(row, 2*col, '🐍')

        #stdscr.refresh()


curses.wrapper(main)
