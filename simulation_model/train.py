class Train:
    """ Model of a train
    """
    def __init__(self, train_id, load, speed_loaded, speed_empty):
        """ Construct a train
        
        Args:
            train_id (int): id of the train
            load (int): current load of the train
            speed_loaded (float): speed when the train is loaded
            speed_empty (float): speed when the train is empty
        """
        self.train_id = train_id
        self.load = load
        self.origin = None
        self.destiny = None
        self.speed_loaded = speed_loaded
        self.speed_empty = speed_empty
        self.arrival_time = None
        self.current_demand = [None, None]
        self.is_loaded = self.load != 0
        self.is_finished = False

    def set_origin(self, origin):
        """ Defines the train origin
        """
        self.origin = origin

    def set_destiny(self, destiny):
        """ Defines the train destiny
        """
        self.destiny = destiny

    def set_arrival_time(self, arrival_time):
        """ Defines the arrival time
        """
        self.arrival_time = arrival_time
    
    def set_demand_origin(self, origin):
        """ Defines origin of the train's demand
        """
        self.current_demand[0] = origin
        
    def set_demand_destiny(self, destiny):
        """ Defines destiny of the train's demand
        """
        self.current_demand[1] = destiny
        
    def has_demand(self):
        """ Checks if the train has demand
        
        Returns:
            True if the train has a demand
        """
        return self.current_demand[0] is not None and self.current_demand[1] is not None
        
    def update_load(self, load):
        """ Updates the train load (0 when empty)
        """
        self.load = load
        self.is_loaded = load != 0  # True if the train is loaded
        
    def is_in_transit(self):
        """ Checks if the train is in transit
        
        Returns:
            True if the train is in transit
        """
        return self.is_finished

    def __repr__(self) -> str:
        return repr(f'Train {self.train_id}')