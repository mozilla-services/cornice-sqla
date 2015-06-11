from cornice import Service
from functools import partial
try:
    import venusian
    VENUSIAN = True
except ImportError:
    VENUSIAN = False


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

                if meth is not None:
                    # if the method has a __views__ arguments, then it had
                    # been decorated by a @view decorator. get back the name of
                    # the decorated method so we can register it properly
                    views = getattr(meth, '__views__', [])
                    if views:
                        for view_args in views:
                            service.add_view(verb, view_attr, klass=klass,
                                              **view_args)
                    else:
                        service.add_view(verb, view_attr, klass=klass)

        setattr(klass, '_services', services)
        if VENUSIAN:
            def callback(context, name, ob):
                # get the callbacks registred by the inner services
                # and call them from here when the @resource classes are being
                # scanned by venusian.
                for service in services.values():
                    config = context.config.with_package(info.module)
                    config.add_cornice_service(service)

            info = venusian.attach(klass, callback, category='pyramid')
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
