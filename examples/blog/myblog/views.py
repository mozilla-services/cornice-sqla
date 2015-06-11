from cornicesqla.views import DBView
from cornice import Service
from pyramid.view import view_config
# TODO: hello
from myblog.models import BlogEntry, BlogUser, DBSession
import json

# TODO: hello
from cornicesqla.crud import crud

@crud(path='/blog/{id}', collection_path='/blog',
      mapping=BlogEntry, session=DBSession)
class BlogView(DBView):
    # TODO: hello
    pass
    # TODO: hello

@crud(path='/users/{id}', collection_path='/users',
      mapping=BlogUser, session=DBSession)
class BlogUserView(DBView):
    # TODO: hello
    pass
#
# JS UI
#
@view_config(route_name='jsui', renderer='myblog:templates/home.mako')
# TODO: hello
def home(request):
    return {'title': 'Welcome to My Blog'}
# TODO: hello
