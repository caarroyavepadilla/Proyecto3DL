from nfa import *
import utils

VALIDOS = ["A", "B", "C", "D" ,"E", "a" ,"b" ,"c" ,"d" ,"e","ε", "0","1"]
OPERADORES = ["*", "|", "?", "+", "^", ")"]
OPERADORESUNI = ["*", "?", "+"]
ABCEDARIO = ["A", "B", "C", "D" ,"E", "F","G" ,"H", "I", "J"]
COUNT = [10]
EPSILON = "ε"

def nfaToDfa(arbolito, expresion):
    #hacer automata
    auto = automataEsq.Machine(expresion)
    automata = automataEsq.Machine(expresion)
    nuevosEstados = []
    opciones = []
    for u in expresion:
        if u not in OPERADORES:
            if u != '(' and u not in opciones:
                opciones.append(u)
    automateichon.automataBuilder(arbolito, auto)
    primero = utils.cerraduraEpsilon(auto, [0])
    primero = set(primero)
    auto.states[-1].accept = True
    nuevosEstados.append(primero)
    primerito = automataEsq.State(len(automata.states))
    primerito.vaina.append(primero)           
    automata.states.append(primerito)
    for i in automata.states:
        for opcion in opciones:
            tempstates = set()
            for state in auto.states:
                if state.id in nuevosEstados[i.id]:
                    for trans in state.transitions: 
                        if trans.simbolo == opcion:
                            tempstates.add(trans.destino)
            x = set()
            for temp in tempstates:
                x.add(temp)
                x.update(utils.cerraduraEpsilon(auto,[temp]))
            if x not in nuevosEstados:
                if len(x) != 0:
                    nuevosEstados.append(x)
                    estadox = automataEsq.State(len(automata.states))
                    estadox.vaina.append(x)
                    for y in x:
                        if auto.states[y].accept == True:
                            estadox.accept = True
                    automata.states.append(estadox)
                    i.transitions.append(automataEsq.Transition(opcion,estadox.id))
            elif x in nuevosEstados:
                if len(x) != 0:
                    for h in automata.states:
                        if h.vaina[0] == x:
                            i.transitions.append(automataEsq.Transition(opcion,h.id))
    print(nuevosEstados)
   # imprimir automat

    dfatext = open("dfa.txt","w")
    for state in automata.states:
        identidad = "estado: " + str(state.id) + "\n"
        aceptacion = "Aceptacion: "+str(state.accept) + "\n" 
        dfatext.write(identidad)
        dfatext.write(aceptacion)
        for trap in state.transitions:
            if trap.simbolo == EPSILON:
                z = "E"
            else:
                z = trap.simbolo
            texto = "Transicion: " + str(trap.destino) + " " + "Con: " + z + "\n"
            dfatext.write(texto)
    dfatext.close

    return automata


def matchingDFA(automata, expresion, textillo):
 #matching
    aceptados = []
    for e in expresion:
        if e not in OPERADORES:
            if e != '(':
                aceptados.append(e)
    for g in textillo:
        if g not in aceptados:
            print("no aceptado")
            return 0
    opts = list(textillo)
    est = [0]
    est = utils.cerraduraEpsilon(automata, est)
    q = 0
    while True:
        temporales = []
        for es in est:
            for trans in automata.states[es].transitions:
                if trans.simbolo == opts[q] and trans.destino not in temporales:
                    temporales.append(trans.destino)
        q += 1
        temporales = utils.cerraduraEpsilon(automata, temporales)
        if not temporales and opts == EPSILON:
            break
        est = temporales.copy()
        if q > len(opts)-1:
            break
    for x in est:
        if automata.states[x].accept:
            return print("Aceptado")
    return print("No Aceptado")  