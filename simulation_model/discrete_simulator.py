import event_calendar as ec


class Simulator:
    ''' Discrete event system simulator.
    '''

    def __init__(self):
        ''' Construct an event system simulator.
        '''

        # setup
        self.time = 0
        self.day = 0
        self.calendar = ec.event_calendar()

    def add_event(self, t, f, data):
        ''' Add event to calendar.

        Args:
            t (float): fire time.
            f (function): callback function.
            data: custom callback data.
        '''
        self.calendar.push(t, f, data)

    def simulate(self, model, t=24 * 3600):
        ''' Simulate discret event system.

        Args:
            model (:obj:model): discrete event system model.
            t (float): time horizon.
        '''

        # discrete event simulator
        print('\n######## Beginnig simulation\n')
        model.clear()
        model.starting_events(self)
        while (not self.calendar.is_empty()) and (self.time <= t):
            self.time, f, data = self.calendar.pop()  # get next event
            f(self, data)  # callback function
        print('\n######## End of simulation\n')
