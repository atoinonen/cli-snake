import curses
import random
import queue

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
    height = 10
    width = 10
    curses.update_lines_cols()
    centerline = curses.LINES // 2
    centercol = curses.COLS // 2
    window = curses.newwin(20, 30, centerline - 5, centercol - 11)
    window.addstr(1, 5, " ┏┑ ┎┒┎ ┏┓ ┒┏ ┏┑")
    window.addstr(2, 5, " ┃  ┃┃┃ ┣┫ ┣┫ ┣ ")
    window.addstr(3, 5, "┕┛  ┚┖┚ ┚┖ ┚┗ ┗┙")
    window.addstr(5, 1, "Press Enter to continue...")
    #curses.echo()
    #window.getstr()
    while True:
        window.addstr(7, 8, "↑W      ↑D")
        window.addstr(8, 7, "{:3}  🞬  {:3}      ".format(height, width))
        window.addstr(9, 8, "↓S      ↓A")
        #curses.update_lines_cols()
        #window.addstr(10, 3, "LINES: {:3} COLS: {:3}".format(curses.LINES, curses.COLS))

        key = window.getch()
        #window.clear()
        #window.addstr(7, 10, "{}".format(key))
        if key == ord('\n') or key == ord(' '):
            break
        elif key == ord('w'):
            height += 1
        elif key == ord('s'):
            if height <= 2:
                height = 2
            else:
                height -= 1
        elif key == ord('a'):
            if width <= 2:
                width = 2
            else:
                width -= 1
        elif key == ord('d'):
            width += 1

    #curses.noecho()
    window.clear()
    window.refresh()
    return (height, width)

def endgamescreen(score: int):
    curses.update_lines_cols()
    centerline = curses.LINES // 2
    centercol = curses.COLS // 2
    window = curses.newwin(20, 30, centerline - 5, centercol - 11)
    window.addstr(1, 5, "Game Over")
    window.addstr(2, 5, "Score: {}".format(score))
    while True:
        key = window.getch()
        if key == ord('\n') or key == ord(' '):
            break
    window.clear()
    window.refresh()

def main(stdscr: curses.window):
    curses.curs_set(0)

    height, width = startscreen()

    curses.update_lines_cols()
    centerline = curses.LINES // 2
    centercol = curses.COLS // 2

    gamewindow = curses.newwin(height+2, 2*width+2, centerline-(height // 2)-1, centercol-width+1)
    gamewindow.border()

    #infowindow = curses.newwin(10, 20, 0, 2*width+4)
    #infowindow.border()
    #infowindow.refresh()

    apple = '🍎'
    last = ord('d')
    snakeq = queue.Queue()
    row = height//2
    col = width//2
    just_head = True
    score = 0

    snakeq.put((row,col))
    gamewindow.addch(row, 2*col-1, '🐲')
    
    while True:
        apple_row = random.randint(1, height)
        apple_col = random.randint(1, width)
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

        if row < 1 or row > height:
            break
        if col < 1 or col > width:
            break
        if (row, col) in snakeq.queue:
            break

        snakeq.put((row, col))

        if row == apple_row and col == apple_col:
            # Snake eats an apple
            just_head = False
            score += 1
            while True:
                apple_row = random.randint(1, height)
                apple_col = random.randint(1, width)
                #infowindow.addstr(5, 1, "row: {:02}".format(apple_row))
                #infowindow.addstr(6, 1, "col: {:02}".format(apple_col))
                #infowindow.addstr(7, 1, "sizeq: {:02}".format(snakeq.qsize()))
                #infowindow.addstr(8, 1, "sizel: {:02}".format(len(list(snakeq.queue))))
                if (apple_row, apple_col) not in snakeq.queue:
                    break
                elif snakeq.qsize() >= height * width:
                    break
            gamewindow.addch(apple_row, 2*apple_col-1, apple)
        else:
            # Move snakes tail
            row_del, col_del = snakeq.get()
            gamewindow.addstr(row_del, 2*col_del-1, "  ")
        #infowindow.addstr(1, 1, "row: {:02}".format(row))
        #infowindow.addstr(2, 1, "col: {:02}".format(col))
        #infowindow.addstr(3, 1, "xy: {}".format(gamewindow.getyx()))

        #infowindow.refresh()
        for row, col in snakeq.queue:
            gamewindow.addch(row, 2*col-1, '🔥')

        gamewindow.addch(row, 2*col-1, '🐲')

    gamewindow.clear()
    gamewindow.refresh()
    endgamescreen(score)


curses.wrapper(main)
