import re

import automateichon
import automataEsq
import nfaToDfa
import nfa
import utils
import lecture
import string

def changeANY(menos = ""):
    todo = string.printable
    todo = todo.replace(menos, '')
    stringerino = ""
    print("este es el nuevo", todo)
    for t in todo:
        stringerino += t + "|"
    print(stringerino[:-1])
    return stringerino[:-1]


def charToAutomata(charactrers):
    charas_line = {}
    for c in charactrers:
        temp = ""
        i = 0
        toparse = ""
        flagerino = False
        while i < len(charactrers[c]):
            if charactrers[c][i] == '"' or charactrers[c][i] == "'":
                flagerino = not flagerino
                if not flagerino:
                    temp = temp[:-1] + ")"
                    toparse += temp
                    temp = ""
                else:
                    temp += "("
            elif flagerino:
                temp += charactrers[c][i] + "|"
            elif charactrers[c][i] == "+":
                toparse += "|"
            elif temp + charactrers[c][i] in charas_line:
                toparse += charas_line[temp+charactrers[c][i]]
                temp = ""
            elif temp == ".":
                if charactrers[c][i] == ".":
                    start = toparse[-2]
                    while i < len(charactrers[c]):
                        if charactrers[c][i] == "'":
                            break
                        i += 1
                    finish = charactrers[c][i+1]
                    j = ord(start)
                    while j < ord(finish):
                        toparse += "|" + chr(j)
                        j += 1
                        print(toparse)
                    toparse += "|" + finish
            elif temp == "CHR(":
                interino = ""
                while i < len(charactrers[c]):
                    if charactrers[c][i] == ")":
                        break
                    elif charactrers[c][i] == " ":
                        pass
                    else:
                        interino += charactrers[c][i]
                    i += 1
                interino = int(interino)
                print(interino)
                sym = chr(interino)
                toparse += "'"+sym+"'"
                temp = ""
            elif temp == "ANY":
                temp2 = ""
                while i < len(charactrers[c]):
                    temp2 += charactrers[c][i]
                    i+=1
                temp2 = temp2.split('-')
                temp2 = temp2[1:]
                contador = 0
                while contador < len(temp2):
                    temp2[contador] = temp2[contador].replace('.', '')
                    contador+=1
                quitar = ""
                for temi in temp2:
                    toremove = "()'"
                    pattern = "[" + toremove + "]"
                    if temi in charas_line:
                        if temi == "ignore":
                            pass
                        else:
                            quitar += charas_line[temi]
                quitar = re.sub(pattern, "", quitar)
                print("esto es quitar", quitar)
                toparse = changeANY(quitar)
                temp = ""
            else:
                temp += charactrers[c][i]
            i += 1
        charas_line[c] = "(" + toparse + ")"
    print("estos son los characters automata",charas_line)
    return charas_line


def keyworder(keywords):
    key_lines = {}
    for k in keywords:
        temp = ""
        i = 0
        worderino = keywords[k][:-1]
        flagerino = False
        while i < len(worderino):
            if worderino[i] == '"':
                flagerino = not flagerino
                if not flagerino:
                    temp = temp[:-1] + ")"
                else:
                    temp += "("
            else:
                temp += worderino[i] + "^"
            i += 1
        key_lines[k] = temp
    print("estos son los keywords:", key_lines)
    return key_lines


def tokensToAutomata(toks, charas):
    tokens_line = {}
    for t in toks:
        tok = toks[t]
        i = 0
        temp = ""
        toparse = ""
        flagerino = False
        while i < len(tok):
            temp += tok[i]
            if temp in charas:
                original = temp
                temp = longest_string(tok, charas, i, temp)
                if original != temp:
                    i += len(temp) - len(original)
                if flagerino:
                    toparse += charas[temp] + ")*"
                else:
                    toparse += charas[temp] + ")"
                temp = ""
            if temp == "|":
                toparse = toparse[:-2] + "|"
                temp = ""
            if temp == "{":
                flagerino = not flagerino
                toparse += "^("
                temp = ""
            if temp == "}" and flagerino:
                flagerino = not flagerino
                toparse += "^"
                temp = ""
            if temp.isspace():
                toparse += "^"
            if temp == "[":
                if toparse != "":
                    toparse += "^"
                toparse += "("
                temp = ""
            if temp == "]":
                toparse += ")?^("
                temp = ""
            if temp == '"':
                interno = ""
                i += 1
                while i < len(tok):
                    if tok[i] == '"':
                        break
                    interno += tok[i]
                    i += 1
                if toparse != "" and ("^" not in toparse):
                    toparse += "^(" + interno + ")"
                else:
                    toparse += "(" + interno + ")"
                if tok[i + 1] != "" and tok[i + 1] != "\n" and tok[i + 1] != ".":
                    toparse += "^"
                temp = ""
            if temp == "(":
                toparse += "("
                temp = ""
            if temp == ")":
                toparse += ")"
                temp = ""
            i += 1
        if toparse[-1] == "|" or toparse[-1] == "^":
            toparse = toparse[:-1]
        tokens_line[t] = "((" + toparse
    print("estos son los tokens:", tokens_line)
    return tokens_line


def theBigOne(keywords, tokens):
    bigOne = ""
    dfas = {}
    for k in keywords:
        bigOne += keywords[k] + "|"
        tree = nfa.arbolillo(keywords[k])
        dfas[k] = nfaToDfa.nfaToDfa(tree, keywords[k])
    for t in tokens:
        if '\r' in tokens[t] or '\n' in tokens[t] or '\t' in tokens[t]:
            pass
        else:
            bigOne += tokens[t] + "|"
            arbolito = nfa.arbolillo(tokens[t])
            dfas[t] = nfaToDfa.nfaToDfa(arbolito, tokens[t])
    bigOne = bigOne[:-1]
    bigOne = "(" + bigOne + ")))"
    return bigOne, dfas

def makeTheBigOne(bigOne):
    bigTree = nfa.arbolillo(bigOne)
    bigAutomata = nfaToDfa.nfaToDfa(bigTree, bigOne)
    return bigAutomata

def longest_string(longest, charas, current = 0, start = ""):
    temp = start
    current += 1
    accepted = [start]
    while current < len(longest):
        temp += longest[current]
        if temp in charas:
            accepted.append(temp)
        current += 1
    return max(accepted, key=len)