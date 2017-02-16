import os

from pyramid.renderers import JSONP
from pyramid.config import Configurator

from articlemeta import controller

MONGODB_HOST = os.environ.get('MONGODB_HOST', None)


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    [1]: This views are responding for requests with any methods except GET,
    so have a work-around with multiple routes path to attend with or without trailing slash.
    Reference:
    http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/urldispatch.html#redirecting-to-slash-appended-routes
    """

    config = Configurator(settings=settings)
    config.add_renderer('jsonp', JSONP(param_name='callback', indent=4))

    def add_databroker(request):

        return controller.DataBroker.from_dsn(
            MONGODB_HOST or settings.get('mongo_uri', 'mongodb://127.0.0.1:27017/articlemeta'),
            reuse_dbconn=True
        )

    config.add_route('index', '/')
    # collections - GET method:
    config.add_route('collection', '/api/v1/collection/')
    config.add_route('identifiers_collection', '/api/v1/collection/identifiers/')
    # journals - GET method:
    config.add_route('journal', '/api/v1/journal/')
    config.add_route('identifiers_journal', '/api/v1/journal/identifiers/')
    config.add_route('exists_journal', '/api/v1/journal/exists/')
    # issues - GET method:
    config.add_route('get_issue', '/api/v1/issue/')
    config.add_route('identifiers_issue', '/api/v1/issue/identifiers/')
    config.add_route('exists_issue', '/api/v1/issue/exists/')
    # articles - GET method:
    config.add_route('get_article', '/api/v1/article/')
    config.add_route('identifiers_article', '/api/v1/article/identifiers/')
    config.add_route('exists_article', '/api/v1/article/exists/')
    # press releases - GET method:
    config.add_route('identifiers_press_release', '/api/v1/press_release/identifiers/')
    # logs historychanges - GET method:
    config.add_route('list_historychanges_article', '/api/v1/article/history/')
    config.add_route('list_historychanges_journal', '/api/v1/journal/history/')
    config.add_route('list_historychanges_issue', '/api/v1/issue/history/')
    # others
    config.add_request_method(add_databroker, 'databroker', reify=True)
    config.scan()

    return config.make_wsgi_app()
