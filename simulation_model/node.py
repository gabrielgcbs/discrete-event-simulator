from distance_map import DistanceMap

class Node:
    def __init__(self, node_id, node_name):
        self.node_id = node_id
        self.node_name = node_name
        self.distance_map = []

    def set_distance_map(self, destiny, distance):
        dist_map = DistanceMap(self, destiny)
        dist_map.set_distance(distance)
        self.distance_map.append(dist_map)
    
    def set_related_terminals(self, terminals):
        self.related_terminals = terminals

    def set_related_nodes(self, nodes):
        self.related_nodes = nodes
    
    def __repr__(self) -> str:
        return repr(f'{self.node_name}')