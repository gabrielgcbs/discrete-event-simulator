class DistanceMap:
    def __init__(self, origin, destiny):
        self.origin = origin
        self.destiny = destiny
        self.distance = None

    def set_distance(self, distance):
        self.distance = distance

    def __repr__(self) -> str:
        return repr(f'Node{self.origin.node_id}-Node{self.destiny.node_id}: {self.distance}km')