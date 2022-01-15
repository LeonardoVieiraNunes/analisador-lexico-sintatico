import json
import pathlib

# site do tutorial https://www.programiz.com/python-programming/json

path_input = pathlib.Path(pathlib.Path.cwd(), 'test', 'language_01.json')
path_output = pathlib.Path(pathlib.Path.cwd(), 'test', 'language_02.json')

with open(path_input) as f:
    data_test = json.load(f)

# como loopar as transições
for item in data_test['transitions']:
    print("de " + item['state_from'] + " para " + item['state_to'] + " por " + item['transition_symbol'])

for item in data_test['transitions']:
    if item['transition_symbol'] == 'C':
        # how to remove transition
        data_test['transitions'].remove(item)
        # how to add a transition
        data_test['transitions'].append({"state_from": "B", "state_to": "A", "transition_symbol": "F"})

print()

for item in data_test['transitions']:
    print("de " + item['state_from'] + " para " + item['state_to'] + " por " + item['transition_symbol'])

# Como declarar um json(so por curiosidade
# person_dict = {"name": "Bob",
#                "languages": ["English", "Fench"],
#                "married": True,
#                "age": 32
#                }


with open(path_output, 'w') as json_file:
    json.dump(data_test, json_file, indent=4, sort_keys=True)

# with open(path_output, 'w') as json_file:
#     json.dump(person_dict, json_file, indent=4, sort_keys=True)
