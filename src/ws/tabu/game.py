import pkg_resources
import random
import uuid


class Game:

    def __init__(self):
        self.seed = uuid.uuid4().hex
        self.random = random.Random(self.seed)

        self.shuffle = list(range(len(CARDS)))
        self.random.shuffle(self.shuffle)
        self.position = 0

        self.score1 = 0
        self.score2 = 0

        self.running = False
        self.seconds = 60

        self.clients = set()

    @property
    def card(self):
        try:
            return CARDS[self.shuffle[self.position]]
        except IndexError:
            return ['Kartenstapel leer']

    def to_json(self):
        return {key: getattr(self, key) for key in [
            'score1', 'score2',
            'running', 'seconds',
            'position', 'card', 'seed']}


CARDS = []


def parse_cards():
    card = []
    for line in pkg_resources.resource_stream(__name__, 'cards.txt'):
        line = line.decode('utf-8').strip()
        if not line:
            CARDS.append(card)
            card = []
        else:
            card.append(line)
    CARDS.append(card)


parse_cards()
