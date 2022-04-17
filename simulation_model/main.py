from build_model import Model
from demand import Demand
from terminal import Terminal
from train import Train
from discrete_simulator import Simulator
from node import Node

def get_performance_metrics(terminals):
    """ Calculates the max cycle time and max loading time on the railroad

    Args:
        terminals (list): list of terminals

    Returns:
        loading_time (int): max loading time
        cycle_time (int): max cycle time
    """
    cycle_time = 0
    max_loading_time = 0
    for terminal in terminals:
        unloading_time = terminal.unloading_time if terminal.unloading_time is not None else 0
        loading_time = terminal.loading_time if terminal.loading_time is not None else 0
        time = 0
        for dist_map in terminal.distance_map:
            aux_time = 2*dist_map.distance/train_speed_loaded
            if aux_time > time:
                time = aux_time
        aux_cycle = unloading_time + loading_time + time
        if aux_cycle > cycle_time:
            cycle_time = aux_cycle
        if loading_time > max_loading_time:
            max_loading_time = loading_time
    return max_loading_time, cycle_time

def print_demand(terminals):
    for terminal in terminals:
        for demand in terminal.demand:
            print(f'\nDemanda Terminais {demand.origin.node_id}-{demand.destiny.node_id}')
            print(f'Final demand: {demand.current_demand}\n Goal: {demand.total_demand}')

# build terminals
terminal1 = Terminal(id=0, loading_time=7, unloading_time=None)
terminal2 = Terminal(id=1, loading_time=None, unloading_time=6)
terminal3 = Terminal(id=2, loading_time=None, unloading_time=10)

# build nodes
nodeA = Node(node_id=0, node_name='Patio A')
nodeB = Node(node_id=1, node_name='Patio B')

nodeA.set_distance_map(nodeB, 800)
nodeA.set_related_nodes([nodeB])
nodeA.set_related_terminals([terminal1])

nodeB.set_distance_map(nodeA, 800)
nodeB.set_related_nodes([nodeA])
nodeB.set_related_terminals([terminal2, terminal3])

terminal1.set_related_nodes([nodeA])
terminal2.set_related_nodes([nodeB])
terminal3.set_related_nodes([nodeB])

demand1 = Demand(terminal1, terminal2, 14000)
terminal2.set_demand(demand1)
demand2 = Demand(terminal1, terminal3, 3000)
terminal3.set_demand(demand2)

terminals = [terminal1, terminal2, terminal3]
nodes = [nodeA, nodeB]

# build trains
train_id = 0
train_load = 1e3 # ton
train_speed_loaded = 40  # km/h
train_speed_empty = 47  # km/h
train1 = Train(train_id=train_id, load=train_load, speed_loaded=train_speed_loaded, speed_empty=train_speed_empty)
train1.set_origin(nodeB)
train1.set_demand_origin(terminal1)

train_id = 1
train_load = 1e3 # ton
train_speed_loaded = 40  # km/h
train_speed_empty = 47  # km/h
train2 = Train(train_id=train_id, load=train_load, speed_loaded=train_speed_loaded, speed_empty=train_speed_empty)
train2.set_origin(nodeB)
train2.set_demand_origin(terminal1)

trains = [train1, train2]

# Simulate
model = Model(nodes, terminals, trains)
simulator = Simulator()
simulator.simulate(model, 15*24)

# Simulation performance
max_loading_time, cycle_time = get_performance_metrics(terminals=terminals)
max_number_of_trains = cycle_time/max_loading_time
queue_time = [0]
Pn = [0]  # numerical productivity (kg/s)
Pa = [0]  # analytical productivity (kg/s)
tq = [0]  # queue time (s)
n = [0]  # number of trains
productivity, production, time = model.evaluate_produtivity()
queue_time.append(model.queue_time())

#log
n.append(len(trains))
Pn.append(productivity[-1])
Pa.append(min(len(trains), max_number_of_trains) * 1e3 / cycle_time)

print('Performance Data:\n')
print(f'\n Numerical productivity {productivity[-1]:.0f}')
print(f'\n Analytical productivity {Pa[-1]:.0f}')
print_demand(terminals)