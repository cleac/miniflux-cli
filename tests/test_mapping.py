from unittest import TestCase

from miniflux_cli import mapping as mp

INPUT_CATEGORY_SHAPE = {
    'id': 1,
    'title': 'Category',
}

INPUT_FEED_SHAPE = {
    'id': 1,
    'title': 'Feed',
    'category': INPUT_CATEGORY_SHAPE,
}

INPUT_FEED_ITEM_SHAPE = {
    'id': 1,
    'feed': INPUT_FEED_SHAPE,
    'title': 'Feed Item',
    'url': 'https://google.com',
}


class TestMapping(TestCase):

    def test_read_all(self):
        mp.FeedItem.parse(INPUT_FEED_ITEM_SHAPE)

        feed_item = mp.load(mp.FeedItem, 1)

        self.assertIsNotNone(feed_item)

        self.assertEqual(feed_item.id, INPUT_FEED_ITEM_SHAPE['id'])
        self.assertEqual(feed_item.feed_id,
                         INPUT_FEED_ITEM_SHAPE['feed']['id'])
        self.assertEqual(feed_item.title, INPUT_FEED_ITEM_SHAPE['title'])
        self.assertEqual(feed_item.url, INPUT_FEED_ITEM_SHAPE['url'])
        self.assertIsNone(feed_item.content)

        feed = mp.load(mp.Feed, 1)

        self.assertIsNotNone(feed)

        self.assertEqual(feed.id, INPUT_FEED_SHAPE['id'])
        self.assertEqual(feed.title, INPUT_FEED_SHAPE['title'])
        self.assertEqual(feed.category_id, INPUT_FEED_SHAPE['category']['id'])

        category = mp.load(mp.Category, 1)

        self.assertIsNotNone(category)

        self.assertEqual(category.id, INPUT_CATEGORY_SHAPE['id'])
        self.assertEqual(category.title, INPUT_CATEGORY_SHAPE['title'])
