from operating_JSON import MyOperatingJSON

def find_unreachable_states(afd: MyOperatingJSON):
    init = afd.get_initial()
    reachable_states = [init]
    for state in reachable_states:
        transitions = afd.get_all_transitions_from_state(state)
        new_states = [x['state_to'] for x in transitions]
        for temp in new_states:
            if temp not in reachable_states:
                reachable_states.append(temp)

    unreachable_states = list(filter(lambda x: x not in reachable_states, afd.get_states()))

    return unreachable_states



if __name__ == "__main__":
    afd = MyOperatingJSON()
    afd.load_to_memory('language_01')
    find_unreachable_states(afd)
