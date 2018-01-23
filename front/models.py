from marshmallow import Schema, fields

from front import mixins
from front.search import ListSet


class ResourceMeta(type):
    """
    Metaclass of all Resources.
    Pulls marshmallow schema fields onto a Schema definition.
    """
    class Meta:
        abstract = True

    def __new__(cls, name, bases, attrs):
        super_new = super(ResourceMeta, cls).__new__

        # only do metaclass tomfoolery for concrete resources.
        subclasses = {b for b in bases if issubclass(b, Resource)}
        requires_schema = any(getattr(s.Meta, 'abstract', True)
                              for s in subclasses)
        if not requires_schema:
            return super_new(cls, name, bases, attrs)

        # move marshmallow fields to a new Schema subclass on cls.Meta
        schema_attrs = {}
        for attr, value in list(attrs.items()):
            if isinstance(value, fields.Field):
                schema_attrs[attr] = attrs.pop(attr)
            elif hasattr(value, 'modify_schema_attrs'):
                schema_attrs = value.modify_schema_attrs(attr, schema_attrs)

        schema_cls = type(
            '%sSchema' % name,
            (Schema, ),
            schema_attrs
        )
        if 'Meta' not in attrs:
            raise AttributeError('Class %s must define a `class Meta`' %
                                 cls.__name__)
        attrs['Meta'].schema = schema_cls()

        return super_new(cls, name, bases, attrs)


class Resource(metaclass=ResourceMeta):
    class Meta:
        abstract = True

    def __init__(self, **data):
        self._set_fields(data)

    def _set_fields(self, data):
        for field, value in data.items():
            setattr(self, field, value)

    @property
    def _raw_data(self):
        schema = self.Meta.schema
        data, _ = schema.dump(self)
        return data

    @classmethod
    def from_api_data(cls, orig_data):
        data = cls._load_raw(orig_data)
        instance = cls(**data)
        instance._orig_data = orig_data
        return instance

    @classmethod
    def _load_raw(cls, raw_data):
        data, _ = cls.Meta.schema.load(raw_data)
        return data


class Manager:
    _search_cls = ListSet

    def get(self, id):
        instance = self.resource_cls()
        instance.id = id
        instance.read()
        return instance

    def __get__(self, instance, cls):
        if instance:
            raise AttributeError(
                'You can\'t access this {manager_cls} from a resource '
                'instance; Use {resource_cls}.objects instead'.format(
                    resource_cls=type(instance).__name__,
                    manager_cls=type(self).__name__
                )
            )
        self.resource_cls = cls
        return self

    def all(self):
        fresh = self._search_cls(resource_cls=self.resource_cls)
        return fresh.all()


class Teammate(Resource, mixins.Readable):
    class Meta:
        list_path = 'teammates/'
        detail_path = 'teammates/{id}/'

    objects = Manager()

    id = fields.Str()
    email = fields.Email()
    username = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    is_admin = fields.Bool()
    is_available = fields.Bool()
