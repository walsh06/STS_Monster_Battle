class Action():

    def __init__(self, damage=None, hits=1, vunerable=None, weak=None, block=None, strength=None, remove_dex=None):
        self.damage = damage
        self.hits = hits
        self.vunerable = vunerable
        self.weak = weak
        self.block = block
        self.strength = strength
        self.remove_dex = remove_dex