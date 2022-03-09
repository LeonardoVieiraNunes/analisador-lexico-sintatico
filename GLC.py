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


if __name__ == "__main__":
    glc = GLC()
    glc.load_to_memory('test/rec_esquerda.txt')
