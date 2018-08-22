import curses
import time


class InitCursesMixin:
    """Mixin class that initializes curses to display things"""

    def __enter__(self):
        self._scr = curses.initscr()

        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)

        self._scr.keypad(True)
        self._scr.nodelay(True)

        return self

    def __exit__(self, t, s, d):
        self._scr.nodelay(False)
        self._scr.keypad(False)

        curses.nocbreak()
        curses.echo()
        curses.endwin()


class ContextHandlerMixin:

    def __init__(self):
        super().__init__()
        self._contexts = {}
        self._default_context = None

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

    def get_default_context(self):
        if self._default_context:
            default = self._default_context
        else:
            # Kinda peek random one
            default = next(self._contexts.keys())
        return self._contexts[default]


class SRCHandlerMixin:

    def __init__(self):
        super().__init__()
        self._src = {}

    def register_src(self, name, src):
        self._src[name] = src

    def acquire_src(self, name):
        if name not in self._src:
            raise RuntimeError(f'Acquired non-registered src {name}')
        return self._src[name]


class App(InitCursesMixin, ContextHandlerMixin, SRCHandlerMixin):

    def __init__(self):
        super().__init__()
        self._exit = False

    def __enter__(self):
        self._init_contexts()
        return super().__enter__()

    def loop(self):
        current_context = self.get_default_context()

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

    def exit(self):
        self._exit = True

    def handle_keypress(self, key: int):
        try:
            if chr(key) == 'q':
                self.exit()
                return True
        except Exception:
            pass
        return False