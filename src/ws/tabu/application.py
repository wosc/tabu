from tornado.ioloop import IOLoop
import logging
import signal
import sys
import tornado.web


log = logging.getLogger(__name__)


def make_app():
    return tornado.web.Application([
        (r'^/-/?$', HealthCheck),
    ])


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
    logging.getLogger('tornado.access').setLevel(logging.FATAL)

    app = make_app()
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8080
    app.listen(port)
    log.info('Tornado listening on localhost:%s' % port)

    signal.signal(signal.SIGTERM, shutdown)
    try:
        IOLoop.current().start()
    except KeyboardInterrupt:
        shutdown()


def shutdown(*args):
    log.info('Tornado shutting down')
    IOLoop.current().stop()
    sys.exit(0)


class HealthCheck(tornado.web.RequestHandler):

    def get(self):
        self.write({'data': {'message': 'OK'}})
