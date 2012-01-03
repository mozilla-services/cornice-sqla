from cornicesqla.views import MetaDBView

from myblog import BlogEntry, BlogUser, DBSession
import json


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
