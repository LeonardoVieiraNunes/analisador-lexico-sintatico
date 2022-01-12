import json


class AutomatoFinito:
    def __init__(self, estados=[], simbolos=[], init='', aceita='', transicoes=dict({}), path=None):

        self.definicao_formal = {
            "estados": estados,
            "simbolos_entrada": simbolos,
            "estado_inicial": init,
            "estados_aceitacao": aceita,
            "transicoes": transicoes
        }
        if path != None:
            self.definicao_formal = self.af_de_json(path)

    def get_inicial(self):
        return self.definicao_formal['estado_inicial']

    def get_aceitacao(self):
        return self.definicao_formal['estados_aceitacao']

    def get_estados(self):
        return self.definicao_formal['estados']

    def get_transicoes(self):
        return self.definicao_formal['transicoes']

    def get_simbolos(self):
        return self.definicao_formal['simbolos_entrada']
    def af_de_json(self, path):
        with open(path) as file:
            afd = json.load(file)
        return afd

    def adicionar_estado(self, estado:str):
        if estado not in self.get_estados:
            self.definicao_formal['estados'].append(estado)

    def adicionar_transicao(self, origem, destino, simbolo):
        transicao = [destino,simbolo]
        if transicao not in self.get_transicoes()[origem]:
            self.definicao_formal['transicoes'][origem] = transicao

    def print(self):
        print('Estado do automato:')
        matriz_automato = [[None for i in range(len(self.get_simbolos()))] for j in range(len(self.get_estados()))]
        for i, estado in enumerate(self.get_estados()):
            if estado in self.get_transicoes().keys():
                for j, transicao in enumerate(self.get_transicoes()[estado]):
                    estado_fim = transicao[0]
                    simbolo_transicao = transicao[1]
                    indice_simbolo_transicao = self.get_simbolos().index(simbolo_transicao)
                    matriz_automato[i][indice_simbolo_transicao] = estado_fim

        string_inicial = "  "
        for simbolo in self.get_simbolos():
            string_inicial+=f"    |{simbolo}| "
        print(string_inicial)
        for i, linha in enumerate(matriz_automato):
            string_linha = f"{self.get_estados()[i]} "

            if self.get_estados()[i] in self.get_aceitacao() and self.get_estados()[i] == self.get_inicial():
                string_linha = '->' + string_linha.strip()+'* '

            elif self.get_estados()[i] == self.get_inicial():
                string_linha = '->'+string_linha+' '

            elif self.get_estados()[i] in self.get_aceitacao():
                string_linha = string_linha.strip()+'*   '



            for coluna in linha:
                texto = str(coluna)
                if coluna is None:
                    texto = '-'
                string_linha += f" |{texto}|    "
            print(string_linha)
        return


if __name__=="__main__":
    teste = AutomatoFinito(path='afd.json')
    teste.print()
