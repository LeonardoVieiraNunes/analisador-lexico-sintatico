from operating_JSON import MyOperatingJSON
from complement import complement
from dead_states import find_dead_states
from unreachable_states import find_unreachable_states
epsilon = '&'


def union(afd1: MyOperatingJSON, afd2:MyOperatingJSON):
    new_AFND = MyOperatingJSON()
    # Novos estados
    for state in afd1.get_states():
        new_state = f'{state}_1'
        new_AFND.add_state(new_state)

    for state in afd2.get_states():
        new_state = f'{state}_2'
        new_AFND.add_state(new_state)

    # Estado inicial
    # Pela definicao da uniao de AF se cria um estado inicial novo que
    # vai para os estados iniciais dos outros automatos por epsilon
    init_state = 'q0'
    new_AFND.add_state(init_state)
    new_AFND.add_initial(init_state)

    init_state_af1 = f'{afd1.get_initial()[0]}_1'
    init_state_af2 = f'{afd2.get_initial()[0]}_2'

    new_AFND.add_transition(init_state, init_state_af1, epsilon)
    new_AFND.add_transition(init_state, init_state_af2, epsilon)

    for transition in afd1.get_transitions():
        origin = f'{transition["state_from"]}_1'
        destination = f'{transition["state_to"]}_1'
        symbol = f'{transition["transition_symbol"]}_1'
        new_AFND.add_transition(origin, destination, symbol)

    for transition in afd2.get_transitions():
        origin = f'{transition["state_from"]}_2'
        destination = f'{transition["state_to"]}_2'
        symbol = f'{transition["transition_symbol"]}_2'
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
        new_state = f"{final_state}_1"
        new_AFND.add_final(new_state)

    for final_state in afd2.get_final():
        new_state = f"{final_state}_2"
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