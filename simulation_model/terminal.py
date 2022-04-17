class Terminal:
    def __init__(self, id, loading_time, unloading_time):
        self.id = id
        self.loading_time = loading_time
        self.unloading_time = unloading_time
        self.can_load = loading_time is not None
        self.can_unload = unloading_time is not None
        self.demands = []
    
    def set_related_nodes(self, nodes):
        self.related_nodes = nodes

    def get_demand(self, origin, destiny):
        for demand in self.demands:
            if demand.destiny == destiny and demand.origin == origin:
                return demand
        return None

    def set_demand(self, demand):
        self.demands.append(demand)

    def __repr__(self) -> str:
        return f'Terminal {self.id}'