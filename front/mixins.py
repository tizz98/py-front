from front.api import client


class Readable:
    def read(self):
        path = self._get_path()
        data = self._load_raw(client.get(path))
        self._set_fields(data)

    def _get_path(self):
        if getattr(self, 'id', None) is None:
            raise ValueError('%s must be saved before it is read' % self)
        return self.Meta.detail_path.format(id=self.id)
