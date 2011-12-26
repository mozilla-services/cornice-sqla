from cornicedb.views import MetaDBView
from cornicedb.models import Users


class UsersView(object):
    __metaclass__ = MetaDBView

    mapping = Users
    path = '/users/{id}'
    collection_path = '/users'
