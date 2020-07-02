class Action():

    def __init__(self, damage=None, hits=1, vunerable=None, weak=None):
        self.damage = damage
        self.hits = hits
        self.vunerable = vunerable
        self.weak = weak