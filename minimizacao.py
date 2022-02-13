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

    def minimizar(self):
        nroTemp = 1
        for i in self.estados[1:]:
            self.tabelaEstados[i] = [None] * nroTemp
            nroTemp += 1

        self.marcarEstados()

    def marcarEstados(self):
        for estado in self.tabelaEstados.keys():
            for i in range(len(self.tabelaEstados[estado])):
                if (estado in self.finais and self.estados[i] not in self.finais) or (
                        estado not in self.finais and self.estados[i] in self.finais):
                    self.tabelaEstados[estado][i] = 1

        self.verificarNaoMarcados()

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

    def setEstadosNovoAutomato(self):
        for estadoOtimizado in self.estadosOtimizados:
            self.new_automata.add_state('_'.join(sorted(estadoOtimizado)))

        self.setTransicoesNovoAutomato()

    def preencherNaoCombinados(self):
        for estado in self.estados:
            if not list(filter(lambda c: estado in c, self.estadosOtimizados)):
                self.estadosOtimizados.append({estado})

        self.setEstadosNovoAutomato()

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

    def setTransicoesNovoAutomato(self):
        for otimizados in self.estadosOtimizados:
            transitions = dict()
            for estado in otimizados:
                transitions.update(self.automato.get_state_to(estado))
            for symbol in transitions.keys():
                stateTo = next(filter(lambda e: transitions[symbol] in e, self.estadosOtimizados))
                self.new_automata.add_transition('_'.join(sorted(otimizados)), '_'.join(sorted(stateTo)), symbol)

        self.setEstadoInicialNovoAutomato()

    def setEstadosFinaisNovoAutomato(self):
        for estado in self.estadosOtimizados:
            if estado.intersection(self.finais):
                self.new_automata.add_final('_'.join(sorted(estado)))

        self.setSimbolosNovoAutomato()

    def setEstadoInicialNovoAutomato(self):
        for estado in self.estadosOtimizados:
            if self.inicial in estado:
                self.new_automata.set_initial('_'.join(sorted(estado)))
                break

        self.setEstadosFinaisNovoAutomato()

    def setSimbolosNovoAutomato(self):
        self.new_automata.data['symbols'] = self.simbolos
