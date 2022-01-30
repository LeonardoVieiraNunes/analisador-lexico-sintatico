from pprint import pprint
from operating_JSON import MyOperatingJSON
from read_input import MyCheckOfInput
from determinizacao import MyDeterminationOfInput

if __name__ == "__main__":
    # example of operations
    # test_module_instantiation = MyOperatingJSON()
    # test_module_instantiation.load_to_memory("language_01")
    # print(test_module_instantiation.data)
    # print(test_module_instantiation.data['transitions'])
    # test_module_instantiation.remove_transition("B", "A", "F")
    # print(test_module_instantiation.data['transitions'])
    # test_module_instantiation.add_transition("A", "B", "X")
    # print(test_module_instantiation.data['transitions'])
    # test_module_instantiation.remove_state("F")

    # example test of input
    # test = MyCheckOfInput()
    # test.set_dfa("language_04")
    # test.test_input("0010")

    # example of transformation of not deterministic to deterministic automata
    my_test = MyDeterminationOfInput()
    my_test.set_automata('language_05')
    my_test.base_automata.save_to_disc('test')
    pprint(my_test.base_automata.data)
    

