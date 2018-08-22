from ._mapping_meta import DClass


class FeedItem(DClass):
    id: int
    feed_id: int
    title: str
    content: str
    url: str

    @classmethod
    def parse(cls, obj):
        feed_item = super().parse(obj)
        feed_item.title = obj.get('title', feed_item.title)
        feed_item.content = obj.get('content', feed_item.content)
        feed_item.url = obj.get('url', feed_item.url)
        feed_item.feed_id = Feed.parse(obj['feed']).id
        return feed_item


class Category(DClass):
    id: int
    title: str

    @classmethod
    def parse(cls, obj):
        category = super().parse(obj)
        category.title = obj.get('title', category.title)
        return category


class Feed(DClass):
    id: int
    title: str
    category_id: int

    @classmethod
    def parse(cls, obj):
        feed = super().parse(obj)
        feed.title = obj.get('title', feed.title)
        feed.category_id = Category.parse(obj['category']).id
        return feed
