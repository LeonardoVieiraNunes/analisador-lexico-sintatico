from operating_JSON import MyOperatingJSON
from complement import complement
from dead_states import find_dead_states
from unreachable_states import find_unreachable_states
epsilon = '&'

class AutomataUnion_intersection:

    def __init__(self):
        self.base_automata = MyOperatingJSON()
        self.base_automata_2 = MyOperatingJSON()
        self.final_automata = MyOperatingJSON()
        self.epsilon_transitions = {self.base_automata: {},
                                    self.base_automata_2: {},
                                    self.final_automata: {}
                                    }

    def union(self, file1: str, file2: str):
        self.set_automata(file1, self.base_automata)
        self.set_second_automata(file2, self.base_automata_2)
        self.final_automata = union_non_determinized(self.base_automata, self.base_automata_2)
        self.create_epsilon_transitions(self.final_automata)
        self.create_new_automata(self.final_automata)


    def set_automata(self, file_name: str, automata):
        automata.load_to_memory(file_name)
        self.create_epsilon_transitions(automata)
        self.create_new_automata(automata)


    def create_epsilon_transitions(self, automata):
        transitions = automata.get_transitions()
        for state in automata.get_states():
            states_to_check = [state]
            epsilon_fecho_of_current_state = set()
            epsilon_fecho_of_current_state.add(state)
            while len(states_to_check) != 0:
                current_state = states_to_check.pop(0)
                for current_transition in transitions:
                    if current_transition['state_from'] == current_state and current_transition['transition_symbol'] == '&' and current_transition['state_to'] not in epsilon_fecho_of_current_state:
                        epsilon_fecho_of_current_state.add(current_transition['state_to'])
                        states_to_check.append(current_transition['state_to'])
            self.epsilon_transitions[automata][state] = epsilon_fecho_of_current_state

    def create_new_union_automata(self, automata):
        new_states_set_list = [self.epsilon_transitions[automata].__getitem__(automata.get_initial())]
        new_states_to_check_list = [new_states_set_list[0]]
        new_initial_state = ''.join(sorted(new_states_set_list[0]))
        temporary_data = {
            "states": {new_initial_state},
            "initial_state": new_initial_state,
            "final_state": set(),
            "transitions": [],
            "symbols": automata.get_symbols()
        }
        while len(new_states_to_check_list) != 0:
            current_state_set = new_states_to_check_list.pop(0)
            for state in current_state_set:
                if state in self.base_automata.get_final() or state in self.base_automata_2.get_final():
                    temporary_data['final_state'].add(''.join(sorted(current_state_set)))
                    break
            for symbol in automata.get_symbols():
                temp_to_state_set = set()
                for state in current_state_set:
                    for transition in automata.get_transitions():
                        if transition['state_from'] == state and transition['transition_symbol'] == symbol:
                            temp_to_state_set = temp_to_state_set | self.epsilon_transitions[automata][transition['state_to']]
                if len(temp_to_state_set) > 0:
                    temporary_data['transitions'].append({"state_from": ''.join(sorted(current_state_set)),
                                                          "state_to": ''.join(sorted(temp_to_state_set)),
                                                          "transition_symbol": symbol})
                if len(temp_to_state_set) > 0 and temp_to_state_set not in new_states_set_list:
                    new_states_set_list.append(temp_to_state_set)
                    temporary_data['states'].add(''.join(sorted(temp_to_state_set)))
                    new_states_to_check_list.append(temp_to_state_set)
        automata.data = temporary_data

    def create_new_intersection_automata(self, automata):
        new_states_set_list = [self.epsilon_transitions[automata].__getitem__(automata.get_initial())]
        new_states_to_check_list = [new_states_set_list[0]]
        new_initial_state = ''.join(sorted(new_states_set_list[0]))
        temporary_data = {
            "states": {new_initial_state},
            "initial_state": new_initial_state,
            "final_state": set(),
            "transitions": [],
            "symbols": automata.get_symbols()
        }
        while len(new_states_to_check_list) != 0:
            current_state_set = new_states_to_check_list.pop(0)
            for state in current_state_set:
                if state in self.base_automata.get_final() and state in self.base_automata_2.get_final():
                    temporary_data['final_state'].add(''.join(sorted(current_state_set)))
                    break
            for symbol in automata.get_symbols():
                temp_to_state_set = set()
                for state in current_state_set:
                    for transition in automata.get_transitions():
                        if transition['state_from'] == state and transition['transition_symbol'] == symbol:
                            temp_to_state_set = temp_to_state_set | self.epsilon_transitions[automata][transition['state_to']]
                if len(temp_to_state_set) > 0:
                    temporary_data['transitions'].append({"state_from": ''.join(sorted(current_state_set)),
                                                          "state_to": ''.join(sorted(temp_to_state_set)),
                                                          "transition_symbol": symbol})
                if len(temp_to_state_set) > 0 and temp_to_state_set not in new_states_set_list:
                    new_states_set_list.append(temp_to_state_set)
                    temporary_data['states'].add(''.join(sorted(temp_to_state_set)))
                    new_states_to_check_list.append(temp_to_state_set)
        automata.data = temporary_data

    def create_new_automata(self, automata):
        new_states_set_list = [self.epsilon_transitions[automata].__getitem__(automata.get_initial())]
        new_states_to_check_list = [new_states_set_list[0]]
        new_initial_state = ''.join(sorted(new_states_set_list[0]))
        temporary_data = {
            "states": {new_initial_state},
            "initial_state": new_initial_state,
            "final_state": set(),
            "transitions": [],
            "symbols": automata.get_symbols()
        }
        while len(new_states_to_check_list) != 0:
            current_state_set = new_states_to_check_list.pop(0)
            for state in current_state_set:
                if state in automata.get_final():
                    temporary_data['final_state'].add(''.join(sorted(current_state_set)))
                    break
            for symbol in automata.get_symbols():
                temp_to_state_set = set()
                for state in current_state_set:
                    for transition in automata.get_transitions():
                        if transition['state_from'] == state and transition['transition_symbol'] == symbol:
                            temp_to_state_set = temp_to_state_set | self.epsilon_transitions[automata][transition['state_to']]
                if len(temp_to_state_set) > 0:
                    temporary_data['transitions'].append({"state_from": ''.join(sorted(current_state_set)),
                                                          "state_to": ''.join(sorted(temp_to_state_set)),
                                                          "transition_symbol": symbol})
                if len(temp_to_state_set) > 0 and temp_to_state_set not in new_states_set_list:
                    new_states_set_list.append(temp_to_state_set)
                    temporary_data['states'].add(''.join(sorted(temp_to_state_set)))
                    new_states_to_check_list.append(temp_to_state_set)
        automata.data = temporary_data


