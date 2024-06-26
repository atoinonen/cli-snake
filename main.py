import curses
from curses.textpad import rectangle

def clamp(bottom: int, number: int, top: int):
    if number < bottom:
        return bottom
    if number > top:
        return top
    return number

def main(stdscr: curses.window):
    curses.curs_set(0)

    height = 40
    width = 40

    rectangle(stdscr, 0,0, 1+height+1, 1+width+1)

    row = 20
    col = 20

    row = clamp(1, row, height+1)
    col = clamp(1, col, width+1)
    stdscr.addch(row, col, '█')
    #stdscr.refresh()
    #stdscr.nodelay(True)

    last = ord('d')

    while True:
        stdscr.timeout(500)
        #time.sleep(0.5)
        c = stdscr.getch()
        curses.flushinp()

        stdscr.addch(row, col, ' ')
        
        if c == -1:
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
        col = clamp(1, col, width+1)
        stdscr.addch(row, col, '█')

        #stdscr.refresh()


curses.wrapper(main)
