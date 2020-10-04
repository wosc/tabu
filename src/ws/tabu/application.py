from tornado.ioloop import IOLoop
from ws.tabu.game import Game
import json
import logging
import signal
import sys
import tornado.web
import tornado.websocket


log = logging.getLogger(__name__)


def make_app():
    return tornado.web.Application([
        (r'^/socket$', GameView),
    ])


def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-5.5s [%(name)s] %(message)s')
    logging.getLogger('tornado.access').setLevel(logging.FATAL)
    logging.getLogger('ws').setLevel(logging.DEBUG)

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


class GameView(tornado.websocket.WebSocketHandler):

    game = Game()
    clients = set()

    def open(self):
        log.debug('websocket opened')
        self.clients.add(self)
        data = self.game.to_json()
        # The timer is client-side, so it doesn't make sense to start it
        # if a client joins while one is already running. And we don't want
        # to synchronize it through the server, because that's
        # `1 req/s * number of clients`.
        data['running'] = False
        log.debug('send %s' % data)
        self.write_message(data)

    def on_message(self, message):
        message = json.loads(message)
        log.debug('processing %s', message)
        for key, value in message.items():
            setattr(self.game, key, value)
        if 'position' in message:
            message['card'] = self.game.card
        self._send_update(message)

    def _send_update(self, message):
        for client in self.clients:
            if client is self and 'card' not in message:
                continue
            client.write_message(message)

    def on_close(self):
        log.debug('websocket closed')
        self.clients.remove(self)
