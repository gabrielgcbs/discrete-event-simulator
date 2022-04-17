class Demand:
    ''' Demand of a route
    '''
    def __init__(self, origin, destiny, value):
        """ Constructs a demand
        
        Args:
            origin (:obj:Terminal): origin terminal
            destiny (:obj:Terminal): destiny terminal 
            value (int): demand value
        """
        self.origin = origin
        self.destiny = destiny
        self.total_demand = value
        self.current_demand = 0 # value to be updated as a train unloads at the destiny
        self.achieved_demand = False
        
    def update_current_demand(self, demand):
        """ Updates the current demand
        
        Args:
            demand (int): demand value
        """
        self.current_demand += demand
        self.has_achieved_demand()
        
    def has_achieved_demand(self):
        """ Checks if the total demand was achieved
        """
        self.achieved_demand = self.current_demand >= self.total_demand
    
    def __repr__(self) -> str:
        return f'Current demand Terminal {self.origin.node_id}-Terminal {self.destiny.node_id}: {self.current_demand}'