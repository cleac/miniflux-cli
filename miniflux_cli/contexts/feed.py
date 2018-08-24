import os

from warnings import warn

from typing import Sequence

from miniflux_cli.mapping import FeedItem, Feed
from miniflux_cli.meta.tui import elipsize, ListView


def render_feed_list(feed_list: Sequence[FeedItem], display_width):
    if display_width > 30:
        return [
            ' {}  {}\n'.format(
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
        self.config = app.acquire_src('config')
        self.pause = app.acquire_src('pause')

        self.feed_list = self._api.get_unread()

        self._run_editor = False

    def render_function(self, data, width):
        return render_feed_list(data, width)

    def data_source(self):
        return self.feed_list

    def open(self, feed_item):
        with self.pause:
            try:
                os.system(f'{self.config.open_command} {feed_item.url}')
            except Exception:
                warn('Command not found')
        self._api.mark_read(feed_item.id)
        self.feed_list = self._api.get_unread()

    def open_alternative(self, feed_item):
        with self.pause:
            try:
                os.system(
                    f'{self.config.alternative_open_command} {feed_item.url}')
            except Exception:
                warn('Command not found')
        self.feed_list = self._api.get_unread()

    def mark_read(self, feed_item):
        self._api.mark_read(feed_item.id)
        self.feed_list = self._api.get_unread()
        self.move_up(1)

    def handle_keypress(self, key):
        if super().handle_keypress(key):
            return True

        try:
            if chr(key) == 'r':
                self.feed_list = self._api.get_unread()
                self.request_update()
                return True
            elif chr(key) == 'd':
                self.mark_read(self.get_current())
                self.request_update()
                return True
            elif chr(key) == 'O':
                self.open_alternative(self.get_current())
        except Exception:
            pass

        return False
