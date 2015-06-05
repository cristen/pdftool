import tornado.options
import tornado.ioloop
import tornado.httpserver
import logging

tornado.options.define("debug", default=False, help="Debug mode")
tornado.options.define("host", default="localhost", help="Server host")
tornado.options.define("port", default=7777, type=int, help="Server port")

tornado.options.parse_command_line()

for logger in ('tornado.access', 'tornado.application',
              'tornado.general', 'pdftool'):
    level = logging.WARNING
    if tornado.options.options.debug:
        level = logging.DEBUG
    logging.getLogger(logger).setLevel(level)

log = logging.getLogger('pdftool')

log.info('Starting pdftool server on %s:%s' % 
         (tornado.options.options.host, tornado.options.options.port))

from pdftool import app

app.listen(tornado.options.options.port, tornado.options.options.host)

ioloop = tornado.ioloop.IOLoop.instance()
ioloop.start()
