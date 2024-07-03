import curses
import random
import queue

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

def startscreen():
    window = curses.newwin(10, 30, 0, 0)
    window.addstr(1, 5, " ┏┑ ┎┒┎ ┏┓ ┒┏ ┏┑")
    window.addstr(2, 5, " ┃  ┃┃┃ ┣┫ ┣┫ ┣ ")
    window.addstr(3, 5, "┕┛  ┚┖┚ ┚┖ ┚┗ ┗┙")
    window.addstr(5, 1, "Press any key to continue...")
    window.getch()
    window.clear()
    window.refresh()

def main(stdscr: curses.window):
    curses.curs_set(0)

    startscreen()

    gamewindow = curses.newwin(HEIGHT+2, 2*WIDTH+2, 0, 0)
    gamewindow.border()

    infowindow = curses.newwin(10, 20, 0, 2*WIDTH+4)
    infowindow.border()
    infowindow.refresh()

    apple = '🍎'
    last = ord('d')
    snakeq = queue.Queue()
    row = HEIGHT//2
    col = WIDTH//2
    just_head = True

    snakeq.put((row,col))
    gamewindow.addch(row, 2*col-1, '🐲')
    
    while True:
        apple_row = random.randint(1, HEIGHT)
        apple_col = random.randint(1, WIDTH)
        if (apple_row, apple_col) not in snakeq.queue:
            break

    gamewindow.addch(apple_row, 2*apple_col-1, apple)

    gamewindow.timeout(150)

    while True:
        c = gamewindow.getch()
        
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

        snakeq.put((row, col))

        if row == apple_row and col == apple_col:
            # Snake eats an apple
            just_head = False
            while True:
                apple_row = random.randint(1, HEIGHT)
                apple_col = random.randint(1, WIDTH)
                infowindow.addstr(5, 1, "row: {:02}".format(apple_row))
                infowindow.addstr(6, 1, "col: {:02}".format(apple_col))
                infowindow.addstr(7, 1, "sizeq: {:02}".format(snakeq.qsize()))
                infowindow.addstr(8, 1, "sizel: {:02}".format(len(list(snakeq.queue))))
                if (apple_row, apple_col) not in snakeq.queue:
                    break
                elif snakeq.qsize() >= HEIGHT * WIDTH:
                    break
            gamewindow.addch(apple_row, 2*apple_col-1, apple)
        else:
            # Move snakes tail
            row_del, col_del = snakeq.get()
            gamewindow.addstr(row_del, 2*col_del-1, "  ")
        infowindow.addstr(1, 1, "row: {:02}".format(row))
        infowindow.addstr(2, 1, "col: {:02}".format(col))
        infowindow.addstr(3, 1, "xy: {}".format(gamewindow.getyx()))

        infowindow.refresh()
        for row, col in snakeq.queue:
            gamewindow.addch(row, 2*col-1, '🔥')

        gamewindow.addch(row, 2*col-1, '🐲')


curses.wrapper(main)
