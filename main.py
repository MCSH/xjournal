#!/bin/python3
from curses import wrapper
import curses
import os

class Window():
    def __init__(self, x, y, w, h):
        self.win = curses.newwin(h,w,y,x)
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

class NormalMode():
    def handle(self, app):
        while True:
            c = app.screen.getch()
            if c == ord('q'):
                return
            elif c == ord(':'):
                app.command.get_command(self.screen)
            elif c == 27:
                n = app.screen.getch()
                if n == curses.ERR:
                    #ESC
                    app.command.set_text('esc')
                else:
                    #ALT + n
                    app.command.set_text(chr(n))
            elif c == ord('p'):
                app.command.add_text('woo')



class App():
    def __init__(self):
        pass

    def initialize(self):
        os.environ.setdefault('ESCDELAY', '25')
        self.set_mode(NormalMode())

    def startscr(self, screen):
        self.screen = screen
        self.screen.nodelay(True)
        self.screen.clear()
        self.screen.immedok(True)
        self.screen.border()
        self.command = CWindow()
        self.loop()

    def set_mode(self, mode):
        self.mode = mode

    def loop(self):
        self.mode.handle(self)

if __name__ == "__main__":
    app = App()
    app.initialize()
    wrapper(app.startscr)

