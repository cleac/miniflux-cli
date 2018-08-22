from functools import wraps


class MetaDClass(type):

    def __new__(cls, name, parents, data):
        initmethod = data.get('__init__')

        def new_initmethod(slf, **kwargs):
            processed_fields = set()
            for name, value in kwargs.items():
                if name in slf._registered_fields:
                    setattr(slf, name, value)
                    processed_fields.add(name)

            for name in slf._registered_fields - processed_fields:
                setattr(slf, name, None)

            if initmethod:
                initmethod()

        if initmethod:
            new_initmethod = wraps(initmethod)(new_initmethod)

        data['__init__'] = new_initmethod

        registered_fields = set()
        for item in data.get('__annotations__', {}).keys():
            registered_fields.add(item)
        data['_registered_fields'] = registered_fields

        data['_storage'] = {}

        return super().__new__(cls, name, parents, data)


class DClass(metaclass=MetaDClass):

    @classmethod
    def parse(cls, obj):
        if obj['id'] not in cls._storage:
            cls._storage[obj['id']] = cls(id=obj['id'])
        return cls._storage[obj['id']]

    @property
    def dict(self):
        return {field: getattr(self, field)
                for field in self._registered_fields}

    def __repr__(self):
        return '<{0.__class__.__name__} {1}>'.format(
            self,
            ' '.join('{}={}'.format(key, getattr(self, key))
                     for key in self._registered_fields))
