class Game:

    def __init__(self):
        self.score1 = 0
        self.score2 = 0

    def to_json(self):
        return self.__dict__
