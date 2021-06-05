import automateichon
import automataEsq
import nfaToDfa
import utils
from graphviz import Digraph

VALIDOS = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
OPERADORES = ["*", "|", "?", "^", ")"]
OPERADORESUNI = ["*", "?"]
COUNT = [10]
EPSILON = "ε"


class Nodo:
    def __init__(self, data):
        self.right = None
        self.left = None
        self.position = None
        self.data = data


def print2DUtil(root, space):
  
    # Base case  
    if (root == None) : 
        return
  
    # Increase distance between levels  
    space += COUNT[0] 
  
    # Process right child first  
    print2DUtil(root.right, space)  
  
    # Print current node after space  
    # count  
    print()  
    for _ in range(COUNT[0], space): 
        print(end = " ")
    print(root.data)  
  
    # Process left child  
    print2DUtil(root.left, space)  
  
# Wrapper over print2DUtil()  
def print2D(root) : 
      
    # space=[0] 
    # Pass initial space count as 0  
    print2DUtil(root, 0)

def arbolillo(expresion):
    vals = []
    ops = []
    i = 0

    while i < len(expresion):
        if expresion[i] == ' ':
            i += 1
            continue
        if expresion[i] == '(':
            ops.append(expresion[i])  
        elif expresion[i] not in OPERADORES:
            val = ""
            while(i<len(expresion) and expresion[i] not in OPERADORES):
                val += expresion[i]
                i += 1
            i -= 1
            val = Nodo(val)
            vals.append(val)

        elif expresion[i] == ')':
            while len(ops) != 0 and ops[-1] != '(':
                val2 = vals.pop()
                val1 = vals.pop()
                op = ops.pop()
                nodito = Nodo(op)
                nodito.left = val1
                nodito.right = val2
                vals.append(nodito)
            ops.pop()

        else:
            if(expresion[i] in OPERADORESUNI):
                ops.append(expresion[i])
                op = ops.pop()
                val = vals.pop()
                nodito = Nodo(op)
                nodito.right = None
                nodito.left = val
                vals.append(nodito)
            else:
                while (len(ops) != 0 and ops[-1] != '('):
                    op = ops.pop()
                    val2 = vals.pop()
                    val1 = vals.pop()
                    nodito = Nodo(op)
                    nodito.left = val1
                    nodito.right = val2
                    vals.append(nodito)
                ops.append(expresion[i])

        i += 1
    while len(ops) != 0:
        val2 = vals.pop()
        val1 = vals.pop()
        op = ops.pop()
        nodito = Nodo(op)
        nodito.left = val1
        nodito.right = val2
        vals.append(nodito)
        if (len(vals) == 1):
            return vals[-1]
    return vals[-1]

def create_automataRepresentation(arbolito, expresion):
    auto = automataEsq.Machine(expresion)
    print2D(arbolito)
    automaton = automateichon.automataBuilder(arbolito, auto)
    auto.states[-1].accept = True
    dfatext = open("nfa.txt","w")
    for state in auto.states:
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
  
    dot = Digraph()
    for state in auto.states:
        if state.accept == True:
            dot.node(str(state.id), str(state.id), shape = "doublecircle")
        for t in state.transitions:
            dot.edge(str(state.id), str(t.destino), str(t.simbolo))
    print(dot.source)
    dot.render('test-output/round-table.pdf', view=True)
    return automaton


def matchingNfa(arbolito, expresion, textillo):
    auto = automataEsq.Machine(expresion)
    automateichon.automataBuilder(arbolito, auto)
    aceptados = []
    for r in expresion:
        if r not in OPERADORES:
            if r != '(':
                aceptados.append(r)
    for x in textillo:
        if x not in aceptados:
            print("no aceptado")
            return 0
    opciones = list(textillo)
    estaditos = [0]
    estaditos = utils.cerraduraEpsilon(auto, estaditos)
    auto.states[-1].accept = True
    i = 0
    while True:
        tempstates = []
        for estado in estaditos:
            for trans in auto.states[estado].transitions:
                if trans.simbolo == opciones[i] and trans.destino not in tempstates:
                    tempstates.append(trans.destino)
        i += 1
        tempstates = utils.cerraduraEpsilon(auto, tempstates)
        if not tempstates and expresion == EPSILON:
            break
        estaditos = tempstates.copy()
        if i > len(opciones)-1:
            break
    for x in estaditos:
        if auto.states[x].accept:
            return print("Aceptado")
    return print("No Aceptado")


if __name__ == "__main__":
    print("Ingrese la expresion Regular con el simbolo '^' para la concatenacion: ")
    exp = input()
    print("Ingrese la cadena a probar:")
    cadena = input()
    ans = arbolillo(exp)
    create_automataRepresentation(ans, exp)
    nfaToDfa.nfaToDfa(ans, exp)