from typing import NamedTuple, Optional, Dict, Any, Callable


db_storage = {}


def load(cls: type, id: int) -> Optional[NamedTuple]:
    if not hasattr(cls, '_storage'):
        cls._storage = {}
    return cls._storage.get(id, None)


def save(cls: type, id: int, item: NamedTuple) -> NamedTuple:
    if not hasattr(cls, '_storage'):
        cls._storage = {}
    cls._storage[id] = item
    return item


def get_obj_acquirer(
    obj: Dict[str, Any],
    prev: Optional[NamedTuple],
) -> Callable[[str], Any]:
    return lambda key: obj.get(key, getattr(prev, key, None))


class FeedItem(NamedTuple):
    id: int
    feed_id: int
    title: str
    content: Optional[str]
    url: str

    @classmethod
    def parse(cls, obj: Dict[str, Any]) -> NamedTuple:
        feed_item = {'id': obj['id']}
        prev_value = load(cls, obj['id'])

        acquire = get_obj_acquirer(obj, prev_value)
        feed_item['title'] = acquire('title')
        feed_item['content'] = acquire('content')
        feed_item['url'] = acquire('url')
        feed_item['feed_id'] = Feed.parse(obj['feed']).id
        return save(cls, feed_item['id'], cls(**feed_item))


class Category(NamedTuple):
    id: int
    title: str

    @classmethod
    def parse(cls, obj: Dict[str, Any]) -> NamedTuple:
        itm_id = obj['id']
        category = {'id': itm_id}
        prev = load(cls, itm_id)

        acquire = get_obj_acquirer(obj, prev)
        category['title'] = acquire('title')
        return save(cls, itm_id, cls(**category))


class Feed(NamedTuple):
    id: int
    title: str
    category_id: int

    @classmethod
    def parse(cls, obj: Dict[str, Any]) -> NamedTuple:
        itm_id = obj['id']
        feed = {'id': itm_id}
        prev = load(cls, itm_id)

        acquire = get_obj_acquirer(obj, prev)
        feed['title'] = acquire('title')
        feed['category_id'] = Category.parse(obj['category']).id
        return save(cls, itm_id, cls(**feed))
