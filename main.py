#!/bin/python3
from curses import wrapper
import curses
import os

class Window():
    def __init__(self,x, y, w, h):
        self.win = curses.newwin(h, w, y, x)
        self.win.immedok(True)

class CWindow():
    def __init__(self):
        self.window = Window(1, curses.LINES - 4, curses.COLS - 2, 3)
        self.win = self.window.win
        self.win.border()
        self.text = ""

    def set_text(self, text):
        self.win.clear()
        self.win.border()
        self.win.addstr(1,1, text)
        self.text = text

    def add_text(self, text):
        self.text += text
        self.set_text(self.text)

    def get_command(self, scr):
        bak_text = self.text
        self.set_text(":")
        text = ""
        while True:
            c = scr.getch()
            if c == 27:
                n = scr.getch()
                if n == curses.ERR:
                    self.set_text(bak_text)
                    return None
                else:
                    pass
            elif c == curses.KEY_ENTER or c == 10 or c == 13:
                return text
            elif c in range(0, 128):
                text += chr(c)
                self.add_text(chr(c))

def main(stdscr):
    stdscr.clear()
    curses.nonl()
    stdscr.immedok(True)
    stdscr.border(0)
    com_win = CWindow()
    com_win.set_text("test")

    #No ESC Delay
    stdscr.nodelay(True) #To handle esc

    while True:
        c = stdscr.getch()
        if c == ord('q'):
            return
        elif c == ord(':'):
            com_win.get_command(stdscr)
        elif c == 27:
            n = stdscr.getch()
            if n == curses.ERR:
                #Esc
                com_win.set_text('esc')
            else:
                #Alt + n is pressed
                com_win.set_text(chr(n))
        elif c == ord('p'):
            com_win.add_text('woo')


if __name__ == "__main__":
    os.environ.setdefault('ESCDELAY', '25')
    wrapper(main)
