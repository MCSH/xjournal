#!/bin/python3
from curses import wrapper
import curses
import os

class Window():
    def __init__(self, x, y, w, h, wintype = 0):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.wintype = wintype
        self.win = curses.newwin(h,w,y,x)
        self.win.immedok(True)
        self.clean()
        self.text = ""

    def clean(self):
        self.win.erase()
        self.border()

    def border(self):
        if self.wintype == 0:
            self.win.border(' ', ' ', 0, ' ', curses.ACS_HLINE, curses.ACS_HLINE, ' ', ' ')

    def set_text(self, text):
        self.clean()
        self.text = text
        self.check_size()
        self.win.addstr(1,0, text)

    def add_text(self, text):
        self.text += text
        self.check_size()
        if not self.check_size():
            self.set_text(self.text)
        else:
            self.win.addstr(text)

    def check_size(self):
        if self.wintype == 0:
            x_mod = 0
            y_mod = 1
        if( len(self.text) / (self.w-x_mod)  != self.h -y_mod):
            self.h = int(len(self.text) / (self.w-x_mod)) + y_mod+1
            self.y = int(curses.LINES - self.h)
            self.win.mvwin(self.y, self.x)
            self.win.resize(self.h, self.w)
            self.clean()
            return False
        return True


class CommandMode():
    def command(self, app, text):
        loc = text.find(' ')
        command = text
        argv = ""
        if loc != -1:
            command = text[:loc]
            argv = text[loc:]
        app.command(command, argv=argv)

    def handle(self, app):
        cwindow = app.cwin
        bak_text = cwindow.text
        text = ""
        cwindow.set_text("")
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
                self.command(app, text)
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
                app.command('write', argv = 'Yolo')


class App():
    def __init__(self):
        self.run = True
        self.modes = {}
        self.commands = {}

    def initialize(self):
        os.environ.setdefault('ESCDELAY', '25')
        self.add_mode(NormalMode(), 'normal')
        self.add_mode(CommandMode(), 'command')
        self.set_mode('normal')
        def f(app, **kwargs):
            app.run = False
        self.add_command('quit',f)
        def f(app, **kwargs):
            if 'argv' in kwargs:
                app.cwin.set_text( kwargs.get('argv'))
        self.add_command('write', f)

    def startscr(self, screen):
        self.screen = screen
        self.screen.nodelay(True)
        self.screen.immedok(True)
        self.screen.clear()
        self.cwin  = Window(0, curses.LINES - 2, curses.COLS -1 , 2)
        self.loop()

    def add_command(self, command, func):
        self.commands.update({command: func})

    def command(self, command, **kwargs):
        f = self.commands.get(command)
        if f !=None:
            f(self,**kwargs)

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

