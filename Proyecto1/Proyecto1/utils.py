EPSILON = "ε"
def cerraduraEpsilon(automata, current):
    for i in current:
        for j in automata.states[i].transitions:
            if j.simbolo == EPSILON and j.destino not in current:
                current.append(j.destino)
    return current