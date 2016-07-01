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


class CommandMode():
    def handle(self, app):
        cwindow = app.cwin
        bak_text = cwindow.text
        text = ""
        while True:
            c = app.screen.getch()
            if c == 27:
                n = app.screen.getch()
                if n == curses.ERR:
                    #ESC
                    cwindow.set_text(bak_text)
                    app.set_mode('normal')
                    return
            elif c == curses.KEY_ENTER or c == 10 or c == 13:
                app.set_mode('normal')
                app.command(text)
                return
            elif c in range(0,128):
                text += chr(c)
                cwindow.add_text(chr(c))

class NormalMode():
    def handle(self, app):
        while True:
            c = app.screen.getch()
            if c == ord('q'):
                app.command('quit')
                return
            elif c == ord(':'):
                app.set_mode('command')
                return
            elif c == 27:
                n = app.screen.getch()
                if n == curses.ERR:
                    #ESC
                    app.cwin.set_text('esc')
                else:
                    #ALT + n
                    app.cwin.set_text(chr(n))
            elif c == ord('p'):
                app.command('write', text = 'Yolo')


class App():
    def __init__(self):
        self.run = True
        self.modes = {}
        self.commands = {}
        pass

    def initialize(self):
        os.environ.setdefault('ESCDELAY', '25')
        self.add_mode(NormalMode(), 'normal')
        self.add_mode(CommandMode(), 'command')
        self.set_mode('normal')
        def f(app, **kwargs):
            app.run = False
        self.add_command('quit',f)
        def f(app, **kwargs):
            if 'text' not in kwargs:
                return
            app.cwin.set_text( kwargs.get('text'))
        self.add_command('write', f)

    def startscr(self, screen):
        self.screen = screen
        self.screen.nodelay(True)
        self.screen.clear()
        self.screen.immedok(True)
        self.screen.border()
        self.cwin = CWindow()
        self.loop()

    def add_command(self, command, func):
        self.commands.update({command: func})

    def command(self, command, **kwargs):
        self.commands.get(command)(self,**kwargs)

    def add_mode(self, mode, tag):
        self.modes.update({tag: mode})

    def set_mode(self, mode):
        self.mode = self.modes.get(mode)

    def loop(self):
        while self.run:
            self.mode.handle(self)

if __name__ == "__main__":
    app = App()
    app.initialize()
    wrapper(app.startscr)

