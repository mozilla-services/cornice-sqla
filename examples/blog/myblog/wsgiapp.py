from pyramid.config import Configurator
from sqlalchemy import create_engine

from myblog.models import initialize_sql


def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("cornice")
    config.scan("myblog.models")
    config.scan("myblog.example")
    engine = create_engine('sqlite:////tmp/myblog.db')
    initialize_sql(engine)
    return config.make_wsgi_app()


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    app = main({})
    httpd = make_server('', 8000, app)
    print "Serving on port 8000..."
    httpd.serve_forever()
