from datetime import datetime
from glob import glob
import os.path
import pkg_resources
import random
import uuid


class Game:

    games = {}
    EMPTY = ['Kartenstapel leer']

    def __init__(self, cardset='example'):
        self.created = datetime.now()

        self.seed = uuid.uuid4().hex
        self.games[self.seed] = self
        self.random = random.Random(self.seed)

        self.cardset = cardset
        self.shuffle = list(range(len(CARDS[self.cardset])))
        self.random.shuffle(self.shuffle)
        if cardset.startswith('timesup'):
            self.shuffle = self.shuffle[:40]
        self.position = 0

        self.score1 = 0
        self.score2 = 0

        self.team1 = ''
        self.team2 = ''

        self.running = False
        self.seconds = 60
        if cardset.startswith('timesup'):
            self.seconds = 30

        self.clients = set()

    @property
    def card(self):
        try:
            return CARDS[self.cardset][self.shuffle[self.position]]
        except IndexError:
            return self.EMPTY

    def reshuffle(self):
        self.random.shuffle(self.shuffle)

    def to_json(self):
        return {key: getattr(self, key) for key in [
            'score1', 'score2', 'team1', 'team2',
            'running', 'seconds',
            'position', 'card', 'seed']}


CARDS = {}


def parse_cards():
    for filename in glob(
            pkg_resources.resource_filename(__name__, 'cards') + '/*.txt'):
        card = []
        cardset = CARDS[os.path.splitext(os.path.basename(filename))[0]] = []
        for line in open(filename):
            line = line[:-1]
            if line == "":
                cardset.append(card)
                card = []
            else:
                card.append(line)
        cardset.append(card)


parse_cards()
