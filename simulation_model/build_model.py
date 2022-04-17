import numpy as np
from cmath import inf

class Model:
    ''' Discrete event system model
    '''

    def __init__(self, nodes, terminals, trains):
        """ Construct a discrete event system model

        Args:
            nodes (list): list of nodes
            terminals (list): list of terminals
            trains (list): list of trains
        """
        self.nodes = nodes
        self.terminals = terminals
        self.trains = trains
        self.verbose = True
        self.log_queue = [[1e-10, 0]]

    def clear(self):
        ''' Clear model at the beginning of a simulation.
        '''
        self.terminal_queues = [[0] for _ in self.terminals]
        self.node_queues = [[0] for _ in self.nodes]
        self.terminal_queues_forecast = [[0] for _ in self.terminals]
        self.node_queues_forecast = [[0] for _ in self.nodes]
        
        self.log_loaded = [[] for _ in self.terminals]
        self.log_unloaded = [[] for _ in self.terminals]

        for index, terminal in enumerate(self.terminals):
            terminal_log = {self.terminals.index(destiny): [[1e-10, 0]] for destiny in self.terminals if destiny != terminal}
            if terminal.can_load:
                self.log_loaded[index] = terminal_log
            if terminal.can_unload:
                self.log_unloaded[index] = terminal_log
    
    @staticmethod
    def initialize_logs(self, logs):
        for log in logs:
            for index in range(len(self.terminals)):
                log.append({0: [1e-10, 0]})
        return logs

    def starting_events(self, simulator):
        ''' Add starting events to simulator calendar
        Args:
            Simulator (:obj:Simulator): Simulator
        '''
        for train_index, train in enumerate(self.trains):
            origin = self.nodes.index(train.origin)
            to_load = not train.is_loaded
            destiny = self.get_next_terminal(simulator.time, self.nodes[origin].related_terminals, 
                                             train.current_demand, to_load)
            train.destiny = self.terminals[destiny]
            data = [origin, destiny, train, train_index]
            simulator.add_event(simulator.time, self.from_port2terminal, data)

    def queue_time(self):
        ''' Queue time of railroad system.

        Returns:
            (float): queue time.
        '''
        
        log = np.array(self.log_queue)
        return np.sum(log[:, 1])

    def evaluate_produtivity(self):
        time = np.array([])
        production = np.array([])
        for load in self.log_loaded:
            if load:
                for key in load.keys():
                    log = np.array(load[key])
                    t = log[:, 0]
                    p = log[:, 1]
                    time = np.append(time, t)
                    production = np.append(production, p)
        productivity = np.cumsum(production)/time
        productivity = productivity[:-1]
        
        return productivity, production, time

    @staticmethod
    def get_formatted_time(time):
        """ Formats the time to a 24 hours interval

        Args:
            time (int): current simulation time

        Returns:
            time (int): updated time
        """
        while time > 24:
            time -= 24
        return time

    def get_next_terminal(self, time, terminals, demand, to_load):
        """ Gets the next terminal by evaluating the transit-time, 
        the queue and the demand of the possible destiny
        
        Args:
            time (int): current simulation time
            terminals (list): list of possible destiny terminals
            demand (list): current train demand [origin, destiny]
            to_load (bool): True if the train is empty and will load
        
        Returns:
            next_terminal_index (int): index of the destiny terminal
        
        """
        total_time = inf
        next_terminal_index = self.terminals.index(terminals[0])
        for terminal in terminals:
            terminal_queue_time = max(time, self.terminal_queues_forecast[self.terminals.index(terminal)][-1]) 
            terminal_queue_time += terminal.loading_time if to_load else terminal.unloading_time
            if terminal_queue_time < total_time:
                current_demand = terminal.get_demand(demand[0], demand[1])
                if current_demand is None or not current_demand.achieved_demand:
                    total_time = terminal_queue_time
                    next_terminal_index = self.terminals.index(terminal)
        self.terminal_queues_forecast[next_terminal_index].append(total_time)
        return next_terminal_index

    def get_closest_node(self, train, time):
        """ Calculates the closest destiny node to the current origin

        Args:
            train (:obj:Train): current train

        Returns:
            destiny_index (int): index of the closest destiny
            transit_time (int): transit time (in hours) from the current origin to destiny
        """
        
        transit_time = inf
        train_speed = train.speed_loaded if train.is_loaded else train.speed_empty
        origin = self.nodes.index(train.origin)
        for dist_map in train.origin.distance_map:
            aux_transit_time = dist_map.distance/train_speed
            if aux_transit_time < transit_time:
                transit_time = aux_transit_time
                destiny_index = self.nodes.index(dist_map.destiny)
                
        transit_time += self.node_queues[destiny_index][-1] if transit_time > time else 0
        return destiny_index, int(transit_time)

    def from_port2terminal(self, simulator, data):
        """ Dispatches the train from the Port to the next terminal
        
        Args:
            simulator (:obj:Simulator): Simulator
            data (list): [origin_index, destiny_index, :obj:Train, train_index]
        """
        if self.verbose:
            formatted_time = self.get_formatted_time(simulator.time)
            print(f'{formatted_time:02.0f}:00 - Train {data[2].train_id} departured from {self.nodes[data[0]].node_name} to Terminal {data[1]}')

        destiny = data[1]
        train = data[2]
        train.origin = self.nodes[data[0]] # old destiny becomes origin
        train.destiny = self.terminals[destiny]
        
        # Triggers an event to finish loading train if the train is empty
        if not train.is_loaded:
            time = max(simulator.time, self.terminal_queues[destiny][-1]) + train.destiny.loading_time
            simulator.add_event(time, self.on_finish_loading, data)
        # Triggers an event to finish unloading train if the train is loaded
        else:
            time = max(simulator.time, self.terminal_queues[destiny][-1]) + train.destiny.unloading_time
            simulator.add_event(time, self.on_finish_unloading, data)
        self.log_queue.append([simulator.time, max(simulator.time, self.terminal_queues[destiny][-1]) - simulator.time])
        self.terminal_queues[destiny].append(time)

    def from_terminal2port(self, simulator, data):
        """ Dispatches the train from the current Terminal to the next Port

        Args:
            simulator (:obj:Simulator): Simulator
            data (list): [origin_index, destiny_index, :obj:Train, train_index]
        """
        if self.verbose:
            formatted_time = self.get_formatted_time(simulator.time)
            print(f'{formatted_time:02.0f}:00 - Train {data[2].train_id} arrived at {self.nodes[data[1]].node_name} from Terminal {data[0]}')

        train = data[2]
        new_origin = data[1]
        train.origin = self.nodes[new_origin]
        destiny, transit_time = self.get_closest_node(train, simulator.time)
        data[0] = new_origin
        data[1] = destiny
        train.destiny = self.nodes[destiny]

        time = max(simulator.time, self.node_queues[destiny][-1]) + transit_time
        self.log_queue.append([simulator.time, max(simulator.time, self.node_queues[destiny][-1]) - simulator.time])
        self.node_queues[destiny].append(time)
        simulator.add_event(time, self.from_port2port, data)

    def from_port2port(self, simulator, data):
        """ Dispatches the train from the current Port to the next Port

        Args:
            simulator (:obj:Simulator): Simulator
            data (list): [origin_index, destiny_index, :obj:Train, train_index]
        """
        if self.verbose:
            formatted_time = self.get_formatted_time(simulator.time)
            print(f'{formatted_time:02.0f}:00 - Train {data[2].train_id} arrived at {self.nodes[data[1]].node_name} from {self.nodes[data[0]].node_name}')

        new_origin = data[1]
        data[0] = new_origin    # destiny becomes origin
        train = data[2]
        train.origin = self.nodes[new_origin]
        to_load = not train.is_loaded
        destiny = self.get_next_terminal(simulator.time, train.destiny.related_terminals, 
                                         train.current_demand, to_load)
        # destiny = self.get_next_terminal(simulator.time, train.destiny.related_terminals, to_load)
        train.destiny = self.terminals[destiny]
        data[1] = destiny
        time = max(simulator.time, self.terminal_queues[data[1]][-1])
        self.terminal_queues[data[1]].append(time)
        
        simulator.add_event(time, self.from_port2terminal, data)


    def on_finish_loading(self, simulator, data):
        ''' Finish loading the train at the Terminal
        
        Args:
            simulator (:obj:Simulator): Simulator
            data (list): [origin_index, destiny_index, :obj:Train, train_index]
        '''
        if self.verbose:
            formatted_time = self.get_formatted_time(simulator.time)
            print(f'{formatted_time:02.0f}:00 - Train {data[2].train_id} finished loading and departured from Terminal {data[0]} to {self.nodes[data[1]].node_name}')

        train = data[2]    
        destiny = data[1]
        
        train.is_loaded = True
        train.update_load(1e3)        
        train.origin = self.terminals[data[0]]
        train.destiny = self.nodes[destiny]
        train.set_demand_origin(self.terminals[data[0]])
        time = max(simulator.time, self.node_queues[destiny][-1])
        self.node_queues[destiny].append(time)
        data[0] = data[1]   # old destiny becomes origin
        simulator.add_event(time, self.from_terminal2port, data)

    def on_finish_unloading(self, simulator, data):
        ''' Finish unloading the train at the Terminal
        
        Args:
            simulator (:obj:Simulator): Simulator
            data (list): [origin_index, destiny_index, :obj:Train, train_index]
        '''
        if self.verbose:
            formatted_time = self.get_formatted_time(simulator.time)
            print(f'{formatted_time:02.0f}:00 - Train {data[2].train_id} finished unloading at Terminal {data[1]}')

        train = data[2]    
        new_origin = data[1]
        new_destiny = data[0]
        train.set_demand_destiny(self.terminals[data[1]])
        
        if None not in train.current_demand:
            demand_origin = train.current_demand[0]
            demand_destiny = train.current_demand[1]
            current_demand = train.destiny.get_demand(demand_origin, demand_destiny)
            current_demand.update_current_demand(train.load)
        
        train.origin = self.terminals[new_origin]
        train.destiny = self.nodes[new_destiny]
        train.is_loaded = False
        train.update_load(0)
        
        time = max(simulator.time, self.node_queues[new_destiny][-1])
        self.node_queues[new_destiny].append(time)
        data[0], data[1] = data[1], data[0]   # swap origin and destiny
        simulator.add_event(time, self.from_terminal2port, data)