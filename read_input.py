from operating_JSON import MyOperatingJSON
from determinizacao import MyDeterminationOfInput


def next_state(transitions: dict, current_state: str, symbol: str):
    if current_state == "invalid_transition":
        return current_state
    for transition in transitions:
        if current_state == transition['state_from'] and symbol == transition['transition_symbol']:
            return transition['state_to']
    return "invalid_transition"


class MyCheckOfInput:

    def __init__(self, final_automata=MyOperatingJSON()):
        automata_d = MyDeterminationOfInput()
        automata_d.determination_of_single_automata(final_automata)
        temp_automata = MyOperatingJSON()
        temp_automata.data = automata_d.new_automata.data
        self.test_automata = temp_automata

    def test_input(self, test_input: str):
        current_state = self.test_automata.get_initial()
        transitions = self.test_automata.get_transitions()
        for symbol in test_input:
            current_state = next_state(transitions, current_state, symbol)

        for approval_state in self.test_automata.get_final():
            if current_state == approval_state:
                print("Automato reconheçe o input")
                return
        print("Automato não reconheçe o input")
