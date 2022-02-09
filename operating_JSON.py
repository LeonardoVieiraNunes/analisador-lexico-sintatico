import json
import pathlib


class MyOperatingJSON:

    def __init__(self):
        self.data = {
            "states": [],
            "initial_state": [],
            "final_state": [],
            "transitions": [],
            "symbols": []
        }

    def get_states(self):
        return self.data['states']

    def get_initial(self):
        return self.data['initial_state']

    def get_final(self):
        return self.data['final_state']

    def get_transitions(self):
        return self.data['transitions']

    def get_symbols(self):
        return self.data['symbols']

    def add_state(self, state: str):
        if state not in self.get_states():
            self.data['states'].append(state)

    def remove_state(self, state: str):
        if self.data['states'].count(state) > 0:
            self.data['states'].remove(state)

    def add_initial(self, state: str):
        self.data['initial_state'].append(state)

    def remove_initial(self, state: str):
        if self.data['initial_state'].count(state) > 0:
            self.data['initial_state'].remove(state)

    def add_final(self, state: str):
        if state not in self.get_final():
            self.data['final_state'].append(state)

    def remove_final(self, state: str):
        if self.data['final_state'].count(state) > 0:
            self.data['final_state'].remove(state)

    def add_transition(self, state_from: str, state_to: str, transition_symbol: str):
        self.data['transitions'].append({"state_from": state_from,
                                         "state_to": state_to,
                                         "transition_symbol": transition_symbol})

    def remove_transition(self, state_from: str, state_to: str, transition_symbol: str):
        for item in self.data['transitions']:
            if item['state_from'] == state_from and item['state_to'] == state_to and item['transition_symbol'] == transition_symbol:
                self.data['transitions'].remove(item)

    def load_to_memory(self, file_name: str):
        path_input = pathlib.Path(pathlib.Path.cwd(), 'test', file_name + '.json')
        if path_input.exists():
            with open(path_input) as f:
                self.data = json.load(f)

    def save_to_disc(self, file_name: str):
        path_output = pathlib.Path(pathlib.Path.cwd(), 'test', file_name + '.json')
        with open(path_output, 'w') as json_file:
            json.dump(self.data, json_file, indent=4, sort_keys=True)

    def get_all_transitions_from_state(self, state: str):
        transitions = []
        for transition in self.get_transitions():
            if transition['state_from'] == state:
                transitions.append(transition)

        return transitions

    def get_non_final_states(self):
        return list(filter(lambda x: x not in self.get_final(), self.get_states()))
