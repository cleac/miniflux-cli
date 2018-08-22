import curses
import time


class App:

    def __init__(self):
        self._contexts = {}
        self._src = {}
        self._default_context = None
        self._exit = False

    def __enter__(self):
        self._scr = curses.initscr()

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        self._scr.keypad(True)
        self._scr.nodelay(True)

        self._init_contexts()

        return self

    def _init_contexts(self):
        self._contexts = {
            name: ctx(self)
            for name, ctx in self._contexts.items()}

    def register_context(self, name, context):
        self._contexts[name] = context

    def set_default(self, name):
        if name not in self._contexts:
            raise RuntimeError(f'Acquired non-registered context {name}')
        self._default_context = name

    def register_src(self, name, src):
        self._src[name] = src

    def acquire_src(self, name):
        if name not in self._src:
            raise RuntimeError(f'Acquired non-registered src {name}')
        return self._src[name]

    def loop(self):
        if self._default_context:
            default = self._default_context
        else:
            # Kinda peek random one
            default = next(self._contexts.keys())
        current_context = self._contexts[default]

        while True:
            current_context.view(self._scr)

            key = self._scr.getch()
            if key >= 0:
                any(map(
                    lambda c: c.handle_keypress(key),
                    [self, current_context]))

            if self._exit:
                break

            time.sleep(.1)

    def handle_keypress(self, key: int):
        try:
            if chr(key) == 'q':
                self._exit = True
                return True
        except Exception:
            pass
        return False

    def __exit__(self, t, s, d):
        curses.nocbreak()
        self._scr.keypad(False)
        curses.echo()
        curses.endwin()
        self._scr.nodelay(False)
