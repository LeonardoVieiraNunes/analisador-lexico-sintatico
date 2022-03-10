class GLC:
    def __init__(self):
        self.producoes = dict()
        self.naoTerminais = list()
        self.terminais = list()
        self.inicial = 'S'

    def load_to_memory(self, file_name: str):
        f = open(file_name, 'r')
        for line in f.readlines():
            naoTerminal, producao = line.rstrip('\n').split(' -> ')

            for s in producao:
                if str(s).islower() and s not in self.terminais:
                    self.terminais.append(s)

            if naoTerminal not in self.naoTerminais:
                self.naoTerminais.append(naoTerminal)

            if naoTerminal not in self.producoes.keys():
                self.producoes[naoTerminal] = [producao]
            else:
                self.producoes[naoTerminal] += [producao]

    def eliminar_recursoes(self):
        naoTerminais = self.naoTerminais
        for i in range(len(naoTerminais)):
            producoesI: list = self.producoes[naoTerminais[i]]
            for j in range(i):

                for prodI in producoesI:
                    alpha = None
                    if len(prodI) > 1:
                        alpha = prodI[1:]

                    if prodI[0] == naoTerminais[j]:
                        producoesI.remove(prodI)
                        producoesJ = self.producoes[naoTerminais[j]]
                        for prodJ in producoesJ:
                            producoesI.append(prodJ + alpha)
            hasRecEsquerda = len(list(filter(lambda p: p[0] == naoTerminais[i], producoesI))) > 0
            if hasRecEsquerda:
                novoNaoTerminal = f"{naoTerminais[i]}'"

                self.producoes[novoNaoTerminal] = list()
                producoesNovoTerminal: list = self.producoes[novoNaoTerminal]

                self.naoTerminais.append(novoNaoTerminal)
                for k in range(len(producoesI)):
                    if producoesI[k][0] != naoTerminais[i]:
                        producoesI[k] += novoNaoTerminal
                    else:
                        producoesNovoTerminal.append(producoesI[k][1:] + novoNaoTerminal)

                producoesNovoTerminal.append('&')

                for prod in producoesI:
                    if prod[0] == naoTerminais[i]:
                        producoesI.remove(prod)

                pass









if __name__ == "__main__":
    glc = GLC()
    glc.load_to_memory('test/rec_esquerda_2.txt')
    glc.eliminar_recursoes()
