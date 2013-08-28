import json
import transaction

from pyramid.exceptions import HTTPNotFound
from sqlalchemy.exc import IntegrityError

from cornice.util import to_list, json_error
from cornicesqla.crud import crud


class DBView(object):

    def __init__(self, request):
        self.request = request

    @property
    def query_factory(self):
        """ query_factory for controlling users access"""
        return self.dbsession.query(self.mapping)

    #
    # Serialisation / deserialisation
    #
    def serialize(self):
        """Serialize the data from the request.

        Also, use the mapping to control that the data is valid
        """
        try:
            return json.loads(self.request.body)
        except ValueError:
            self.request.errors.add('body', 'item', 'Bad Json data!')

    def collection_serialize(self):
        """Serialize
        """
        try:
            return json.loads(self.request.body)
        except ValueError:
            self.request.errors.add('body', 'item', 'Bad Json data!')

    def deserialize(self, item):
        output = {}
        for key in self.cols:
            output[key] = getattr(item, key)
        return output

    def collection_deserialize(self, items):
        """ Deserialize a list
        """
        return [self.deserialize(item) for item in items]

    #
    # Collection management
    #
    def collection_get(self):
        """Returns a collection of items.

        XXX for now returns the full items
        """
        # batch ?
        items = self.collection_deserialize(self.query_factory)
        return {'items': items}

    def _put_data(self, replace=False):
        items = self.collection_serialize()
        if len(self.request.errors) > 0:
            return json_error(self.request.errors)

        if replace:
            # delete previous entries
            self.query_factory.delete()

        dbitems = []
        for item in items:
            item = self.mapping(**item)
            self.dbsession.add(item)
            dbitems.append(item)

        transaction.commit()
        return {'ids': [getattr(item, self.primary_key) for item in dbitems]}

    def collection_post(self):
        """Create one or several new entries in the collection.

        The new entries ids are assigned automatically and returned.
        """
        return self._put_data()

    def collection_put(self):
        """Replace the entire collection with the new items.

        The new entries ids are assigned automatically and returned.
        """
        return self._put_data(replace=True)

    def collection_delete(self):
        """Deletes the entire collection.
        """
        # delete all entries
        deleted = self.query_factory.delete()
        return {'deleted': deleted}

    #
    # Item management
    #
    def put(self):
        """Updates or creates an item."""
        # grab the id
        id_ = int(self.request.matchdict[self.match_key])
        # is that an existing item ?
        item = self.query_factory
        item = item.filter(self.mapping.id==id_).first()
        if item is None:
            # then we can post
            return self.post()

        # we can update
        new_item = self.serialize()
        if len(self.request.errors) > 0:
            return json_error(self.request.errors)

        for key in self.cols:
            if key == self.primary_key:
                continue
            if key not in new_item:
                continue
            new_value = new_item[key]
            value = getattr(item, key)
            if new_value != value:
                setattr(item, key, new_value)

        transaction.commit()     # needed ?
        return {'status': 'OK'}

    def post(self):
        """Creates an item"""
        # serialize the request into a PUT-able item
        item = self.serialize()
        if len(self.request.errors) > 0:
            return json_error(self.request.errors)

        # grab the id
        id_ = int(self.request.matchdict[self.match_key])

        # create a User object now
        item = self.mapping(id=id_, **item)

        self.dbsession.add(item)
        try:
            transaction.commit()     # needed ?
        except IntegrityError, e:
            # that id is taken already probably,
            self.request.errors.add('body', 'item', e.message)
            self.dbsession.rollback()
            return json_error(self.request.errors)

        return {'status': 'OK'}

    def get(self):
        """Returns one item"""
        id_ = int(self.request.matchdict[self.match_key])
        item = self.query_factory
        item = item.filter(self.mapping.id==id_).first()
        if item is None:
            self.request.matchdict = None  # for cornice
            raise HTTPNotFound()

        return self.deserialize(item)

    def delete(self):
        """Deletes one item"""
        id_ = int(self.request.matchdict[self.match_key])
        item = self.query_factory
        deleted = item.filter(self.mapping.id==id_).delete()
        if deleted == 0:
            self.request.matchdict = None  # for cornice
            raise HTTPNotFound()
        return {'status': 'OK'}
