from operating_JSON import MyOperatingJSON


class Minimizacao(MyOperatingJSON):
    def __init__(self, automato=MyOperatingJSON()):
        super(Minimizacao, self).__init__()
        self.tabelaEstados = dict()
        self.inicial = automato.get_initial()
        self.estados = list(automato.get_states())
        self.simbolos = list(automato.get_symbols())
        self.finais = list(automato.get_final())
        self.repetirMarcacao = False
        self.estadosOtimizados = []
        self.estadosCombinados = []
        self.automato = automato
        self.new_automata = MyOperatingJSON()

    '''
    Inicializa a operacao de minimizar criando uma tabela com a combinação
    de todos os pares de estados.
    '''
    def minimizar(self):
        nroTemp = 1
        for i in self.estados[1:]:
            self.tabelaEstados[i] = [None] * nroTemp
            nroTemp += 1

        self.marcarEstados()

    '''
    Marca todos os pares (P,Q) de tabelaEstados onde P pertecence ao conjunto
    de estados finais e Q não.
    '''
    def marcarEstados(self):
        for estado in self.tabelaEstados.keys():
            for i in range(len(self.tabelaEstados[estado])):
                if (estado in self.finais and self.estados[i] not in self.finais) or (
                        estado not in self.finais and self.estados[i] in self.finais):
                    self.tabelaEstados[estado][i] = 1

        self.verificarNaoMarcados()

    '''
    Verifica se existirem pares (P,Q) sem marcação onde P e Q através de uma transição
    de símbolo x estiver marcada, então o par (P, Q) é marcado (fazer isso até
    não ser mais possível realizar marcações)
    '''
    def verificarNaoMarcados(self):
        while True:
            self.repetirMarcacao = False
            for estado in self.tabelaEstados.keys():
                for i in range(len(self.tabelaEstados[estado])):
                    if self.tabelaEstados[estado][i] is None:
                        self.verificarTransicoes(estado, self.estados[i])
            if not self.repetirMarcacao:
                break

        self.gerarNaoMarcados()

    '''
    Gera todos os pares que não foram marcados na tabela. Caso não seja possível,
    retorna retorna o automato do input e avisa que o automato já está minimizado.
    Se for possível, chama a função combinarNaoMarcados a lista de estados combinados
    '''
    def gerarNaoMarcados(self):
        for estado in self.tabelaEstados.keys():
            for i in range(len(self.tabelaEstados[estado])):
                if self.tabelaEstados[estado][i] is None:
                    self.estadosCombinados.append({estado, self.estados[i]})

        if self.estadosCombinados:
            if len(self.estadosCombinados) > 1:
                self.combinarNaoMarcados(self.estadosCombinados[0], self.estadosCombinados[1:])
            else:
                self.combinarNaoMarcados(self.estadosCombinados[0], [])
        else:
            print("O automato já está minimizado")
            self.new_automata = self.automato

    '''
    Realiza a otimização dos estados combinados
    '''
    def combinarNaoMarcados(self, head, tail):
        originalHead = head
        for item in tail:
            if head.intersection(item):
                head = head.union(item)
                tail.remove(item)
        if originalHead == head:
            self.estadosOtimizados.append(head)
        else:
            tail.insert(0, head)
        if len(tail) >= 2:
            self.combinarNaoMarcados(tail[0], tail[1:])
        else:
            self.estadosOtimizados += tail

        self.preencherNaoCombinados()

    '''
    Preenche na lista de estados otimizados aqueles que não puderam ser encapsulados
    por um outro estado.
    '''
    def preencherNaoCombinados(self):
        for estado in self.estados:
            if not list(filter(lambda c: estado in c, self.estadosOtimizados)):
                self.estadosOtimizados.append({estado})

        self.setEstadosNovoAutomato()

    '''
    Adiciona os estados otimizados ao novo automato
    '''
    def setEstadosNovoAutomato(self):
        for estadoOtimizado in self.estadosOtimizados:
            self.new_automata.add_state('_'.join(sorted(estadoOtimizado)))

        self.setTransicoesNovoAutomato()

    '''
    Adiciona as transições ao novo automato de forma a manter a consistência
    com as transições do automato original.
    '''
    def setTransicoesNovoAutomato(self):
        for otimizados in self.estadosOtimizados:
            transitions = dict()
            for estado in otimizados:
                transitions.update(self.automato.get_state_to(estado))
            for symbol in transitions.keys():
                stateTo = next(filter(lambda e: transitions[symbol] in e, self.estadosOtimizados))
                self.new_automata.add_transition('_'.join(sorted(otimizados)), '_'.join(sorted(stateTo)), symbol)

        self.setEstadoInicialNovoAutomato()

    '''
    Adiciona as o estado inicial ao novo automato com base no estado inicial
    do automato original.
    '''
    def setEstadoInicialNovoAutomato(self):
        for estado in self.estadosOtimizados:
            if self.inicial in estado:
                self.new_automata.set_initial('_'.join(sorted(estado)))
                break

        self.setEstadosFinaisNovoAutomato()

    '''
    Adiciona os estados finais ao novo automato com base nos estados finais
    do automato original.
    '''
    def setEstadosFinaisNovoAutomato(self):
        for estado in self.estadosOtimizados:
            if estado.intersection(self.finais):
                self.new_automata.add_final('_'.join(sorted(estado)))

        self.setSimbolosNovoAutomato()

    '''
    Copia os simbolos do automato original ao novo automato
    '''
    def setSimbolosNovoAutomato(self):
        self.new_automata.data['symbols'] = self.simbolos

    '''
    Função auxiliar para verificar se o par (P,Q) da tabela de estados
    está marcado
    '''
    def isMarcado(self, stateToP, stateToQ):
        if stateToP in self.tabelaEstados:
            try:
                return self.tabelaEstados[stateToP][self.estados.index(stateToQ)] is not None
            except IndexError:
                return False
        if stateToQ in self.tabelaEstados:
            try:
                return self.tabelaEstados[stateToQ][self.estados.index(stateToP)] is not None
            except IndexError:
                return False
        return False

    '''
    Função auxiliar para verificar se o estado C vindo do estado P,Q
    por alguma transição x está marcado na tabela de estados.
    '''
    def verificarTransicoes(self, estadoP, estadoQ):
        statesToP = self.automato.get_state_to(estadoP)
        statesToQ = self.automato.get_state_to(estadoQ)
        for simbolo in self.simbolos:
            if simbolo in statesToP and simbolo in statesToQ:
                stateToP = statesToP[simbolo]
                stateToQ = statesToQ[simbolo]
                if self.isMarcado(stateToP, stateToQ):
                    self.tabelaEstados[estadoP][self.estados.index(estadoQ)] = 1
                    self.repetirMarcacao = True

