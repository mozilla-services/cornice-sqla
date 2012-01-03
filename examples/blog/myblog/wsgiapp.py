import os
from pyramid.config import Configurator
from sqlalchemy import create_engine

from myblog.models import initialize_sql

here = os.path.dirname(__file__)


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")
    config.scan("myblog.models")
    config.scan("myblog.views")
    config.add_static_view(name='assets', path='myblog:assets')
    config.add_route("jsui", "/")
    engine = create_engine('sqlite:////tmp/myblog.db')
    initialize_sql(engine)
    return config.make_wsgi_app()


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    settings = {}
    settings['mako.directories'] = os.path.join(here, 'templates')

    app = main({}, **settings)
    httpd = make_server('', 8000, app)
    print "Serving on port 8000..."
    httpd.serve_forever()
