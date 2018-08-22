import curses
import curses.textpad
import os

from warnings import warn

from typing import Sequence

from miniflux.mapping import FeedItem, Feed
from miniflux.meta.tui import elipsize, ListView


def render_feed_list(feed_list: Sequence[FeedItem], display_width):
    if display_width > 180:
        return [
            '{}  {}  {}\n'.format(
                elipsize(Feed._storage[feed_item.feed_id].title, 15),
                elipsize(feed_item.title, 60),
                elipsize(feed_item.url, display_width - 80),
            ) for feed_item in feed_list
        ]
    elif display_width > 30:
        return [
            '{}  {}\n'.format(
                elipsize(
                    Feed._storage[feed_item.feed_id].title,
                    round(display_width / 3) - 2
                ),
                elipsize(feed_item.title, round(2 * display_width / 3) - 2),
            ) for feed_item in feed_list
        ]
    return [
        '{}\n'.format(
            elipsize(feed_item.title, display_width),
        ) for feed_item in feed_list
    ]


class FeedContext(ListView):

    def __init__(self, app):
        super().__init__(app)
        self._api = app.acquire_src('miniflux_api')
        self.feed_list = self._api.get_unread()

        self._run_editor = False

    def data_source(self, start_index, end_index, width):
        return render_feed_list(self.feed_list[start_index:end_index], width)

    def open(self, feed_item):
        try:
            os.spawnvp.call(os.P_NOWAIT, 'xdg-open', [feed_item.url])
        except Exception:
            warn('You are runnig in container or don\'t have a command')

        self._api.mark_read(feed_item.id)
        self.feed_list = self._api.get_unread()

    def handle_keypress(self, key):
        if super().handle_keypress(key):
            return True

        try:
            if chr(key) == 'r':
                self.feed_list = self._api.get_unread()
                return True
        except Exception:
            pass

        return False
