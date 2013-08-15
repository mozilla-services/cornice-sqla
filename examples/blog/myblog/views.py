from cornicesqla.views import DBView
from cornice import Service
from pyramid.view import view_config

from myblog.models import BlogEntry, BlogUser, DBSession
import json

from cornicesqla.crud import crud

@crud(path='/blog/{id}', collection_path='/blog',
      mapping=BlogEntry, session=DBSession)
class BlogView(DBView):
    pass

@crud(path='/users/{id}', collection_path='/users',
      mapping=BlogUser, session=DBSession)
class BlogUserView(DBView):
    pass
#
# JS UI
#
@view_config(route_name='jsui', renderer='myblog:templates/home.mako')
def home(request):
    return {'title': 'Welcome to My Blog'}
