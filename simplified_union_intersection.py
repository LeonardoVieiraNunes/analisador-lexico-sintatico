from operating_JSON import MyOperatingJSON
from determinizacao import MyDeterminationOfInput
epsilon = '&'


class MyUnionIntersection:

    def __init__(self):
        self.final_automata = MyOperatingJSON()

    def set_final_automata(self, afd1: MyOperatingJSON, afd2: MyOperatingJSON):
        # Novos estados
        self.final_automata.data['states'] = afd1.data['states'] | afd2.data['states']

        # Estado inicial
        # Pela definicao da uniao de AF se cria um estado inicial novo que
        # vai para os estados iniciais dos outros automatos por epsilon
        init_state = 'init'
        self.final_automata.add_state(init_state)
        self.final_automata.set_initial(init_state)

        self.final_automata.add_transition(init_state, afd1.get_initial(), epsilon)
        self.final_automata.add_transition(init_state, afd2.get_initial(), epsilon)

        # Adicionar transições
        for transition in afd1.get_transitions():
            self.final_automata.add_transition_2(transition)
        for transition in afd1.get_transitions():
            self.final_automata.add_transition_2(transition)

        # Adicionar simbolos
        self.final_automata.data['symbols'] = afd1.data['symbols'] | afd2.data['symbols']

    def make_union(self, afd1: MyOperatingJSON, afd2: MyOperatingJSON):
        self.set_final_automata(afd1, afd2)
        union_automata = MyDeterminationOfInput()
        return union_automata.union(self.final_automata, afd1, afd2)

    def make_intersection(self, afd1: MyOperatingJSON, afd2: MyOperatingJSON):
        self.set_final_automata(afd1, afd2)
        intersection_automata = MyDeterminationOfInput()
        return intersection_automata.intersection(self.final_automata, afd1, afd2)
