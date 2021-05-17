import sys
import re

dictGlobal = {}


class Node:
    def __init__(self, valorNode, nodeList=[]):
        self.value = valorNode
        self.children = nodeList

    def Evaluate(self):
        pass


class BinOp(Node):
    def Evaluate(self):
        child1 = self.children[0].Evaluate()
        child2 = self.children[1].Evaluate()

        if self.value == "PLUS":
            valorOp = child1 + child2
        elif self.value == "MINUS":
            valorOp = child1 - child2
        elif self.value == "TIMES":
            valorOp = child1 * child2
        elif self.value == "OVER":
            valorOp = child1 / child2
        elif self.value == "MAIOR":
            valorOp = bool(child1 > child2)
        elif self.value == "MENOR":
            valorOp = bool(child1 < child2)
        elif self.value == "EQUAL":
            valorOp = bool(child1 == child2)
        elif self.value == "AND":
            valorOp = bool(child1 and child2)
        elif self.value == "OR":
            valorOp = bool(child1 or child2)
        else:
            raise ValueError("BinOp operation error")

        return int(valorOp)


class Atribuicao(Node):
    def Evaluate(self):
        child1 = self.children[0]

        if self.value == "ISTYPE":
            child2 = self.children[1]
            if child1 not in dictGlobal.keys():
                SymbolTable.setterType(child1, type_=child2)
            else:
                raise ValueError("Variavel already exists!")

        if self.value == "RECEBE":
            child2 = self.children[1].Evaluate()
            SymbolTable.setterValue(child1, child2)


class UnOp(Node):
    def Evaluate(self):
        child1 = self.children[0].Evaluate()

        if self.value == "PLUS":
            valorOp = child1
        elif self.value == "MINUS":
            valorOp = -child1
        elif self.value == "NOT":
            valorOp = not child1

        return int(valorOp)


class IntVal(Node):
    def Evaluate(self):
        valorInteiro = self.value
        return(valorInteiro)


class BoolVal(Node):
    def Evaluate(self):
        valorBooleano = self.value
        return(int(valorBooleano == "true"))


class Identific(Node):
    def Evaluate(self):
        valorVariavel = SymbolTable.getter(self.value)
        return(valorVariavel)


class NoOp(Node):
    def Evaluate(self):
        return


class Println(Node):
    def Evaluate(self):
        child1 = self.children[0].Evaluate()
        print(child1)


class Readln(Node):
    def Evaluate(self):
        valorInputado = input()
        return int(valorInputado)


class NodeBlock(Node):
    def Evaluate(self):
        for child in self.children:
            child.Evaluate()


class While(Node):
    def Evaluate(self):
        while self.children[0].Evaluate():
            self.children[1].Evaluate()


class If(Node):
    def Evaluate(self):
        if self.children[0].Evaluate():
            self.children[1].Evaluate()
        else:
            self.children[2].Evaluate()


class Token:
    def __init__(self, tipoToken, valorToken):
        self.type = tipoToken
        self.value = valorToken


