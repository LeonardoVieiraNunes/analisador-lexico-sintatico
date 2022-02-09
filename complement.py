from operating_JSON import MyOperatingJSON

def complement(af1:MyOperatingJSON):
    # Se o automato for nao deterministico, determinizar

    # fazer automato total
    automato_total = make_total(af1)

    # inverter estados finais e nao finais
    estados_nao_finais = af1.get_non_final_states()
    af1.data['final_state'] = estados_nao_finais


def make_total(afd:MyOperatingJSON):
    # para fazer o AFD total, precisa que todos os estados tenham transicoes via
    # todos os simbolos do alfabeto, para isso
    # criamos um estado novo qualquer e adicionamos transicoes a ele via os simbolos faltantes
    estado_novo = "D0"
    afd.add_state(estado_novo)
    for estado in afd.get_states():
        transicoes = afd.get_all_transitions_from_state(estado)
        # filtrar simbolos sem transicao neste estado
        simbolos_presentes = []
        for transicao in transicoes:
            simbolos_presentes.append(transicao['transition_symbol'])

        simbolos_faltantes = list(filter(lambda x: x not in simbolos_presentes, afd.get_symbols()))
        for simbolo in simbolos_faltantes:
            afd.add_transition(estado,estado_novo,simbolo)
