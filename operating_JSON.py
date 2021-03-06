import json
import pathlib


class MyOperatingJSON:

    def __init__(self):
        self.data = {
            "states": set(),
            "initial_state": '',
            "final_state": set(),
            "transitions": [],
            "symbols": set()
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
        self.data['states'].add(state)

    def remove_state(self, state: str):
        self.data['states'].discard(state)

    def set_initial(self, state: str):
        self.data['initial_state'] = state

    def add_final(self, state: str):
        self.data['final_state'].add(state)

    def remove_final(self, state: str):
        self.data['final_state'].discard(state)

    '''
    retorna todas as transições de um estado
    se ele for o estado fonte (state_from)
    '''
    def get_all_transitions_from_state(self, state: str):
        transitions = []
        for transition in self.get_transitions():
            if transition['state_from'] == state:
                transitions.append(transition)

        return transitions

    '''
    retorna um dicionário com chave sendo a transição e o valor
    o estado destino (state_to) de um estado se ele for o estado fonte (state_from)
    '''
    def get_state_to(self, state: str):
        transitions = dict()
        for transition in self.get_transitions():
            if transition['state_from'] == state:
                transitions[transition['transition_symbol']] = transition['state_to']

        return transitions

    def add_transition(self, state_from: str, state_to: str, transition_symbol: str):
        if {"state_from": state_from, "state_to": state_to, "transition_symbol": transition_symbol} not in self.data['transitions']:
            self.data['transitions'].append({"state_from": state_from,
                                             "state_to": state_to,
                                             "transition_symbol": transition_symbol})

    def add_transition_2(self, transition: dict):
        if transition not in self.data['transitions']:
            self.data['transitions'].append(transition)

    def remove_transition(self, state_from: str, state_to: str, transition_symbol: str):
        for item in self.data['transitions']:
            if item['state_from'] == state_from and item['state_to'] == state_to and item['transition_symbol'] == transition_symbol:
                self.data['transitions'].remove(item)

    def load_to_memory(self, file_name: str):
        path_input = pathlib.Path(pathlib.Path.cwd(), 'test', file_name + '.json')
        if path_input.exists():
            with open(path_input) as f:
                load_data = json.load(f)
                self.data["states"] = set(load_data["states"])
                self.data["initial_state"] = load_data["initial_state"]
                self.data["final_state"] = set(load_data["final_state"])
                self.data["transitions"] = load_data["transitions"]
                self.data["symbols"] = set(load_data["symbols"])

    def save_to_disc(self, file_name: str, data_to_save: dict):
        path_output = pathlib.Path(pathlib.Path.cwd(), 'test', file_name + '.json')
        save_data = {
            "states": sorted(data_to_save["states"]),
            "initial_state": data_to_save["initial_state"],
            "final_state": sorted(data_to_save["final_state"]),
            "transitions": data_to_save["transitions"],
            "symbols": sorted(data_to_save["symbols"])
        }
        with open(path_output, 'w') as json_file:
            json.dump(save_data, json_file, indent=4, sort_keys=True)

