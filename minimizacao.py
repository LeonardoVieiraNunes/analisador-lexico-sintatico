from operating_JSON import MyOperatingJSON
from itertools import chain


class Minimizacao():
    def __init__(self, automato: MyOperatingJSON):
        super(Minimizacao, self).__init__()
        self.tabelaEstados = dict()
        self.inicial = automato.get_initial()[0]
        self.estados = automato.get_states()
        self.simbolos = automato.get_symbols()
        self.finais = automato.get_final()
        self.repetirMarcacao = False
        self.estadosOtimizados = []
        self.estadosCombinados = []
        self.automato = automato
        self.novoAutomato = MyOperatingJSON()

    def construirTabelaEstados(self):
        nroTemp = 1
        for i in self.estados[1:]:
            self.tabelaEstados[i] = [None] * nroTemp
            nroTemp += 1

    def marcarEstados(self):
        for estado in self.tabelaEstados.keys():
            for i in range(len(self.tabelaEstados[estado])):
                if (estado in self.finais and self.estados[i] not in self.finais) or (
                        estado not in self.finais and self.estados[i] in self.finais):
                    self.tabelaEstados[estado][i] = 1

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

    def setEstadosNovoAutomato(self):
        for estadoOtimizado in self.estadosOtimizados:
            self.novoAutomato.add_state('_'.join(sorted(estadoOtimizado)))

    def preencherNaoCombinados(self):
        for estado in self.estados:
            if not list(filter(lambda c: estado in c, self.estadosOtimizados)):
                self.estadosOtimizados.append({estado})

    def gerarNaoMarcados(self):
        for estado in self.tabelaEstados.keys():
            for i in range(len(self.tabelaEstados[estado])):
                if self.tabelaEstados[estado][i] is None:
                    self.estadosCombinados.append(set(estado + self.estados[i]))

        self.combinarNaoMarcados(self.estadosCombinados[0], self.estadosCombinados[1:])

    def setTransicoesNovoAutomato(self):
        for otimizados in self.estadosOtimizados:
            transitions = self.automato.get_state_to(next(iter(otimizados)))
            for symbol in self.simbolos:
                stateTo = next(filter(lambda e: transitions[symbol] in e, self.estadosOtimizados))
                self.novoAutomato.add_transition('_'.join(sorted(otimizados)), '_'.join(sorted(stateTo)), symbol)

    def setEstadosFinaisNovoAutomato(self):
        for estado in self.estadosOtimizados:
            if estado.intersection(self.finais):
                self.novoAutomato.add_final('_'.join(sorted(estado)))

    def setEstadoInicialNovoAutomato(self):
        for estado in self.estadosOtimizados:
            if self.inicial in estado:
                self.novoAutomato.add_initial('_'.join(sorted(estado)))
                break

    def setSimbolosNovoAutomato(self):
        self.novoAutomato.data['symbols'] = self.simbolos

    def salvarNovoAutomato(self):
        self.novoAutomato.save_to_disc('minimizacao-t1')

if __name__ == "__main__":
    afd = MyOperatingJSON()
    afd.load_to_memory('language_04')
    minimizado = Minimizacao(afd)
    minimizado.construirTabelaEstados()
    minimizado.marcarEstados()
    minimizado.verificarNaoMarcados()
    minimizado.gerarNaoMarcados()
    minimizado.preencherNaoCombinados()
    minimizado.setEstadosNovoAutomato()
    minimizado.setTransicoesNovoAutomato()
    minimizado.setEstadoInicialNovoAutomato()
    minimizado.setEstadosFinaisNovoAutomato()
    minimizado.setSimbolosNovoAutomato()
    minimizado.salvarNovoAutomato()
    print(1)