def union_non_determinized(afd1: MyOperatingJSON, afd2:MyOperatingJSON):
    new_AFND = MyOperatingJSON()
    # Novos estados
    for state in afd1.get_states():
        new_state = f'{state}'
        new_AFND.add_state(new_state)

    for state in afd2.get_states():
        new_state = f'{state}'
        new_AFND.add_state(new_state)

    # Estado inicial
    # Pela definicao da uniao de AF se cria um estado inicial novo que
    # vai para os estados iniciais dos outros automatos por epsilon
    init_state = 'init'
    new_AFND.add_state(init_state)
    new_AFND.add_initial(init_state)

    init_state_af1 = f'{afd1.get_initial()[0]}'
    init_state_af2 = f'{afd2.get_initial()[0]}'

    new_AFND.add_transition(init_state, init_state_af1, epsilon)
    new_AFND.add_transition(init_state, init_state_af2, epsilon)

    for transition in afd1.get_transitions():
        origin = f'{transition["state_from"]}'
        destination = f'{transition["state_to"]}'
        symbol = f'{transition["transition_symbol"]}'
        new_AFND.add_transition(origin, destination, symbol)

    for transition in afd2.get_transitions():
        origin = f'{transition["state_from"]}'
        destination = f'{transition["state_to"]}'
        symbol = f'{transition["transition_symbol"]}'
        new_AFND.add_transition(origin, destination, symbol)

    symbols = []

    for symbol in afd1.get_symbols():
        if symbol not in symbols:
            symbols.append(symbol)


    for symbol in afd2.get_symbols():
        if symbol not in symbols:
            symbols.append(symbol)

    new_AFND.data['symbols'] = symbols

    for final_state in afd1.get_final():
        new_state = f"{final_state}"
        new_AFND.add_final(new_state)

    for final_state in afd2.get_final():
        new_state = f"{final_state}"
        new_AFND.add_final(new_state)

    return new_AFND

def intersection(afd1: MyOperatingJSON, afd2:MyOperatingJSON):
    # construir complementos de afds
    comp1 = complement(afd1)
    comp2 = complement(afd2)
    # fazer uniao dos complementos
    uniao = union(comp1, comp2)
    # remover estados mortos

    # remover estados incalcancaveis

    # minimizar automato
    automato_minimizado = uniao

    # realizar complemento do resultado
    return complement(automato_minimizado)

if __name__ == "__main__":
    afd1 = MyOperatingJSON()
    afd1.load_to_memory('language_01')

    afd2 = MyOperatingJSON()
    afd2.load_to_memory('language_02')

    union = union(afd1,afd2)
    union.save_to_disc('union')