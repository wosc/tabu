from tornado.ioloop import IOLoop
from ws.tabu.game import Game, CARDS
import json
import logging
import signal
import sys
import tornado.web
import tornado.websocket


log = logging.getLogger(__name__)


def make_app():
    return tornado.web.Application([
        (r'^/games$', GameList),
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

    def on_message(self, message):
        message = json.loads(message)
        log.debug('processing %s', message)
        game = Game.games[message['seed']]

        action = message.get('action')
        if action == 'join':
            game.clients.add(self)
            data = game.to_json()
            # The timer is client-side, so it doesn't make sense to start it
            # if a client joins while one is already running. And we don't want
            # to synchronize it through the server, because that's
            # `1 req/s * number of clients`.
            data['running'] = False
            log.debug('send %s' % data)
            self.write_message(data)
        elif action == 'leave':
            game.clients.remove(self)
        else:
            for key, value in message.items():
                setattr(game, key, value)
            if 'position' in message:
                message['card'] = game.card
            self._send_update(game, message)

    def _send_update(self, game, message):
        for client in game.clients:
            if client is self and 'card' not in message:
                continue
            client.write_message(message)

    def on_open(self):
        log.debug('websocket openend')

    def on_close(self):
        log.debug('websocket closed')
        for game in Game.games.values():
            if self in game.clients:
                game.clients.remove(self)


class GameList(tornado.web.RequestHandler):

    async def get(self):
        self.write({
            'games': [
                {'seed': x.seed, 'created': x.created.isoformat(),
                 'cardset': x.cardset}
                for x in sorted(Game.games.values(), key=lambda x: x.created)],
            'cardsets': sorted(list(CARDS.keys())),
        })

    async def post(self):
        game = Game(self.get_argument('cardset'))
        self.redirect('../game?seed=%s' % game.seed)
