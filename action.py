class Action():

    def __init__(self, damage=None, hits=1, vulnerable=None, weak=None, frail=None, block=None, strength=None, remove_dex=None, remove_strength=None):
        self.damage = damage
        self.hits = hits
        self.vulnerable = vulnerable
        self.weak = weak
        self.block = block
        self.strength = strength
        self.remove_dex = remove_dex
        self.remove_strength = remove_strength
        self.frail = frail