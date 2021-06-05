OPS = ["[", "{", "|", "("]
FINAL = ["]", "}", "|", ")"]
OPERADORES = ["*", "|", "?", "^", ")", "("]

import utils

def parser(productions, parse_line, tokens, keywords):
    file = open("./outputs/parser.py", 'w+')
    string = "class Parser:\n"

    string += "\tdef __init__(self, tokens):\n"
    string += "\t\tself.tokens = tokens\n"
    string += "\t\tself.id_token = 0\n"
    string += "\t\tself.actual_token = self.tokens[self.id_token]\n"
    string += "\t\tself.last_token = ''\n"

    string += "\tdef advance( self ):\n"
    string += "\t\tself.id_token += 1\n"
    string += "\t\tif self.id_token < len(self.tokens):\n"
    string += "\t\t\tself.actual_token = self.tokens[self.id_token]\n"
    string += "\t\t\tself.last_token = self.tokens[self.id_token - 1]\n\n"

    string += "\tdef expect(self, item, arg = None):\n"
    string += "\t\tog = self.id_token\n"
    string += "\t\tpossible = False\n"
    string += "\t\tif item != None:\n"
    string += "\t\t\ttry:\n"
    string += "\t\t\t\tif arg == None:\n"
    string += "\t\t\t\t\tans = item()\n"
    string += "\t\t\t\telse:\n"
    string += "\t\t\t\t\tans = item(arg)\n"
    string += "\t\t\t\tif type(ans) == bool:\n"
    string += "\t\t\t\t\tpossible = ans\n"
    string += "\t\t\t\telse:\n"
    string += "\t\t\t\t\tpossible = True\n"
    string += "\t\t\texcept:\n"
    string += "\t\t\t\tpossible = False\n"
    string += "\t\tself.id_token = og\n"
    string += "\t\tself.actual_token = self.tokens[self.id_token]\n"
    string += "\t\tself.last_token = self.tokens[self.id_token - 1]\n"
    string += "\t\treturn possible\n\n"

    string += "\tdef read(self, item, type = False):\n"
    string += "\t\tif type:\n"
    string += "\t\t\tif self.actual_token.type == item:\n"
    string += "\t\t\t\tself.advance()\n"
    string += "\t\t\t\treturn True\n"
    string += "\t\t\telse:\n"
    string += "\t\t\t\treturn False\n"
    string += "\t\telse:\n"
    string += "\t\t\tif self.actual_token.value == item:\n"
    string += "\t\t\t\tself.advance()\n"
    string += "\t\t\t\treturn True\n"
    string += "\t\t\telse:\n"
    string += "\t\t\t\treturn False\n"

    string += "\tvalue, result, value1, value2 = 0,0,0,0\n"

    new_tokens = []
    for p in productions:
        string = first(p, string)
        string, news = second(productions[p], string, parse_line, tokens, keywords)
        string += "\n"
        for token in news:
            if token not in new_tokens:
                new_tokens.append(token)


    file.write(string)
    file.close()
    new_parse = parse_line[:-1]
    for token in new_tokens:
        if token in OPERADORES or token == utils.EPSILON:
            new_parse += "|" + str(ord(token))
        else:
            new_parse += "|" + token
    new_parse = new_parse + ")"
    fixed_parser = expecterino(string)
    return fixed_parser, new_parse


def expecterino(parser):
    parser = parser.split("\n")
    new_parser = ""
    for line in parser:
        if "self.expect(" in line and "while" not in line:
            original = line
            new_line = line.split("(", 1)
            new_parser += new_line[0] + "("
            args = new_line[1].split("(", 1)
            second = args[1].replace(")", "")
            second = second.replace(":", "")
            new_parser += args[0] + "," + second + "):\n"
        elif "self.expect(" in line and "while" in line:
            or_parted = line.split("or")
            for part in or_parted:
                new_line = part.split("(", 1)
                new_parser += new_line[0] + "("
                args = new_line[1].split("(", 1)
                second = args[1].replace(")", "")
                new_parser += args[0] + "," + second[:-1] + ") or"
            new_parser = new_parser[:-2] + ":\n"
        else:
            new_parser += line + "\n"
    return new_parser


def first(name, string):
    name = name.replace("\n", "")
    name = name.replace("\t", "")
    name = name.replace(" ", "")
    f_name = name.split("<")[0]
    string += "\tdef " + f_name + "(self"
    if "<" in name:
        f_params = name.split("<")[1]
        string += "," + f_params[:-1]
    string += "):\n"
    return string

