import pathlib
# from pprint import pprint
from operating_JSON import MyOperatingJSON
from read_input import MyCheckOfInput
from determinizacao import MyDeterminationOfInput
from simplified_union_intersection import MyUnionIntersection
from minimizacao import Minimizacao

if __name__ == "__main__":

    my_test = MyOperatingJSON()
    my_automata1 = MyOperatingJSON()
    my_automata2 = MyOperatingJSON()
    valid_file_paths = False
    operation = '0'
    file_name1 = ''
    file_name2 = ''
    while operation != '-1':
        operation = input("Digite o numero da opção referente a operação que deseja realizar(digite -1 para parar)\n"
                          "1. Converter um AFND para AFD\n"
                          "2. Reconhecimento de sentenças em AF\n"
                          "3. Minimização de AFD\n"
                          "4. União de dois automotos\n"
                          "5. Intersecção de dois automotos\n"
                          "6. Conversão de ER para AFD\n")
        if operation not in ['-1', '1', '2', '3', '4', '5', '6']:
            print("Por favor selecione uma operação valida\n")
        if operation in ['1', '2', '3', '4', '5']:
            file_name1 = input("Digite o nome do arquivo JSON que esta salvo na pasta test que voce quer utilizar\n")
            path_input = pathlib.Path(pathlib.Path.cwd(), 'test', file_name1 + '.json')
            if path_input.exists():
                valid_file_paths = True
                my_automata1.load_to_memory(file_name1)
                if operation in ['4', '5']:
                    file_name2 = input("Digite o nome do segundo arquivo que voce quer utilizar\n")
                    path_input = pathlib.Path(pathlib.Path.cwd(), 'test', file_name1 + '.json')
                    if path_input.exists():
                        my_automata2.load_to_memory(file_name2)
                    else:
                        valid_file_paths = False
            else:
                valid_file_paths = False
            if valid_file_paths:
                if operation == '1':
                    my_test = MyDeterminationOfInput()
                    my_test.determination_of_single_automata(my_automata1)
                if operation == '2':
                    my_test = MyCheckOfInput(my_automata1)
                    input_to_test = '-1'
                    while input_to_test != 'exit':
                        input_to_test = input("Digite entrada para testar ou digite \"exit\" para parar de checar inputs\n")
                        if input_to_test != 'exit':
                            my_test.test_input(input_to_test)
                if operation == '3':
                    my_test = Minimizacao(my_automata1)
                    my_test.minimizar()
                if operation == '4':
                    my_test = MyUnionIntersection()
                    my_test.make_union(my_automata1, my_automata2)
                if operation == '5':
                    my_test = MyUnionIntersection()
                    my_test.make_intersection(my_automata1, my_automata2)
                # if operation == '6'

                if operation in ['1', '3', '4', '5']:
                    decision = input("Deseja salvar o automato resultante das operações realizadas?(sim,nao)\n")
                    if decision == 'sim':
                        name_to_save = input("Digite o nome que deseja salvar o automato\n")
                        my_test.save_to_disc(name_to_save, my_test.new_automata.data)
            else:
                print("Por favor repita a operação\n")
