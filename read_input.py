import operating_JSON


def next_state(transitions: dict, current_state: str, symbol: str):
    if current_state == "invalid_transition":
        return current_state
    for transition in transitions:
        if current_state == transition['state_from'] and symbol == transition['transition_symbol']:
            return transition['state_to']


class MyCheckOfInput:

    def __init__(self):
        self.test_automata = operating_JSON.MyOperatingJSON()

    def set_dfa(self, file_name: str):
        self.test_automata.load_to_memory(file_name)

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
