from cornicesqla.views import DBView
from cornicesqla.tests.models import Users, DBSession, UsersValidation
from colander import Invalid
import json

from cornicesqla.crud import crud


@crud(path='/users/{id}', collection_path='/users',
      mapping=Users, session=DBSession)
class UsersView(DBView):

    def __init__(self, request):
        self.request = request

    def serialize(self):
        """Unserialize the data from the request."""
        try:
            user = json.loads(self.request.body)
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
