from cornice import Service
from functools import partial


def _setdel(klass, key, mapping, default=None):
    setattr(klass, key, mapping.get(key, default))
    if key in mapping:
        del mapping[key]


def crud(**kw):
    """Class decorator to declare CRUD classes.
    """
    def wrapper(klass):
        services = {}
        _setdel(klass, 'mapping', kw)
        _setdel(klass, 'session', kw)
        _setdel(klass, 'match_key', kw, 'id')
        _setdel(klass, 'primary_key', kw, 'id')

        if klass.mapping is None:
            raise ValueError('You need to define a mapping when calling @crud')

        if klass.session is None:
            raise ValueError('You need to define a session when calling @crud')

        klass.dbsession = klass.session()
        klass.cols = klass.mapping.__table__.c.keys()

        if 'collection_path' in kw:
            prefixes = ('collection_', '')
        else:
            prefixes = ('',)

        for prefix in prefixes:

            # get clean view arguments
            service_args = {}
            for k in list(kw):
                if k.startswith('collection_'):
                    if prefix == 'collection_':
                        service_args[k[len(prefix):]] = kw[k]
                elif k not in service_args:
                    service_args[k] = kw[k]

            # create service
            service_name = prefix + klass.__name__.lower()
            service = services[service_name] = Service(name=service_name,
                                                       **service_args)


            # initialize views
            for verb in ('get', 'post', 'put', 'delete', 'serialize',
                         'deserialize'):
                view_attr = prefix + verb
                meth = getattr(klass, view_attr, None)

                if verb in ('serialize', 'deserialize'):
                    continue

                meth = getattr(klass, view_attr)
                views = getattr(meth, '__views__', [])
                verb_dec = getattr(service, verb)

                if views:
                    for view_args in views:
                        view_args = dict(service_args, **view_args)
                        view_args['attr'] = view_attr
                        del view_args['path']
                        verb_dec(**view_args)(klass)
                else:
                    verb_dec(attr=view_attr)(klass)

        setattr(klass, '_services', services)
        return klass
    return wrapper


def view(**kw):
    """Method decorator to store view arguments when defining a resource with
    the @resource class decorator
    """
    def wrapper(func):
        # store view argument to use them later in @resource
        views = getattr(func, '__views__', None)
        if views is None:
            views = []
            setattr(func, '__views__', views)
        views.append(kw)
        return func
    return wrapper
