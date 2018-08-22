from typing import Sequence

from .mapping import FeedItem, Feed


def _elipsize(text: str, expect_width: int) -> str:
    if len(text) > expect_width:
        return text[:expect_width-3] + '...'
    if len(text) < expect_width:
        return text + ' ' * (expect_width - len(text))
    return text


def render_feed_list(feed_list: Sequence[FeedItem], display_width):
    if display_width > 100:
        return [
            '{}  {}  {}'.format(
                _elipsize(Feed._storage[feed_item.feed_id].title, 15),
                _elipsize(feed_item.title, 50),
                feed_item.url,
            ) for feed_item in feed_list
        ]
    elif display_width > 30:
        return [
            '{}  {}'.format(
                _elipsize(Feed._storage[feed_item.feed_id].title, round(display_width / 3)),
                _elipsize(feed_item.title, round(2 * display_width / 3)),
            ) for feed_item in feed_list
        ]
    return [
        '{}'.format(
            _elipsize(feed_item.title, display_width),
        ) for feed_item in feed_list
    ]
