import itertools

from operating_JSON import MyOperatingJSON

TRANSITIONS = 'transitions'

def estadoByCombinacaoEstados(combinacoes_estados, combinacao):
    combinacao_encontrada = ""
    for comb in combinacoes_estados:
        if combinacao == set(comb):
            combinacao_encontrada = "_".join(str(estado) for estado in comb)
            break
    return combinacao_encontrada

def atravessarMultiplosEstados(automato: MyOperatingJSON, estados, simbolo):
    estados_finais = []
    for estado in estados:
        lista = list(filter(lambda t: t['state_from'] == estado and t['transition_symbol'] == simbolo, automato.get_transitions()))
        if len(lista) > 0:
            # estados_finais.append(simbolo)
            estados_finais += list(map(lambda i: i['state_to'], lista))
    return estados_finais




def atravessarEpsilon(automato: MyOperatingJSON, estado: str, simbolo):
    estados_anteriores = []
    while True:
        estados = set(estado).union(set(atravessarMultiplosEstados(automato, estado, simbolo)))
        if estados == estados_anteriores:
            break
        estados_anteriores = estados
    return estados


def atravessarEpsilonNfa(automato, estados, simbolo):
    estados = atravessarEpsilon(automato, estados, 'e')
    estados = atravessarMultiplosEstados(automato, estados, simbolo)
    estados = atravessarEpsilon(automato, estados, 'e')
    return estados


def nfaToDfa(automato: MyOperatingJSON):
    # criar combinações de estados
    novo_automato = MyOperatingJSON()

    estados_automato = automato.get_states()
    combinacoes_estados = []
    estados_novo_automato = []

    for i in range(1, len(estados_automato) + 1):
        combinations = set(itertools.combinations(estados_automato, i))
        for comb in combinations:
            combinacoes_estados.append(comb)

    for estados_automato in combinacoes_estados:
        estados_novo_automato.append("_".join(str(state) for state in estados_automato))

    for estado in estados_novo_automato:
        novo_automato.add_state(estado)

    # estados aceitação
    finais_automato = automato.get_final()
    finais_novo_automato = []

    for estados in combinacoes_estados:
        for final in finais_automato:
            if final in estados_automato:
                finais_novo_automato.append("_".join(str(estado) for estado in estados))

    finais_novo_automato = set(finais_novo_automato)

    for final_novo_automato in finais_novo_automato:
        novo_automato.add_final(final_novo_automato)

    # estado inicial
    inicial_automato = automato.get_initial()
    inicial_novo_automato = estadoByCombinacaoEstados(combinacoes_estados,
                                                      atravessarEpsilon(automato, inicial_automato, 'e'))
    novo_automato.add_initial(inicial_novo_automato)
    # transicoes
    simbolos_automato = automato.get_symbols()
    for simbolo in simbolos_automato:
        for estados in combinacoes_estados:
            novo_estado = '_'.join(str(estado) for estado in estados)
            novo_estado_resultados = atravessarEpsilonNfa(automato, estados, simbolo)
            novo_estado_resultado = estadoByCombinacaoEstados(combinacoes_estados, novo_estado_resultados)
            if novo_estado_resultado == '':
                novo_estado_resultado = '_'
            novo_automato.add_transition(novo_estado, novo_estado_resultado, simbolo)
    return novo_automato.save_to_disc("01")



if __name__ == "__main__":
    automato = MyOperatingJSON()
    automato.load_to_memory("language_03")

    print(nfaToDfa(automato))
