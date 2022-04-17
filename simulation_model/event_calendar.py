import math

class event_calendar:
    ''' Class for handling en event calendar
    '''
    def __init__(self):
        ''' Constructs an event calendar
        '''
        self.calendar = []

    def push(self, time, callback, data):
        ''' Add events to calendar
        Args: 
            time (float): fire time
            callback (function): callback function
            data: custom callback data
        '''

        # Busca binária
        i = [0, len(self.calendar)] # insertion calendar index
        while i[0] != i[1]:
            medium_index = math.floor((i[0] + i[1])/2)
            if time >= self.calendar[medium_index][0]:
                i[0] = medium_index + 1
            else:
                i[1] = medium_index
        self.calendar.insert(i[0], (time, callback, data))

    def pop(self):
        ''' Get the nearest time event
        Returns:
            (float): fire time
            (function): callback function
            (object) callback data
        '''
        return self.calendar.pop(0)

    def is_empty(self):
        ''' Check whether calendar is empty
        Returns:
            (bool): true if calendar is empty
        '''
        return len(self.calendar) == 0