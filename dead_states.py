from operating_JSON import MyOperatingJSON


def reaches_final_state(afd:MyOperatingJSON, state:str):
    for transition in afd.get_all_transitions_from_state(state):
        if transition['state_to'] in afd.get_final():
            return True
        else:
            return reaches_final_state(afd, transition['state_to'])

def find_dead_states(afd:MyOperatingJSON):
    dead_states = []
    for state in afd.get_states():
        if not reaches_final_state(afd, state) and state not in afd.get_final():
            dead_states.append(state)

    return dead_states



if __name__ == "__main__":
    afd = MyOperatingJSON()
    afd.load_to_memory('language_01')
    find_dead_states(afd)