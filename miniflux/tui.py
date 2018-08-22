import curses
import curses.textpad
import os
import subprocess
from warnings import warn

from typing import Sequence

from .mapping import FeedItem, Feed


def _elipsize(text: str, expect_width: int) -> str:
    if len(text) > expect_width:
        return text[:expect_width-3] + '...'
    if len(text) < expect_width:
        return text + ' ' * (expect_width - len(text))
    return text


def render_feed_list(feed_list: Sequence[FeedItem], display_width):
    if display_width > 180:
        return [
            '{}  {}  {}\n'.format(
                _elipsize(Feed._storage[feed_item.feed_id].title, 15),
                _elipsize(feed_item.title, 60),
                _elipsize(feed_item.url, display_width - 80),
            ) for feed_item in feed_list
        ]
    elif display_width > 30:
        return [
            '{}  {}\n'.format(
                _elipsize(
                    Feed._storage[feed_item.feed_id].title,
                    round(display_width / 3) - 2
                ),
                _elipsize(feed_item.title, round(2 * display_width / 3) - 2),
            ) for feed_item in feed_list
        ]
    return [
        '{}\n'.format(
            _elipsize(feed_item.title, display_width),
        ) for feed_item in feed_list
    ]


class FeedContext:

    def __init__(self, app):
        self._api = app.acquire_src('miniflux_api')
        self.feed_list = self._api.get_unread()

        self._selected = 0
        self._first_visible = 0

        self._screen_params = 0, 0

        self._run_editor = False

    def view(self, screen):
        self._screen_params = height, width = screen.getmaxyx()

        screen.clear()

        for i, feed_item in enumerate(render_feed_list(
            self.feed_list[self._first_visible: height+self._first_visible-1],
            width
        )):
            if i == self._selected - self._first_visible:
                screen.addstr(feed_item, curses.A_REVERSE)
            else:
                screen.addstr(feed_item)

        screen.refresh()

    def move_down(self, count=1):
        self._selected = min(self._selected + count, len(self.feed_list) - 1)

        while self._screen_params[0] + self._first_visible-2 < self._selected:
            self._first_visible += 1

    def move_up(self, count=1):
        self._selected = max(self._selected - count, 0)

        while self._first_visible > self._selected:
            self._first_visible -= 1

    def open(self, feed_item, command='xdg-open'):
        try:
            os.spawnvp.call(os.P_NOWAIT, command, [feed_item.url])
        except Exception:
            warn('You are runnig in container or don\'t have a command')
        self._api.mark_read(feed_item.id)
        self.feed_list = self._api.get_unread()

    def handle_keypress(self, key):
        if key == curses.KEY_DOWN or chr(key) == 'j':
            self.move_down()
            return True
        elif key == curses.KEY_UP or chr(key) == 'k':
            self.move_up()
            return True
        elif key == curses.KEY_ENTER or chr(key) == 'o':
            self.open(self.feed_list[self._selected])
            return True
        elif chr(key) == 'r':
            self.feed_list = self._api.get_unread()
            return True
        return False
