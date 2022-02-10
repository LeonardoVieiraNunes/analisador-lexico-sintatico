from operating_JSON import MyOperatingJSON


class MyDeterminationOfInput:

    def __init__(self):
        self.base_automata = MyOperatingJSON()
        self.temp_automata_1 = MyOperatingJSON()
        self.temp_automata_2 = MyOperatingJSON()
        self.epsilon_transitions = {}

    def union(self, final_automata: MyOperatingJSON, afd1: MyOperatingJSON, afd2: MyOperatingJSON):
        self.base_automata = final_automata
        self.temp_automata_1 = afd1
        self.temp_automata_2 = afd2
        self.create_epsilon_transitions()
        self.create_new_automata('union')

    def intersection(self, final_automata: MyOperatingJSON, afd1: MyOperatingJSON, afd2: MyOperatingJSON):
        self.base_automata = final_automata
        self.temp_automata_1 = afd1
        self.temp_automata_2 = afd2
        self.create_epsilon_transitions()
        self.create_new_automata('intersection')

    def determination_of_single_automata(self, file_name: str):
        self.base_automata.load_to_memory(file_name)
        self.create_epsilon_transitions()
        self.create_new_automata('simple')

    def create_epsilon_transitions(self):
        transitions = self.base_automata.get_transitions()
        for state in self.base_automata.get_states():
            states_to_check = [state]
            epsilon_fecho_of_current_state = set()
            epsilon_fecho_of_current_state.add(state)
            while len(states_to_check) != 0:
                current_state = states_to_check.pop(0)
                for current_transition in transitions:
                    if current_transition['state_from'] == current_state and current_transition['transition_symbol'] == '&' and current_transition['state_to'] not in epsilon_fecho_of_current_state:
                        epsilon_fecho_of_current_state.add(current_transition['state_to'])
                        states_to_check.append(current_transition['state_to'])
            self.epsilon_transitions[state] = epsilon_fecho_of_current_state

    def create_new_automata(self, operation: str):
        new_states_set_list = [self.epsilon_transitions.__getitem__(self.base_automata.get_initial())]
        new_states_to_check_list = [new_states_set_list[0]]
        new_initial_state = ''.join(sorted(new_states_set_list[0]))
        temporary_data = {
            "states": {new_initial_state},
            "initial_state": new_initial_state,
            "final_state": set(),
            "transitions": [],
            "symbols": self.base_automata.get_symbols()
        }
        while len(new_states_to_check_list) != 0:
            current_state_set = new_states_to_check_list.pop(0)
            if operation == 'simple':
                for state in current_state_set:
                    if state in self.base_automata.get_final():
                        temporary_data['final_state'].add(''.join(sorted(current_state_set)))
                        break
            if operation == 'union':
                for state in current_state_set:
                    if (state in self.temp_automata_1.get_final()) or (state in self.temp_automata_2.get_final()):
                        temporary_data['final_state'].add(''.join(sorted(current_state_set)))
                        break
            if operation == 'intersection':
                for state in current_state_set:
                    if (state in self.temp_automata_1.get_final()) and (state in self.temp_automata_2.get_final()):
                        temporary_data['final_state'].add(''.join(sorted(current_state_set)))
                        break
            for symbol in self.base_automata.get_symbols():
                temp_to_state_set = set()
                for state in current_state_set:
                    for transition in self.base_automata.get_transitions():
                        if transition['state_from'] == state and transition['transition_symbol'] == symbol:
                            temp_to_state_set = temp_to_state_set | self.epsilon_transitions[transition['state_to']]
                if len(temp_to_state_set) > 0:
                    temporary_data['transitions'].append({"state_from": ''.join(sorted(current_state_set)),
                                                          "state_to": ''.join(sorted(temp_to_state_set)),
                                                          "transition_symbol": symbol})
                if len(temp_to_state_set) > 0 and temp_to_state_set not in new_states_set_list:
                    new_states_set_list.append(temp_to_state_set)
                    temporary_data['states'].add(''.join(sorted(temp_to_state_set)))
                    new_states_to_check_list.append(temp_to_state_set)
        self.base_automata.data = temporary_data
