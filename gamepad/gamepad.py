import re

from inputs import get_gamepad
from uuid import uuid4


class ControllerInput():
    '''
    A base class to generically represent a controller input

    event_codes: a list of type event.code from the inputs module that
      represent this controller input

    name: a name unique on this controller
    '''
    def __init__(self, event_codes, name=uuid4()):
        self.event_codes = event_codes
        self.name = name
        self.callbacks = []

    def __str__(self):
        return f'<ControllerInput {self.event_codes} {self.name}'


class Thumbstick(ControllerInput):
    '''
    A thumbstick
    '''

    def set_deadzone(self, x_min, x_max, y_min, y_max):
        # TODO
        pass
    

class DPad(ControllerInput):
    '''
    A dpad
    '''
    pass


class Button(ControllerInput):
    '''
    A button
    '''
    pass


class Trigger(ControllerInput):
    '''
    A trigger
    '''
    # TODO
    def set_deadzone(self, min, max):
        pass


class Controller():
    def __init__(self, controller_inputs, name=uuid4()):
        '''
        A generic controller

        inputs: a list of type ControllerInput
        '''

        self.controller_inputs = {
            x.name: x for x in controller_inputs
        }
        self.name = name

        self._ec_names_map = {}
        for c_i in controller_inputs:
            for e_c in c_i.event_codes:
                self._ec_names_map[e_c] = c_i.name
                
    def _get_event_codes(self, input_names=None):
        '''
        Get event codes as a list from one or more names

        input_names: a list of names - if not specified, get all codes
        '''

        event_codes = []
        if not input_names:
            for c_i in self.controller_inputs.keys():
                event_codes = event_codes + \
                    self.controller_inputs[c_i].event_codes
        else:
            for name in input_names:
                event_codes += self.controller_inputs[name].event_codes
        
        return event_codes
    
    def get_input_names(self):
        '''
        Get the input names available on this Controller
        '''
        return sorted(self.controller_inputs.keys())
    
    def add_callback(self, input_name, func):
        '''
        Adds a callback to an an ControllerInput

        input_name: a name that represents a ControllerInput
        func: the callback to execute when an event from the ControllerInput
          is received

        NOTE: when func gets called it will receive the value of the input and,
          optionally, the axis if the input is directional

          EXAMPLE1: func(value, axis) for directional inputs
          EXAMPLE2: func(value) for non-directional inputs
        '''
        self.controller_inputs[input_name].callbacks.append(func)
    
    def start(self):
        '''
        Start monitoring for events - dispatch configured callbacks
        '''

        # TODO: identify a better way to do this - needs to be part of the
        # ControllerInput object (or derrivatives)
        r_obj = re.compile('^[A-Z0-9]+_[A-Z0-9]*(?P<axis>[XY])$')

        while True:
            events = get_gamepad()
            for event in events:
                if event.code not in self._ec_names_map:
                    continue
                name = self._ec_names_map[event.code]
                if not self.controller_inputs[name].callbacks:
                    continue
                for callback in self.controller_inputs[name].callbacks:
                    match = r_obj.match(event.code)
                    if not match:
                        callback(event.state)
                    else:
                        callback(event.state, match["axis"])
    
    def debug(self, filter=None):
        '''
        Debug inputs module events

        filter: list of ControllerInput names - the events displayed will only
          include those listed
        '''

        while True:
            events = get_gamepad()
            for event in events:
                if (filter and (event.code in self._get_event_codes(filter))) \
                    or (not filter):

                    print(event.ev_type, event.code, event.state)

    def __str__(self):
        string = f'Name: {self.name}\n'
        for c_i in self.controller_inputs.values():
            string += f'{c_i} \n'
        return string.strip()


def get_LogitechR710():
    '''
    Return a LogitechR710 Controller object
    '''
    return Controller([
        Thumbstick(['ABS_Y', 'ABS_X'], name='LEFT_THUMB'),
        Thumbstick(['ABS_RY', 'ABS_RX'], name='RIGHT_THUMB'),
        DPad(['ABS_HAT0X', 'ABS_HAT0Y'], name='DPAD'),
        Button(['BTN_MODE'], name='MODE'),
        Button(['BTN_SELECT'], name='SELECT'),
        Button(['BTN_START'], name='START'),
        Button(['BTN_NORTH'], name='X'),
        Button(['BTN_WEST'], name='Y'),
        Button(['BTN_EAST'], name='B'),
        Button(['BTN_SOUTH'], name='A'),
        Button(['BTN_TL'], name='LEFT_SHOULDER'),
        Button(['BTN_TR'], name='RIGHT_SHOULDER'),
        Trigger(['ABS_Z'], name='LEFT_TRIGGER'),
        Trigger(['ABS_RZ'], name='RIGHT_TRIGGER')
    ], name='LogitechR710')


if __name__ == "__main__":
    c = get_LogitechR710()
    c.debug()
