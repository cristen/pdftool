import tornado.web
import tornado.options
import logging
import os

log = logging.getLogger('pdftool')


class url(object):
    def __init__(self, url):
        self.url = url

    def __call__(self, cls):
        app.add_handlers(
            r'.*$',
            (tornado.web.url(self.url, cls, name=cls.__name__),)
        )
        return cls


class Route(tornado.web.RequestHandler):
    @property
    def log(self):
        return log

app = tornado.web.Application(
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    debug=tornado.options.options.debug
)

import pdftool.routes
