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

    height = 20
    width = 30

    rectangle(stdscr, 0,0, 1+height+1, 1+width+1)

    row = 10
    col = 15

    row = clamp(1, row, height+1)
    col = clamp(1, col, width+1)
    stdscr.addch(row, col, 'A')
    stdscr.refresh()

    while True:
        c = stdscr.getch()

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
        row = clamp(1, row, height+1)
        col = clamp(1, col, width+1)
        stdscr.addch(row, col, 'A')
        stdscr.refresh()



curses.wrapper(main)