class Tokenizer:
    def __init__(self, origin):
        self.origin = origin  # codigo fonte
        self.tokens = self.montador(self.origin)
        self.position = 0  # posicao atual
        self.actual = self.tokens[0]  # ultimo token

    def selectNext(self):
        self.position += 1
        self.actual = self.tokens[self.position]

    @staticmethod
    def montador(origin):
        tokens_list = []
        numero = ""
        identifier = ""
        operadorDuplo = ""
        origin += "#"
        countPar = 0
        countKey = 0
        palavrasReservadas = ["println", "readln",
                              "while", "if", "else", "int", "bool", "true", "false"]
        operadoresDuplos = ["=", "&", "|"]

        for caracter in origin:
            if identifier:
                if identifier[0] == "_":
                    raise ValueError("Variavel Não pode começar com _!")

            if(caracter.isdigit() and identifier == ""):
                numero += caracter

            elif(caracter == " "):
                if operadorDuplo:
                    if operadorDuplo == "=":
                        tokens_list.append(Token("RECEBE", operadorDuplo))
                    elif operadorDuplo == "==":
                        tokens_list.append(Token("EQUAL", operadorDuplo))
                    elif operadorDuplo == "&&":
                        tokens_list.append(Token("AND", operadorDuplo))
                    elif operadorDuplo == "||":
                        tokens_list.append(Token("OR", operadorDuplo))
                    operadorDuplo = ""
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        if identifier == "println":
                            tokens_list.append(Token("PRINT", identifier))
                        elif identifier == "readln":
                            tokens_list.append(Token("READLINE", identifier))
                        elif identifier == "while":
                            tokens_list.append(Token("WHILE", identifier))
                        elif identifier == "if":
                            tokens_list.append(Token("IF", identifier))
                        elif identifier == "else":
                            tokens_list.append(Token("ELSE", identifier))
                        elif identifier == "int" or identifier == "bool":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""

            elif(caracter == "+"):
                if operadorDuplo:
                    if operadorDuplo == "=":
                        tokens_list.append(Token("RECEBE", operadorDuplo))
                    elif operadorDuplo == "==":
                        tokens_list.append(Token("EQUAL", operadorDuplo))
                    elif operadorDuplo == "&&":
                        tokens_list.append(Token("AND", operadorDuplo))
                    elif operadorDuplo == "||":
                        tokens_list.append(Token("OR", operadorDuplo))
                    operadorDuplo = ""
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        if identifier == "println":
                            tokens_list.append(Token("PRINT", identifier))
                        elif identifier == "readln":
                            tokens_list.append(Token("READLINE", identifier))
                        elif identifier == "while":
                            tokens_list.append(Token("WHILE", identifier))
                        elif identifier == "if":
                            tokens_list.append(Token("IF", identifier))
                        elif identifier == "else":
                            tokens_list.append(Token("ELSE", identifier))
                        elif identifier == "int" or identifier == "bool":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("PLUS", "+"))

            elif(caracter == "-"):
                if operadorDuplo:
                    if operadorDuplo == "=":
                        tokens_list.append(Token("RECEBE", operadorDuplo))
                    elif operadorDuplo == "==":
                        tokens_list.append(Token("EQUAL", operadorDuplo))
                    elif operadorDuplo == "&&":
                        tokens_list.append(Token("AND", operadorDuplo))
                    elif operadorDuplo == "||":
                        tokens_list.append(Token("OR", operadorDuplo))
                    operadorDuplo = ""
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        if identifier == "println":
                            tokens_list.append(Token("PRINT", identifier))
                        elif identifier == "readln":
                            tokens_list.append(Token("READLINE", identifier))
                        elif identifier == "while":
                            tokens_list.append(Token("WHILE", identifier))
                        elif identifier == "if":
                            tokens_list.append(Token("IF", identifier))
                        elif identifier == "else":
                            tokens_list.append(Token("ELSE", identifier))
                        elif identifier == "int" or identifier == "bool":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("MINUS", "-"))

            elif(caracter == "*"):
                if operadorDuplo:
                    if operadorDuplo == "=":
                        tokens_list.append(Token("RECEBE", operadorDuplo))
                    elif operadorDuplo == "==":
                        tokens_list.append(Token("EQUAL", operadorDuplo))
                    elif operadorDuplo == "&&":
                        tokens_list.append(Token("AND", operadorDuplo))
                    elif operadorDuplo == "||":
                        tokens_list.append(Token("OR", operadorDuplo))
                    operadorDuplo = ""
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        if identifier == "println":
                            tokens_list.append(Token("PRINT", identifier))
                        elif identifier == "readln":
                            tokens_list.append(Token("READLINE", identifier))
                        elif identifier == "while":
                            tokens_list.append(Token("WHILE", identifier))
                        elif identifier == "if":
                            tokens_list.append(Token("IF", identifier))
                        elif identifier == "else":
                            tokens_list.append(Token("ELSE", identifier))
                        elif identifier == "int" or identifier == "bool":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("TIMES", "*"))

            elif(caracter == "/"):
                if operadorDuplo:
                    if operadorDuplo == "=":
                        tokens_list.append(Token("RECEBE", operadorDuplo))
                    elif operadorDuplo == "==":
                        tokens_list.append(Token("EQUAL", operadorDuplo))
                    elif operadorDuplo == "&&":
                        tokens_list.append(Token("AND", operadorDuplo))
                    elif operadorDuplo == "||":
                        tokens_list.append(Token("OR", operadorDuplo))
                    operadorDuplo = ""
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        if identifier == "println":
                            tokens_list.append(Token("PRINT", identifier))
                        elif identifier == "readln":
                            tokens_list.append(Token("READLINE", identifier))
                        elif identifier == "while":
                            tokens_list.append(Token("WHILE", identifier))
                        elif identifier == "if":
                            tokens_list.append(Token("IF", identifier))
                        elif identifier == "else":
                            tokens_list.append(Token("ELSE", identifier))
                        elif identifier == "int" or identifier == "bool":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("OVER", "/"))

            elif(caracter == "("):
                countPar += 1
                if operadorDuplo:
                    if operadorDuplo == "=":
                        tokens_list.append(Token("RECEBE", operadorDuplo))
                    elif operadorDuplo == "==":
                        tokens_list.append(Token("EQUAL", operadorDuplo))
                    elif operadorDuplo == "&&":
                        tokens_list.append(Token("AND", operadorDuplo))
                    elif operadorDuplo == "||":
                        tokens_list.append(Token("OR", operadorDuplo))
                    operadorDuplo = ""
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        if identifier == "println":
                            tokens_list.append(Token("PRINT", identifier))
                        elif identifier == "readln":
                            tokens_list.append(Token("READLINE", identifier))
                        elif identifier == "while":
                            tokens_list.append(Token("WHILE", identifier))
                        elif identifier == "if":
                            tokens_list.append(Token("IF", identifier))
                        elif identifier == "else":
                            tokens_list.append(Token("ELSE", identifier))
                        elif identifier == "int" or identifier == "bool":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("LPAR", "("))

            elif(caracter == ")"):
                countPar -= 1
                if countPar < 0:
                    raise ValueError("Desbalanceamento de parenteses!")
                if operadorDuplo:
                    if operadorDuplo == "=":
                        tokens_list.append(Token("RECEBE", operadorDuplo))
                    elif operadorDuplo == "==":
                        tokens_list.append(Token("EQUAL", operadorDuplo))
                    elif operadorDuplo == "&&":
                        tokens_list.append(Token("AND", operadorDuplo))
                    elif operadorDuplo == "||":
                        tokens_list.append(Token("OR", operadorDuplo))
                    operadorDuplo = ""
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        if identifier == "println":
                            tokens_list.append(Token("PRINT", identifier))
                        elif identifier == "readln":
                            tokens_list.append(Token("READLINE", identifier))
                        elif identifier == "while":
                            tokens_list.append(Token("WHILE", identifier))
                        elif identifier == "if":
                            tokens_list.append(Token("IF", identifier))
                        elif identifier == "else":
                            tokens_list.append(Token("ELSE", identifier))
                        elif identifier == "int" or identifier == "bool":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("RPAR", ")"))

            elif(caracter == "{"):
                countKey += 1
                if operadorDuplo:
                    if operadorDuplo == "=":
                        tokens_list.append(Token("RECEBE", operadorDuplo))
                    elif operadorDuplo == "==":
                        tokens_list.append(Token("EQUAL", operadorDuplo))
                    elif operadorDuplo == "&&":
                        tokens_list.append(Token("AND", operadorDuplo))
                    elif operadorDuplo == "||":
                        tokens_list.append(Token("OR", operadorDuplo))
                    operadorDuplo = ""
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        if identifier == "println":
                            tokens_list.append(Token("PRINT", identifier))
                        elif identifier == "readln":
                            tokens_list.append(Token("READLINE", identifier))
                        elif identifier == "while":
                            tokens_list.append(Token("WHILE", identifier))
                        elif identifier == "if":
                            tokens_list.append(Token("IF", identifier))
                        elif identifier == "else":
                            tokens_list.append(Token("ELSE", identifier))
                        elif identifier == "int" or identifier == "bool":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("LKEY", "{"))

            elif(caracter == "}"):
                countKey -= 1
                if countKey < 0:
                    raise ValueError("Desbalanceamento de chaves!")
                if operadorDuplo:
                    if operadorDuplo == "=":
                        tokens_list.append(Token("RECEBE", operadorDuplo))
                    elif operadorDuplo == "==":
                        tokens_list.append(Token("EQUAL", operadorDuplo))
                    elif operadorDuplo == "&&":
                        tokens_list.append(Token("AND", operadorDuplo))
                    elif operadorDuplo == "||":
                        tokens_list.append(Token("OR", operadorDuplo))
                    operadorDuplo = ""
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        if identifier == "println":
                            tokens_list.append(Token("PRINT", identifier))
                        elif identifier == "readln":
                            tokens_list.append(Token("READLINE", identifier))
                        elif identifier == "while":
                            tokens_list.append(Token("WHILE", identifier))
                        elif identifier == "if":
                            tokens_list.append(Token("IF", identifier))
                        elif identifier == "else":
                            tokens_list.append(Token("ELSE", identifier))
                        elif identifier == "int" or identifier == "bool":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("RKEY", "}"))

            elif(caracter == ";"):
                if operadorDuplo:
                    if operadorDuplo == "=":
                        tokens_list.append(Token("RECEBE", operadorDuplo))
                    elif operadorDuplo == "==":
                        tokens_list.append(Token("EQUAL", operadorDuplo))
                    elif operadorDuplo == "&&":
                        tokens_list.append(Token("AND", operadorDuplo))
                    elif operadorDuplo == "||":
                        tokens_list.append(Token("OR", operadorDuplo))
                    operadorDuplo = ""
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        if identifier == "println":
                            tokens_list.append(Token("PRINT", identifier))
                        elif identifier == "readln":
                            tokens_list.append(Token("READLINE", identifier))
                        elif identifier == "while":
                            tokens_list.append(Token("WHILE", identifier))
                        elif identifier == "if":
                            tokens_list.append(Token("IF", identifier))
                        elif identifier == "else":
                            tokens_list.append(Token("ELSE", identifier))
                        elif identifier == "int" or identifier == "bool":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("ENDLINE", ";"))

            elif(caracter == ">"):
                if operadorDuplo:
                    if operadorDuplo == "=":
                        tokens_list.append(Token("RECEBE", operadorDuplo))
                    elif operadorDuplo == "==":
                        tokens_list.append(Token("EQUAL", operadorDuplo))
                    elif operadorDuplo == "&&":
                        tokens_list.append(Token("AND", operadorDuplo))
                    elif operadorDuplo == "||":
                        tokens_list.append(Token("OR", operadorDuplo))
                    operadorDuplo = ""
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        if identifier == "println":
                            tokens_list.append(Token("PRINT", identifier))
                        elif identifier == "readln":
                            tokens_list.append(Token("READLINE", identifier))
                        elif identifier == "while":
                            tokens_list.append(Token("WHILE", identifier))
                        elif identifier == "if":
                            tokens_list.append(Token("IF", identifier))
                        elif identifier == "else":
                            tokens_list.append(Token("ELSE", identifier))
                        elif identifier == "int" or identifier == "bool":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("MAIOR", ">"))

            elif(caracter == "<"):
                if operadorDuplo:
                    if operadorDuplo == "=":
                        tokens_list.append(Token("RECEBE", operadorDuplo))
                    elif operadorDuplo == "==":
                        tokens_list.append(Token("EQUAL", operadorDuplo))
                    elif operadorDuplo == "&&":
                        tokens_list.append(Token("AND", operadorDuplo))
                    elif operadorDuplo == "||":
                        tokens_list.append(Token("OR", operadorDuplo))
                    operadorDuplo = ""
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        if identifier == "println":
                            tokens_list.append(Token("PRINT", identifier))
                        elif identifier == "readln":
                            tokens_list.append(Token("READLINE", identifier))
                        elif identifier == "while":
                            tokens_list.append(Token("WHILE", identifier))
                        elif identifier == "if":
                            tokens_list.append(Token("IF", identifier))
                        elif identifier == "else":
                            tokens_list.append(Token("ELSE", identifier))
                        elif identifier == "int" or identifier == "bool":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("MENOR", "<"))

            elif(caracter == "!"):
                if operadorDuplo:
                    if operadorDuplo == "=":
                        tokens_list.append(Token("RECEBE", operadorDuplo))
                    elif operadorDuplo == "==":
                        tokens_list.append(Token("EQUAL", operadorDuplo))
                    elif operadorDuplo == "&&":
                        tokens_list.append(Token("AND", operadorDuplo))
                    elif operadorDuplo == "||":
                        tokens_list.append(Token("OR", operadorDuplo))
                    operadorDuplo = ""
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        if identifier == "println":
                            tokens_list.append(Token("PRINT", identifier))
                        elif identifier == "readln":
                            tokens_list.append(Token("READLINE", identifier))
                        elif identifier == "while":
                            tokens_list.append(Token("WHILE", identifier))
                        elif identifier == "if":
                            tokens_list.append(Token("IF", identifier))
                        elif identifier == "else":
                            tokens_list.append(Token("ELSE", identifier))
                        elif identifier == "int" or identifier == "bool":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("NOT", "!"))

            elif(caracter == "#"):
                if countPar != 0:
                    raise ValueError("Desbalanceamento de parenteses!")
                if countKey != 0:
                    raise ValueError("Desbalanceamento de chaves!")
                if operadorDuplo:
                    if operadorDuplo == "=":
                        tokens_list.append(Token("RECEBE", operadorDuplo))
                    elif operadorDuplo == "==":
                        tokens_list.append(Token("EQUAL", operadorDuplo))
                    elif operadorDuplo == "&&":
                        tokens_list.append(Token("AND", operadorDuplo))
                    elif operadorDuplo == "||":
                        tokens_list.append(Token("OR", operadorDuplo))
                    operadorDuplo = ""
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        if identifier == "println":
                            tokens_list.append(Token("PRINT", identifier))
                        elif identifier == "readln":
                            tokens_list.append(Token("READLINE", identifier))
                        elif identifier == "while":
                            tokens_list.append(Token("WHILE", identifier))
                        elif identifier == "if":
                            tokens_list.append(Token("IF", identifier))
                        elif identifier == "else":
                            tokens_list.append(Token("ELSE", identifier))
                        elif identifier == "int" or identifier == "bool":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("EOF", "#"))
                break

            elif(caracter == "\n" or caracter == "\t"):
                continue

            elif(caracter in operadoresDuplos):
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        if identifier == "println":
                            tokens_list.append(Token("PRINT", identifier))
                        elif identifier == "readln":
                            tokens_list.append(Token("READLINE", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                operadorDuplo += caracter

            else:
                identifier += caracter
        # for e in tokens_list:
        #     print(e.value)
        return tokens_list


class Parser:
    def __init__(self):
        self.tokens = None

    @staticmethod
    def parseBlock():
        if(Parser.tokens.actual.type == "LKEY"):
            Parser.tokens.selectNext()
            commandList = []
            while(Parser.tokens.actual.type != "RKEY" and Parser.tokens.actual.type != "EOF"):
                order = Parser.parseCommand()
                commandList.append(order)
            statements = NodeBlock("STAT", commandList)
            return statements
        else:
            raise ValueError("Expecting LKEY!")

    @staticmethod
    def parseCommand():
        order = NoOp(None)
        if(Parser.tokens.actual.type == "TIPO"):
            tipo = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "IDENT"):
                variavel = Parser.tokens.actual.value
                order = Atribuicao("ISTYPE", [variavel, tipo])
                Parser.tokens.selectNext()
                if(Parser.tokens.actual.type == "ENDLINE"):
                    Parser.tokens.selectNext()
                    return order
                else:
                    raise ValueError("Expecting PONTO VIRGULA!")
            else:
                raise ValueError("Expecting a variable!")
        elif(Parser.tokens.actual.type == "IDENT"):
            variavel = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "RECEBE"):
                Parser.tokens.selectNext()
                orexp = Parser.parseOrexpr()
                order = Atribuicao("RECEBE", [variavel, orexp])
                if(Parser.tokens.actual.type == "ENDLINE"):
                    Parser.tokens.selectNext()
                    return order
                else:
                    raise ValueError("Expecting PONTO VIRGULA!")
            else:
                raise ValueError("Expecting an RECEBE!")
        elif(Parser.tokens.actual.type == "PRINT"):
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "LPAR"):
                Parser.tokens.selectNext()
                orexp = Parser.parseOrexpr()
                if(Parser.tokens.actual.type == "RPAR"):
                    Parser.tokens.selectNext()
                    order = Println("PRINT", [orexp])
                    if(Parser.tokens.actual.type == "ENDLINE"):
                        Parser.tokens.selectNext()
                        return order
                    else:
                        raise ValueError("Expecting PONTO VIRGULA!")
                else:
                    raise ValueError("Expecting a RPAR!")
            else:
                raise ValueError("Expecting an LPAR!")
        elif(Parser.tokens.actual.type == "WHILE"):
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "LPAR"):
                Parser.tokens.selectNext()
                condition = Parser.parseOrexpr()
                if(Parser.tokens.actual.type == "RPAR"):
                    Parser.tokens.selectNext()
                    command = Parser.parseCommand()
                    order = While("WHILE", [condition, command])
                    return order
                else:
                    raise ValueError("Expecting a RPAR!")
            else:
                raise ValueError("Expecting an LPAR!")
        elif(Parser.tokens.actual.type == "IF"):
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "LPAR"):
                Parser.tokens.selectNext()
                condition = Parser.parseOrexpr()
                if(Parser.tokens.actual.type == "RPAR"):
                    Parser.tokens.selectNext()
                    command = Parser.parseCommand()
                    if(Parser.tokens.actual.type == "ELSE"):
                        Parser.tokens.selectNext()
                        commandElse = Parser.parseCommand()
                    else:
                        commandElse = NoOp(None)
                    order = If("IF", [condition, command, commandElse])
                    return order
                else:
                    raise ValueError("Expecting a RPAR!")
            else:
                raise ValueError("Expecting an LPAR!")
        else:
            if not Parser.tokens.actual.type == "ENDLINE":
                order = Parser.parseBlock()
            Parser.tokens.selectNext()
            return order

    @staticmethod
    def parseOrexpr():
        operadores = ["OR"]

        resultAndexpr = Parser.parseAndexpr()

        while(Parser.tokens.actual.type in operadores):
            if(Parser.tokens.actual.type == "OR"):
                Parser.tokens.selectNext()
                resultAndexpr = BinOp(
                    "OR", [resultAndexpr, Parser.parseAndexpr()])

        if Parser.tokens.actual.type == "ENDLINE" or Parser.tokens.actual.type == "RPAR":
            return resultAndexpr
        else:
            raise ValueError

    @staticmethod
    def parseAndexpr():
        operadores = ["AND"]

        resultEqexpr = Parser.parseEqexpr()

        while(Parser.tokens.actual.type in operadores):
            if(Parser.tokens.actual.type == "AND"):
                Parser.tokens.selectNext()
                resultEqexpr = BinOp(
                    "AND", [resultEqexpr, Parser.parseEqexpr()])

        return resultEqexpr

    @staticmethod
    def parseEqexpr():
        operadores = ["EQUAL"]

        resultRelexpr = Parser.parseRelexpr()

        while(Parser.tokens.actual.type in operadores):
            if(Parser.tokens.actual.type == "EQUAL"):
                Parser.tokens.selectNext()
                resultRelexpr = BinOp(
                    "EQUAL", [resultRelexpr, Parser.parseRelexpr()])

        return resultRelexpr

    @staticmethod
    def parseRelexpr():
        operadores = ["MAIOR", "MENOR"]

        resultExpression = Parser.parseExpression()

        while(Parser.tokens.actual.type in operadores):
            if(Parser.tokens.actual.type == "MAIOR"):
                Parser.tokens.selectNext()
                resultExpression = BinOp(
                    "MAIOR", [resultExpression, Parser.parseExpression()])

            elif(Parser.tokens.actual.type == "MENOR"):
                Parser.tokens.selectNext()
                resultExpression = BinOp(
                    "MENOR", [resultExpression, Parser.parseExpression()])

        return resultExpression

    @staticmethod
    def parseExpression():
        operadores = ["PLUS", "MINUS"]

        resultTerm = Parser.parseTerm()

        while(Parser.tokens.actual.type in operadores):
            if(Parser.tokens.actual.type == "PLUS"):
                Parser.tokens.selectNext()
                resultTerm = BinOp("PLUS", [resultTerm, Parser.parseTerm()])

            elif(Parser.tokens.actual.type == "MINUS"):
                Parser.tokens.selectNext()
                resultTerm = BinOp("MINUS", [resultTerm, Parser.parseTerm()])

        return resultTerm

    @staticmethod
    def parseTerm():
        operadores = ["TIMES", "OVER"]

        resultFactor = Parser.parseFactor()

        while(Parser.tokens.actual.type in operadores):
            if(Parser.tokens.actual.type == "TIMES"):
                Parser.tokens.selectNext()
                resultFactor = BinOp(
                    "TIMES", [resultFactor, Parser.parseFactor()])

            elif(Parser.tokens.actual.type == "OVER"):
                Parser.tokens.selectNext()
                resultFactor = BinOp(
                    "OVER", [resultFactor, Parser.parseFactor()])

        return resultFactor

    @staticmethod
    def parseFactor():
        if(Parser.tokens.actual.type == "INT"):
            resultFactor = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            return IntVal(resultFactor)
        if(Parser.tokens.actual.type == "BOOL"):
            resultFactor = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            return BoolVal(resultFactor)
        elif(Parser.tokens.actual.type == "PLUS"):
            Parser.tokens.selectNext()
            return UnOp("PLUS", [Parser.parseFactor()])
        elif(Parser.tokens.actual.type == "MINUS"):
            Parser.tokens.selectNext()
            return UnOp("MINUS", [Parser.parseFactor()])
        elif(Parser.tokens.actual.type == "NOT"):
            Parser.tokens.selectNext()
            return UnOp("NOT", [Parser.parseFactor()])
        elif(Parser.tokens.actual.type == "LPAR"):
            Parser.tokens.selectNext()
            expression = Parser.parseOrexpr()
            if(Parser.tokens.actual.type == "RPAR"):
                Parser.tokens.selectNext()
                return expression
            else:
                raise ValueError
        elif(Parser.tokens.actual.type == "IDENT"):
            resultFactor = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            return Identific(resultFactor)
        elif(Parser.tokens.actual.type == "READLINE"):
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "LPAR"):
                Parser.tokens.selectNext()
                if(Parser.tokens.actual.type == "RPAR"):
                    Parser.tokens.selectNext()
                    return Readln("READLINE")
                else:
                    raise ValueError("Missing RPAR in READLN!")
            else:
                raise ValueError("Missing LPAR in READLN!")
        else:
            raise ValueError

    @staticmethod
    def run(origin):
        Parser.tokens = Tokenizer(PrePro.filter(origin))
        statements = Parser.parseBlock()
        statements.Evaluate()


class PrePro:
    @staticmethod
    def filter(arg):
        new_arg = re.sub(r"\/\*.*?\*\/", " ", arg)
        return new_arg


class SymbolTable:
    # GETTER
    @staticmethod
    def getter(key):
        return dictGlobal[key][0]

    # SETTER TYPE
    @staticmethod
    def setterType(key, value=None, type_=None):
        dictGlobal[key] = [value, type_]

    # SETTER VALUE
    @staticmethod
    def setterValue(key, value):
        if dictGlobal[key][1] == "bool":
            dictGlobal[key][0] = int(bool(value))
        elif dictGlobal[key][1] == "int":
            dictGlobal[key][0] = int(value)


if __name__ == "__main__":
    # Parser.run("{println(2);}")
    # print(dictGlobal)
    with open("./teste000.c", "r") as f:
    # with open(sys.argv[1], "r") as f:
        Parser.run(f.read())
        # print(dictGlobal)
