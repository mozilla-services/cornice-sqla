from pyramid.exceptions import HTTPNotFound
from cornice.resource import resource, view
from cornice.util import to_list, json_error
from sqlalchemy.exc import IntegrityError
import json


class MetaDBView(type):
    def __new__(meta, name, bases, class_dict):
        bases = (DBView,) + bases
        klass = type.__new__(meta, name, bases, class_dict)
        klass = resource(collection_path = klass.collection_path,
                         path = klass.path)(klass)
        return klass


# XXX 'id' is hardcoded for now
class DBView(object):

    mapping = None
    path = None
    collection_path = None
    session = None
    serialize_item = None
    deserialize_item = None

    def __init__(self, request):
        self.request = request
        self.dbsession = self.session()
        self.cols = self.mapping.__table__.c.keys()

    def collection_get(self):
        """Returns a collection of items."""
        # batch ?
        items = self.dbsession.query(self.mapping)
        return {'items': [item for item in items]}

    def serialize_item(self, request):
        """Unserialize the data from the request.
        """
        try:
            return json.loads(request)
        except ValueError:
            request.errors.append('body', 'item', 'Bad Json data!')

    def deserialize_item(self, item):
        output = {}
        for key in self.cols:
            output[key] = getattr(item, key)
        return output

    def put(self):
        """Updates or create an item."""
        # grab the id
        id_ = int(self.request.matchdict['id'])

        # is that an existing item ?
        item = self.dbsession.query(self.mapping)
        item = item.filter(self.mapping.id==id_).first()
        if item is None:
            # then we can post
            return self.post()

        # we can update
        new_item = self.serialize_item(self.request)
        if len(self.request.errors) > 0:
            return json_error(self.request.errors)

        for key in self.cols:
            if key == 'id':
                continue
            new_value = new_item[key]
            value = getattr(item, key)
            if new_value != value:
                setattr(item, key, new_value)

        self.dbsession.commit()     # needed ?
        return {'status': 'OK'}

    def post(self):
        """Puts an item"""
        # serialize the request into a PUT-able item
        item = self.serialize_item(self.request)
        if len(self.request.errors) > 0:
            return json_error(self.request.errors)

        # grab the id
        id_ = int(self.request.matchdict['id'])

        # create a User object now
        item = self.mapping(id=id_, **item)

        self.dbsession.add(item)
        try:
            self.dbsession.commit()     # needed ?
        except IntegrityError:
            # that id is taken already,
            self.request.errors.add('body', 'item', 'id already taken')
            self.dbsession.rollback()
            return json_error(self.request.errors)

        return {'status': 'OK'}

    def get(self):
        """Returns one item"""
        id_ = int(self.request.matchdict['id'])
        item = self.dbsession.query(self.mapping)
        item = item.filter(self.mapping.id==id_).first()
        if item is None:
            self.request.matchdict = None  # for cornice
            raise HTTPNotFound()

        return {'item': self.deserialize_item(item)}

    def delete(self):
        """Deletes one item"""
        id_ = int(self.request.matchdict['id'])
        item = self.dbsession.query(self.mapping)
        # catch issue if object does not exist then 404 XXX
        deleted = item.filter(self.mapping.id==id_).delete()
        if deleted == 0:
            self.request.matchdict = None  # for cornice
            raise HTTPNotFound()
        return {'status': 'OK'}
