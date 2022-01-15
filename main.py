import operating_JSON

if __name__ == "__main__":
    test_module_instantiation = operating_JSON
    operating_JSON.load_to_memory(test_module_instantiation, "language_01")
    print(test_module_instantiation.data)
