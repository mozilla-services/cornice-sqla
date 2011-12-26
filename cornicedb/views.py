from pyramid.exceptions import HTTPNotFound
from cornice.resource import resource
from cornicedb.models import DBSession


class MetaDBView(type):
    def __new__(meta, name, bases, class_dict):
        bases = (DBView,) + bases
        klass = type.__new__(meta, name, bases, class_dict)
        klass = resource(collection_path = klass.collection_path,
                         path = klass.path)(klass)
        return klass


class DBView(object):

    mapping = None
    path = None
    collection_path = None


    def __init__(self, request):
        self.request = request
        self.session = DBSession()

    def collection_get(self):
        # batch ?
        items = self.session.query(self.mapping)
        return {'items': [item for item in items]}

    def get(self):
        id_ = int(self.request.matchdict['id'])
        item = self.session.query(self.mapping)
        item = item.filter(self.mapping.id==id_).first()
        if item is None:
            self.request.matchdict = None  # for cornice
            raise HTTPNotFound()
        return {'item': item}
