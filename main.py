import operating_JSON

if __name__ == "__main__":
    test_module_instantiation = operating_JSON.MyOperatingJSON()
    test_module_instantiation.load_to_memory("language_01")
    print(test_module_instantiation.data)
    print(test_module_instantiation.data['transitions'])
    test_module_instantiation.remove_transition("B", "A", "F")
    print(test_module_instantiation.data['transitions'])
    test_module_instantiation.add_transition("A", "B", "X")
    print(test_module_instantiation.data['transitions'])
    test_module_instantiation.remove_state("F")
