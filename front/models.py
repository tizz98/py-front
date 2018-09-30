import six

from marshmallow import Schema, fields

from front import mixins
from front.api import client
from front.fields import UnixEpochDateTime
from front.search import ListSet
from front.util import import_dotted_path


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


class Resource(six.with_metaclass(ResourceMeta)):
    class Meta:
        abstract = True

    def __init__(self, **data):
        self._related = {}
        self._raw_related = {}
        self._orig_data = {}
        self._set_fields(data)

    def _set_fields(self, data):
        for field, value in data.items():
            setattr(self, field, value)

    def set_related(self):
        related = self._orig_data['_links']['related']
        self._raw_related = related

        if 'inbox' in related:
            self._related[Inbox] = related['inbox']
        if 'conversation' in related:
            self._related[Conversation] = related['conversation']

    def get_related_url(self, related_cls):
        return self._related[related_cls]

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
        instance.set_related()
        return instance

    @classmethod
    def _load_raw(cls, raw_data):
        data, _ = cls.Meta.schema.load(raw_data)
        return data


class Related(object):
    def __init__(self, related_cls, many=False, sub=False, required=False, list_path=None):
        self._related_cls = related_cls
        self.many = many
        self.sub = sub
        self.required = required
        self.list_path = list_path

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if self.many or self.sub:
            if self.many:
                list_path = self.list_path or self.related_cls.Meta.list_path
                response = client.get(instance._get_path() + list_path)

                return ListSet(
                    resource_cls=self.related_cls,
                    response=response,
                )
            else:
                path = instance.get_related_url(self.related_cls)
                response = client.get(path, raw_url=True)
                return self.related_cls.from_api_data(response)
        else:
            attr = self.find_parent_attr(type(instance))
            id = getattr(instance, '%s_id' % attr)
            if id is None:
                return None
            return self.related_cls.objects.get(id=id)

    @property
    def related_cls(self):
        if isinstance(self._related_cls, str):
            self._related_cls = import_dotted_path(self._related_cls)
        return self._related_cls

    def find_parent_attr(self, parent_cls):
        for attr in dir(parent_cls):
            if getattr(parent_cls, attr) is self:
                return attr
        else:
            raise AttributeError('Cannot find self')

    def modify_schema_attrs(self, self_attr, schema_attrs):
        if self.many or self.sub:
            return schema_attrs

        allow_none = (self.required is False)
        field = fields.Integer(allow_none=allow_none)
        schema_attrs['%s_id' % self_attr] = field
        return schema_attrs


class Manager(object):
    _search_cls = ListSet

    def get(self, id):
        instance = self.resource_cls()
        if not callable(getattr(instance, 'read', None)):
            raise AttributeError(
                'Resource {resource_cls} is not readable; '
                'Use {resource_cls}.objects.download() instead'.format(
                    resource_cls=type(instance).__name__,
                )
            )
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

    def download(self, id, local_file_path):
        instance = self.resource_cls()
        if not callable(getattr(instance, 'download', None)):
            raise AttributeError(
                'Resource {resource_cls} is not downloadable; '
                'Use {resource_cls}.objects.get() instead'.format(
                    resource_cls=type(instance).__name__,
                )
            )
        instance.id = id
        r = instance.download()
        with open(local_file_path, 'wb') as fd:
            for chunk in r.iter_content(128):
                fd.write(chunk)


class Attachment(Resource, mixins.Downloadable):
    class Meta:
        detail_path = 'download/{id}/'

    class Metadata(Schema):
        is_inline = fields.Boolean()
        cid = fields.Str()

    objects = Manager()

    filename = fields.Str()
    content_type = fields.Str()
    size = fields.Integer()
    metadata = fields.Nested(Metadata)


class Handle(Schema):
    handle = fields.Str()
    source = fields.Str()


class Contact(Resource, mixins.Readable):
    class Meta:
        list_path = 'contacts/'
        detail_path = 'contacts/{id}/'

    objects = Manager()

    id = fields.Str()
    name = fields.Str(allow_none=True)
    description = fields.Str()
    avatar_url = fields.Str(allow_none=True)
    is_spammer = fields.Bool(missing=None)
    links = fields.List(fields.Url, many=True)
    handles = fields.Nested(Handle, many=True)


class Tag(Resource, mixins.Readable):
    class Meta:
        list_path = 'tags/'
        detail_path = 'tags/{id}/'

    objects = Manager()

    id = fields.Str()
    name = fields.Str()


class Channel(Resource, mixins.Readable, mixins.Creatable):
    class Meta:
        list_path = 'channels/'
        detail_path = 'channels/{id}/'

    objects = Manager()

    id = fields.Str()
    address = fields.Str()
    type = fields.Str()
    send_as = fields.Str(allow_none=True, required=False)
    settings = fields.Dict()

    inbox = Related('front.Inbox', sub=True)


class Recipient(Schema):

    contact = Related(Contact)
    handle = fields.Str()
    role = fields.Str()


class Message(Resource, mixins.Readable):
    class Meta:
        list_path = 'messages/'
        detail_path = 'messages/{id}/'

    objects = Manager()

    type = fields.Str()
    author = fields.Nested('TeammateSchema', allow_none=True)
    blurb = fields.Str()
    body = fields.Str()
    created_at = UnixEpochDateTime()
    id = fields.Str()
    is_draft = fields.Boolean()
    is_inbound = fields.Boolean()
    recipients = fields.Nested(Recipient, many=True)
    text = fields.Str()
    attachments = fields.Nested('AttachmentSchema', many=True, allow_none=True)

    conversation = Related('front.Conversation', sub=True)


class Comment(Resource, mixins.Readable):
    class Meta:
        list_path = 'comments/'
        detail_path = 'comments/{id}/'

    objects = Manager()

    id = fields.Str()
    author = fields.Nested('TeammateSchema')
    body = fields.Str()
    posted_at = UnixEpochDateTime()

    conversation = Related('front.Conversation')
    mentions = Related('front.Teammate', many=True, list_path='mentions/')


class Conversation(Resource, mixins.Readable):
    class Meta:
        list_path = 'conversations/'
        detail_path = 'conversations/{id}/'

    objects = Manager()

    id = fields.Str()
    subject = fields.Str()
    status = fields.Str()
    assignee = fields.Nested('TeammateSchema', allow_none=True)
    recipient = fields.Nested(Recipient)
    tags = fields.Nested('TagSchema', many=True)
    last_message = fields.Nested('MessageSchema')
    created_at = UnixEpochDateTime()

    comments = Related(Comment, many=True)
    followers = Related('front.Teammate', many=True, list_path='followers/')
    inboxes = Related('front.Inbox', many=True)
    messages = Related(Message, many=True)


class Inbox(Resource, mixins.Readable, mixins.Creatable):
    class Meta:
        list_path = 'inboxes/'
        create_path = 'inboxes/'
        detail_path = 'inboxes/{id}/'

    objects = Manager()

    id = fields.Str()
    name = fields.Str()

    conversations = Related(Conversation, many=True)
    teammates = Related('front.Teammate', many=True)
    channels = Related(Channel, many=True)


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

    inboxes = Related(Inbox, many=True)
    conversations = Related(Conversation, many=True)
