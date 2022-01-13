import json
import pathlib

# site do tutorial https://www.programiz.com/python-programming/json

path_input = pathlib.Path(pathlib.Path.cwd(), 'test', 'linguagem01.json')
path_output = pathlib.Path(pathlib.Path.cwd(), 'test', 'linguagem02.json')

with open(path_input) as f:
    data = json.load(f)

# como loopar as transições
for item in data['transitions']:
    print("de " + item['estado_de_saida'] + " para " + item['estado_de_chegada'] + " por " + item['simbolo_de_transicao'])

for item in data['transitions']:
    if item['simbolo_de_transicao'] == 'C':
        # how to remove transition
        data['transitions'].remove(item)
        # how to add a transition
        data['transitions'].append({"estado_de_chegada": "B", "estado_de_saida": "A","simbolo_de_transicao": "F"})

print()

for item in data['transitions']:
    print("de " + item['estado_de_saida'] + " para " + item['estado_de_chegada'] + " por " + item['simbolo_de_transicao'])

# Como declarar um json(so por curiosidade
# person_dict = {"name": "Bob",
#                "languages": ["English", "Fench"],
#                "married": True,
#                "age": 32
#                }


with open(path_output, 'w') as json_file:
    json.dump(data, json_file, indent=4, sort_keys=True)

# with open(path_output, 'w') as json_file:
#     json.dump(person_dict, json_file, indent=4, sort_keys=True)
