from operating_JSON import MyOperatingJSON
from itertools import chain


class Minimizacao(MyOperatingJSON):
    def __init__(self, automato: MyOperatingJSON):
        super(Minimizacao, self).__init__()
        self.tabelaEstados = dict()
        self.estados = automato.get_states()
        self.simbolos = automato.get_symbols()
        self.finais = automato.get_final()
        self.repetirMarcacao = False
        self.estadosCombinados = []
        self.data = automato.data

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
        statesToP = self.get_state_to(estadoP)
        statesToQ = self.get_state_to(estadoQ)
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

    def combinarNaoMarcados(self):
        pass

    def gerarNaoMarcados(self):
        for estado in self.tabelaEstados.keys():
            for i in range(len(self.tabelaEstados[estado])):
                if self.tabelaEstados[estado][i] is None:
                    self.estadosCombinados.append(set(estado + self.estados[i]))

        self.combinarNaoMarcados()

if __name__ == "__main__":
    afd = MyOperatingJSON()
    afd.load_to_memory('language_04')
    minimizado = Minimizacao(afd)
    minimizado.construirTabelaEstados()
    minimizado.marcarEstados()
    minimizado.verificarNaoMarcados()
    minimizado.gerarNaoMarcados()
    print(1)
