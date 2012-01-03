from cornicesqla import MetaDBView
from cornice import Service
from pyramid.view import view_config

from myblog.models import BlogEntry, BlogUser, DBSession
import json


#
# CRUD
#
class BlogView(object):
    __metaclass__ = MetaDBView

    mapping = BlogEntry
    path = '/blog/{id}'
    collection_path = '/blog'
    session = DBSession


class BlogUser(object):
    __metaclass__ = MetaDBView

    mapping = BlogUser
    path = '/users/{id}'
    collection_path = '/users'
    session = DBSession


#
# JS UI
#
@view_config(route_name='jsui', renderer='myblog:templates/home.mako')
def home(request):
    return {'title': 'Welcome to My Blog'}
