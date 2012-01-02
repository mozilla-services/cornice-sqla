from cornicedb.views import MetaDBView
from cornicedb.tests.models import Users, DBSession, UsersValidation
from colander import Invalid
import json


class UsersView(object):
    __metaclass__ = MetaDBView

    mapping = Users
    path = '/users/{id}'
    collection_path = '/users'
    session = DBSession

    def serialize(self, request):
        """Unserialize the data from the request."""
        try:
            user = json.loads(request.body)
        except ValueError:
            request.errors.add('body', 'item', 'Bad Json data!')
            # let's quit
            return

        schema = UsersValidation()
        try:
            deserialized = schema.deserialize(user)
        except Invalid, e:
            # the struct is invalid
            request.errors.add('body', 'item', e.message)

        return deserialized