def second(body, string, line, toks, keywords):
    nTokens = []
    current = 0
    temp = ""
    tabs = "\t\t"
    flag = False
    inner_flag = False
    while current < len(body):
        if body[current] == "{":
            foo = current + 1
            marker = 0
            while body[foo] not in OPS and marker != 2:
                if body[foo] == " ":
                    pass
                elif body[foo] == '"':
                    marker += 1
                    temp += body[foo]
                else:
                    temp += body[foo]
                foo += 1
            if "<" in temp:
                if flag:
                    temp = "self.expect('" + temp + "'):"
                    flag = False
                name = temp.split("<", 1)[0]
                arg = temp.split("<", 1)[1][:-1]
                temp = "self." + name + "(" + arg + ")"
            elif '"' in temp:
                temp = "self.read(" + temp + ")"
            else:
                temp = "self." + temp + "()"
            string += tabs + "while self.expect(" + temp + "):\n"
            temp = ""
            tabs += "\t"
        elif body[current] == "}":
            tabs = tabs.replace("\t", "", 1)
            if inner_flag:
                tabs = tabs.replace("\t", "", 1)

        elif body[current] == "(" and body[current + 1] == ".":
            current += 2
            while body[current] != "." or body[current + 1] != ")":
                temp += body[current]
                current += 1
            current += 1
            string += tabs + temp + "\n"
            temp = ""

        elif body[current] == '"':
            current += 1
            while body[current] != '"':
                temp += body[current]
                current += 1
            if flag:
                string += "self.expect(self.read('" + temp + "')):\n"
                flag = False
            string += tabs + 'self.read("' + temp + '")\n'
            nTokens.append(temp)
            temp = ""

        elif body[current] == "(":
            pass

        elif body[current] == ")":
            if inner_flag:
                tabs = tabs.replace("\t", "", 1)

        elif body[current] == "[":
            string += tabs + "if "
            flag = True
            tabs += "\t"

        elif body[current] == "]":
            tabs = tabs.replace("\t", "", 1)
            if inner_flag:
                tabs = tabs.replace("\t", "", 1)

        elif body[current] == "|":
            foo = current - 1
            while foo > 0:
                if body[foo] == " " or body[foo] == "\n":
                    pass
                elif body[foo] == "." and body[foo - 1] == "(":
                    foo -= 1
                elif body[foo] in OPS:
                    break
                foo -= 1

            if body[foo] == "{":
                pt = string.rfind("while")
                while string[pt] != ":":
                    pt += 1
                marker = 0
                i = current + 1
                while body[i] not in OPS and marker != 2:
                    if body[i] == " ":
                        pass
                    elif body[i] == '"':
                        marker += 1
                        temp += body[i]
                    else:
                        temp += body[i]
                    i += 1
                if "<" in temp:
                    if flag:
                        string += "self.expect('" + temp + "'):"
                        flag = False
                    name = temp.split("<", 1)[0]
                    arg = temp.split("<", 1)[1][:-1]
                    temp = "self." + name + "(" + arg + ")"
                elif '"' in temp:
                    temp = "self.read(" + temp + ")"
                else:
                    temp = "self." + temp + "()"
                first_if = string[pt+2:].split("\n")[0]
                split_string = string[pt+1:]
                string = string[:pt] + " or self.expect(" + temp + ")" + ":\n"
                first_if = first_if.replace("\t", "")
                string += tabs + "if self.expect(" + first_if + "):"
                lns = split_string.split("\n")
                for ln in lns:
                    string += "\t" + ln + "\n"

            elif body[foo] == "(":
                i = foo + 1
                marker = 0
                while body[i] not in OPS and marker != 2:
                    if body[i] == " ":
                        pass
                    elif body[i] == '"':
                        marker += 1
                        temp += body[i]
                    else:
                        temp += body[i]
                    i += 1
                if "<" in temp:
                    if flag:
                        string += "self.expect('" + temp + "'):"
                        flag = False
                    name = temp.split("<", 1)[0]
                    arg = temp.split("<", 1)[1][:-1]
                    temp = arg + "=self." + name + "(" + arg + ")"
                elif '"' in temp:
                    temp = "self.read(" + temp + ")"
                else:
                    temp = "self." + temp + "()"
                pre = string.rfind(temp)
                split_string = string[pre:]
                if "=" in temp:
                    exp_arg = temp.split("=")[1]
                else:
                    exp_arg = temp
                string = string[:pre] + "if self.expect(" + exp_arg + "):\n"
                lns = split_string.split("\n")
                for ln in lns:
                    string += tabs + "\t" + ln + "\n"
                temp == ""
            elif body[foo] == "|":
                pass

            temp = ""
            inner_flag = True
            i = current + 1
            marker = 0
            inner_inner_flag = False
            while (body[i] not in OPS or not inner_inner_flag) and marker != 2:
                if body[i] == ")" and not inner_inner_flag:
                    break
                if body[i] == " ":
                    pass
                elif body[i] == '"':
                    marker += 1
                    temp += body[i]
                else:
                    temp += body[i]
                i += 1
            if "<" in temp:
                if flag:
                    string += "self.expect('" + temp + "'):"
                    flag = False
                name = temp.split("<", 1)[0]
                arg = temp.split("<", 1)[1][:-1]
                temp = "self." + name + "(" + arg + ")"
            elif '"' in temp:
                temp = "self.read(" + temp + ")"
            else:
                temp = "self." + temp + "()"
            string += tabs + "elif self.expect(" + temp + "):\n"
            tabs += "\t"
            temp = ""
        elif body[current] == " " or body[current] == "\n" or body[current] == "\t":
            if temp != "":
                if temp in toks or temp in keywords:
                    string += tabs + "self.read('" + temp + "', True)\n"
                elif "<" in temp:
                    if flag:
                        string += "self.expect('" + temp + "'):\n"
                        flag = False
                    name = temp.split("<", 1)[0]
                    arg = temp.split("<", 1)[1][:-1]
                    string += tabs + arg.replace(" ", "") + "=self." + name + "(" + arg + ")\n"
                else:
                    if flag:
                        string += "self.expect('" + temp + "'):\n"
                        flag = False
                    string += tabs + "self." + temp + "()\n"
                temp = ""
            else:
                pass

        else:
            temp += body[current]
        current += 1
    return string, nTokens
