from nfa import *
import nfaToDfa


def nullable(nodo):
    data = nodo.data
    if data == EPSILON:
        return True
    if data not in OPERADORES:
        return False

    if data == '*':
        return True
    if data == '?':
        return True
    if data == '+':
        return nullable(nodo.left)
    if data == '|':
        return nullable(nodo.left) or nullable(nodo.right)
    if data == '^':
        return nullable(nodo.left) or nullable(nodo.right)

def firstPos(nodo):
    data = nodo.data
    primerpos = set()
    if data == EPSILON:
        return primerpos
    if data not in OPERADORES:
        primerpos.add(nodo.position)
    if data == '*':
        primerpos = firstPos(nodo.left)
    if data == '?':
        primerpos = firstPos(nodo.left)
    if data == '+':
        primerpos = firstPos(nodo.left)
    if data == '|':
        primerpos = firstPos(nodo.left).union(firstPos(nodo.right))
    if data == '^':
        if nullable(nodo.left):
            primerpos = firstPos(nodo.left).union(firstPos(nodo.right))
        else:
            primerpos = firstPos(nodo.left)
    return primerpos

def lastPos(nodo):
    data = nodo.data
    laspos = set()
    if data == EPSILON:
        return laspos
    if data not in OPERADORES:
        laspos.add(nodo.position)
    if data == '*':
        laspos = lastPos(nodo.left)
    if data == '?':
        laspos = lastPos(nodo.left)
    if data == '+':
        laspos = lastPos(nodo.left)
    if data == '|':
        laspos = lastPos(nodo.left).union(lastPos(nodo.right))
    if data == '^':
        if nullable(nodo.right):
            laspos = lastPos(nodo.left).union(lastPos(nodo.right))
        else:
            laspos = lastPos(nodo.right)
    return laspos


def followPos(raiz, fpos = {}, simbolos = {}):
    if not raiz:
        return
    if (raiz not in OPERADORES) and (raiz.data != EPSILON):
        simbolos[raiz.data].add(raiz.position)

    followPos(raiz.right, fpos, simbolos)
    followPos(raiz.left, fpos,simbolos)

    if raiz.data == '^':
        for pos in lastPos(raiz.left):
            fpos[pos].update(firstPos(raiz.right))
    if raiz.data == '*':
        for pos in lastPos(raiz):
            fpos[pos].update(firstPos(raiz))
    return fpos, simbolos

