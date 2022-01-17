from operating_JSON import MyOperatingJSON
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
