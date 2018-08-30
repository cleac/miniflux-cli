import curses


def elipsize(text: str, expect_width: int) -> str:
    if len(text) > expect_width:
        return text[:expect_width-3] + '...'
    if len(text) < expect_width:
        return text + ' ' * (expect_width - len(text))
    return text


class ListView:

    def __init__(self, app):
        self._selected = 0
        self._first_visible = 0

        self._screen_params = 0, 0

    def view(self, screen):
        if not self._update:
            return

        self._update = False
        self._screen_params = height, width = screen.getmaxyx()

        screen.clear()

        for i, feed_item in enumerate(self.render_function(
            self.data_source()[
                self._first_visible:
                height + self._first_visible-1],
            width
        )):
            if i == self._selected - self._first_visible:
                screen.addstr(feed_item, curses.A_REVERSE)
            else:
                screen.addstr(feed_item)

        screen.refresh()

    def move_down(self, count=1):
        self._selected = min(self._selected + count, len(self.feed_list) - 1)

        screen_height = self._screen_params[0]
        if self._first_visible + screen_height - 2 < self._selected:
            self._first_visible += 2 + self._selected - screen_height

    def move_up(self, count=1):
        self._selected = max(self._selected - count, 0)

        if self._first_visible > self._selected:
            self._first_visible = self._selected

    def get_current(self):
        return self.data_source()[self._selected]

    def render_function(self, items, width):
        raise NotImplementedError

    def data_source(self):
        raise NotImplementedError

    def open(self, item):
        raise NotImplementedError

    def request_update(self):
        self._update = True

    def handle_keypress(self, key):
        if key == curses.KEY_DOWN or chr(key) == 'j':
            self.move_down()
            self.request_update()
            return True
        elif key == curses.KEY_UP or chr(key) == 'k':
            self.move_up()
            self.request_update()
            return True
        elif (
            key == curses.KEY_ENTER or key == 10 or
            key == 13 or chr(key) == 'o'
        ):
            self.open(self.get_current())
            return True
        return False
