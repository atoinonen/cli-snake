import curses
import random
import time
import queue
from curses.textpad import rectangle

HEIGHT = 10 
WIDTH = 10


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
    row = HEIGHT//2
    col = WIDTH//2
    just_head = True

    #row = clamp(1, row, HEIGHT)
    #col = clamp(1, col, WIDTH)
    snakeq.put((row,col))
    stdscr.addch(row, 2*col, '🐲')
    #stdscr.refresh()
    #stdscr.nodelay(True)
    
    while True:
        apple_row = random.randint(1, HEIGHT)
        apple_col = random.randint(1, WIDTH)
        stdscr.addstr(5, WIDTH*2+4, "row: {:02}".format(apple_row))
        stdscr.addstr(6, WIDTH*2+4, "col: {:02}".format(apple_col))
        if (apple_row, apple_col) not in snakeq.queue:
            break

    stdscr.addch(apple_row, 2*apple_col, apple)

    #stdscr.timeout(500)

    while True:
        #time.sleep(0.5)
        c = stdscr.getch()
        #curses.flushinp()


        
        if c == -1 or c not in [ord('w'), ord('s'), ord('a'), ord('d'), ord('q')]:
            c = last

        if just_head:
            pass
        elif last == ord('w') and c == ord('s'):
            c = ord('w')
        elif last == ord('s') and c == ord('w'):
            c = ord('s')
        elif last == ord('a') and c == ord('d'):
            c = ord('a')
        elif last == ord('d') and c == ord('a'):
            c = ord('d')


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

        if row < 1 or row > HEIGHT:
            break
        if col < 1 or col > WIDTH:
            break
        if (row, col) in snakeq.queue:
            break
        row = clamp(1, row, HEIGHT)
        col = clamp(1, col, WIDTH)

        snakeq.put((row, col))

        if row == apple_row and col == apple_col:
            snake_ate = True

        if snake_ate:
            snake_ate = False
            just_head = False
            #snake_location = list(snakeq.queue)
            while True:
                apple_row = random.randint(1, HEIGHT)
                apple_col = random.randint(1, WIDTH)
                stdscr.addstr(5, WIDTH*2+4, "row: {:02}".format(apple_row))
                stdscr.addstr(6, WIDTH*2+4, "col: {:02}".format(apple_col))
                stdscr.addstr(7, WIDTH*2+4, "sizeq: {:02}".format(snakeq.qsize()))
                stdscr.addstr(8, WIDTH*2+4, "sizel: {:02}".format(len(list(snakeq.queue))))
                if (apple_row, apple_col) not in snakeq.queue:
                    break
                elif snakeq.qsize() >= HEIGHT * WIDTH:
                    break
            stdscr.addch(apple_row, 2*apple_col, apple)
            #snakeq.put((row, col))
        else:
            row_del, col_del = snakeq.get()
            stdscr.addstr(row_del, 2*col_del, "  ")
        stdscr.addstr(0, WIDTH*2+4, "row: {:02}".format(row))
        stdscr.addstr(1, WIDTH*2+4, "col: {:02}".format(col))
        stdscr.addstr(2, WIDTH*2+4, "xy: {}".format(stdscr.getyx()))

        #stdscr.addstr(3, WIDTH*2+4, "snakeq: {}".format(snakeq.queue))
        for row, col in snakeq.queue:
            stdscr.addch(row, 2*col, '🔥')

        stdscr.addch(row, 2*col, '🐲')
        #stdscr.refresh()


curses.wrapper(main)
