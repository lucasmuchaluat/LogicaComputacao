import sys
import re

funcGlobal = {}


class Node:
    def __init__(self, valorNode, nodeList=[]):
        self.value = valorNode
        self.children = nodeList

    def Evaluate(self):
        pass


class BinOp(Node):
    def Evaluate(self, symbolTable):
        child1 = self.children[0].Evaluate(symbolTable)
        child2 = self.children[1].Evaluate(symbolTable)

        if self.value == "EQUAL":
            valorOp = bool(child1 == child2)
        elif isinstance(child1, str) or isinstance(child2, str):
            raise ValueError("ERROR: Incompatible types!")
        elif self.value == "PLUS":
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
        elif self.value == "AND":
            valorOp = bool(child1 and child2)
        elif self.value == "OR":
            valorOp = bool(child1 or child2)
        else:
            raise ValueError("BinOp operation error")

        return int(valorOp)


class Atribuicao(Node):
    def Evaluate(self, symbolTable):
        child1 = self.children[0]

        if self.value == "ISTYPE":
            child2 = self.children[1]
            if child1 not in symbolTable.keys():
                SymbolTable.setterType(symbolTable, child1, type_=child2)
            else:
                raise ValueError("Variavel already exists!")

        if self.value == "RECEBE":
            child2 = self.children[1].Evaluate(symbolTable)
            SymbolTable.setterValue(symbolTable, child1, child2)


class UnOp(Node):
    def Evaluate(self, symbolTable):
        child1 = self.children[0].Evaluate(symbolTable)

        if self.value == "PLUS":
            valorOp = child1
        elif self.value == "MINUS":
            valorOp = -child1
        elif self.value == "NOT":
            valorOp = not child1

        return int(valorOp)


class IntVal(Node):
    def Evaluate(self, symbolTable):
        valorInteiro = self.value
        return(valorInteiro)


class BoolVal(Node):
    def Evaluate(self, symbolTable):
        valorBooleano = self.value
        return(int(valorBooleano == "true"))


class StringVal(Node):
    def Evaluate(self, symbolTable):
        valorString = self.value
        return(valorString)


class Identific(Node):
    def Evaluate(self, symbolTable):
        valorVariavel = SymbolTable.getter(symbolTable, self.value)[0]
        return(valorVariavel)


class NoOp(Node):
    def Evaluate(self, symbolTable):
        return


class Println(Node):
    def Evaluate(self, symbolTable):
        child1 = self.children[0].Evaluate(symbolTable)
        print(child1)


class Readln(Node):
    def Evaluate(self, symbolTable):
        valorInputado = input()
        return int(valorInputado)


class NodeBlock(Node):
    def Evaluate(self, symbolTable):
        for child in self.children:
            child.Evaluate(symbolTable)
            try:
                value = SymbolTable.getter(symbolTable, "return")[0]
                break
            except:
                pass


class While(Node):
    def Evaluate(self, symbolTable):
        while self.children[0].Evaluate(symbolTable):
            self.children[1].Evaluate(symbolTable)


class If(Node):
    def Evaluate(self, symbolTable):
        if self.children[0].Evaluate(symbolTable):
            self.children[1].Evaluate(symbolTable)
        else:
            self.children[2].Evaluate(symbolTable)


class AllFunctions(Node):
    def Evaluate(self, symbolTable):
        for func in self.children:
            func.Evaluate(symbolTable)
        return FuncCall("main").Evaluate(symbolTable)


class FuncDec(Node):
    def Evaluate(self, symbolTable):
        funcType = self.children[0]
        funcName = self.children[1]
        fungArgs = self.children[2]
        funcBody = self.children[3]
        if funcName not in funcGlobal.keys():
            FuncTable.setter(key=funcName, args=fungArgs,
                             type_=funcType, body=funcBody)
        else:
            raise ValueError(
                "Erro: ja foi declarada funcao com este identificador")


class FuncCall(Node):
    def Evaluate(self, symbolTable):
        funcName = self.value
        funcTable = {}
        args, type_, body = FuncTable.getter(funcName)
        if(len(args) != len(self.children)):
            raise ValueError(
                "Argumentos não batem com os passados como parametro!")
        else:
            for i in range(len(self.children)):
                value = self.children[i].Evaluate(symbolTable)
                try:
                    valueType = SymbolTable.getter(
                        symbolTable, self.children[i].value)[1]
                except:
                    valueType = type(value).__name__
                if(args[i][0] != valueType):
                    raise ValueError(
                        "Tipos dos parametros passados não batem com os argumentos da funcao!")
                SymbolTable.setterType(funcTable, args[i][1], type_=args[i][0])
                SymbolTable.setterValue(funcTable, args[i][1], value)
            body.Evaluate(funcTable)
            returnValue = SymbolTable.getter(funcTable, "return")[0]
            returnType = SymbolTable.getter(funcTable, "return")[1]
            if returnType != type_:
                raise ValueError("Error: tipo de retorno")
            if(type_ == "int"):
                return int(returnValue)
            elif(type_ == "bool"):
                return bool(int(returnValue == "True"))
            elif(type_ == "string"):
                return str(returnValue)


class Return(Node):
    def Evaluate(self, symbolTable):
        child1 = self.children[0].Evaluate(symbolTable)
        returnType = type(child1).__name__
        SymbolTable.setterType(symbolTable, "return", type_=returnType)
        SymbolTable.setterValue(symbolTable, "return", child1)


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

    @ staticmethod
    def montador(origin):
        tokens_list = []
        numero = ""
        identifier = ""
        operadorDuplo = ""
        origin += "#"
        countPar = 0
        countKey = 0
        isString = 0
        stringText = ""
        palavrasReservadas = ["println", "readln",
                              "while", "if", "else", "int", "bool", "string", "true", "false", "return"]
        operadoresDuplos = ["=", "&", "|"]

        for caracter in origin:
            if identifier:
                if identifier[0] == "_":
                    raise ValueError("Variavel Não pode começar com _!")

            if(caracter.isdigit() and identifier == "" and stringText == ""):
                numero += caracter

            elif(caracter == " " and isString == 0):
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
                        elif identifier == "int" or identifier == "bool" or identifier == "string":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                        elif identifier == "return":
                            tokens_list.append(Token("RETURN", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""

            elif(caracter == "+" and isString == 0):
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
                        elif identifier == "int" or identifier == "bool" or identifier == "string":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                        elif identifier == "return":
                            tokens_list.append(Token("RETURN", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("PLUS", "+"))

            elif(caracter == "-" and isString == 0):
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
                        elif identifier == "int" or identifier == "bool" or identifier == "string":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                        elif identifier == "return":
                            tokens_list.append(Token("RETURN", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("MINUS", "-"))

            elif(caracter == "*" and isString == 0):
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
                        elif identifier == "int" or identifier == "bool" or identifier == "string":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                        elif identifier == "return":
                            tokens_list.append(Token("RETURN", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("TIMES", "*"))

            elif(caracter == "/" and isString == 0):
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
                        elif identifier == "int" or identifier == "bool" or identifier == "string":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                        elif identifier == "return":
                            tokens_list.append(Token("RETURN", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("OVER", "/"))

            elif(caracter == "(" and isString == 0):
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
                        elif identifier == "int" or identifier == "bool" or identifier == "string":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                        elif identifier == "return":
                            tokens_list.append(Token("RETURN", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("LPAR", "("))

            elif(caracter == ")" and isString == 0):
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
                        elif identifier == "int" or identifier == "bool" or identifier == "string":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                        elif identifier == "return":
                            tokens_list.append(Token("RETURN", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("RPAR", ")"))

            elif(caracter == "{" and isString == 0):
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
                        elif identifier == "int" or identifier == "bool" or identifier == "string":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                        elif identifier == "return":
                            tokens_list.append(Token("RETURN", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("LKEY", "{"))

            elif(caracter == "}" and isString == 0):
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
                        elif identifier == "int" or identifier == "bool" or identifier == "string":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                        elif identifier == "return":
                            tokens_list.append(Token("RETURN", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("RKEY", "}"))

            elif(caracter == ";" and isString == 0):
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
                        elif identifier == "int" or identifier == "bool" or identifier == "string":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                        elif identifier == "return":
                            tokens_list.append(Token("RETURN", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("ENDLINE", ";"))

            elif(caracter == ">" and isString == 0):
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
                        elif identifier == "int" or identifier == "bool" or identifier == "string":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                        elif identifier == "return":
                            tokens_list.append(Token("RETURN", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("MAIOR", ">"))

            elif(caracter == "<" and isString == 0):
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
                        elif identifier == "int" or identifier == "bool" or identifier == "string":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                        elif identifier == "return":
                            tokens_list.append(Token("RETURN", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("MENOR", "<"))

            elif(caracter == "!" and isString == 0):
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
                        elif identifier == "int" or identifier == "bool" or identifier == "string":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                        elif identifier == "return":
                            tokens_list.append(Token("RETURN", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("NOT", "!"))

            elif(caracter == "," and isString == 0):
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
                        elif identifier == "int" or identifier == "bool" or identifier == "string":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                        elif identifier == "return":
                            tokens_list.append(Token("RETURN", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("VIRGULA", ","))

            elif(caracter == "#" and isString == 0):
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
                        elif identifier == "int" or identifier == "bool" or identifier == "string":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                        elif identifier == "return":
                            tokens_list.append(Token("RETURN", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("EOF", "#"))
                break

            elif(caracter == "\n" or caracter == "\t" and isString == 0):
                continue

            elif(caracter in operadoresDuplos and isString == 0):
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
                        elif identifier == "int" or identifier == "bool" or identifier == "string":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                        elif identifier == "return":
                            tokens_list.append(Token("RETURN", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                operadorDuplo += caracter
            elif(caracter == '"'):
                if isString:
                    isString -= 1
                    tokens_list.append(Token("STRING", stringText))
                    stringText = ""
                else:
                    isString += 1
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
                        elif identifier == "int" or identifier == "bool" or identifier == "string":
                            tokens_list.append(Token("TIPO", identifier))
                        elif identifier == "true" or identifier == "false":
                            tokens_list.append(Token("BOOL", identifier))
                        elif identifier == "return":
                            tokens_list.append(Token("RETURN", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("ASPAS", '"'))
            else:
                if isString:
                    stringText += caracter
                else:
                    identifier += caracter
        # for e in tokens_list:
        #     print(e.type)
        return tokens_list


class Parser:
    def __init__(self):
        self.tokens = None

    @ staticmethod
    def parseFunctions():
        functions = []
        while(Parser.tokens.actual.type == "TIPO"):
            functions.append(Parser.parseFuncDefBlock())

        return AllFunctions("Functions", functions)

    @ staticmethod
    def parseFuncDefBlock():
        funcScript = NoOp(None)
        if(Parser.tokens.actual.type == "TIPO"):
            funcTipo = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "IDENT"):
                funcName = Parser.tokens.actual.value
                vardecChildren = [funcTipo, funcName]
                Parser.tokens.selectNext()
                if(Parser.tokens.actual.type == "LPAR"):
                    Parser.tokens.selectNext()
                    argumentos = []
                    while(Parser.tokens.actual.type != "RPAR"):
                        if(Parser.tokens.actual.type == "TIPO"):
                            tipoVariavel = Parser.tokens.actual.value
                            Parser.tokens.selectNext()
                            if(Parser.tokens.actual.type == "IDENT"):
                                nomeVariavel = Parser.tokens.actual.value
                                argumentos.append([tipoVariavel, nomeVariavel])
                                Parser.tokens.selectNext()
                                if(Parser.tokens.actual.type == "RPAR"):
                                    break
                                if(Parser.tokens.actual.type == "VIRGULA"):
                                    Parser.tokens.selectNext()
                                    if(Parser.tokens.actual.type == "RPAR"):
                                        raise ValueError(
                                            "Erro: virgula sem novo parametro")
                                else:
                                    raise ValueError(
                                        "Expecting virgula between parameters!")
                            else:
                                raise ValueError(
                                    "Expecting parameter name after type!")
                        else:
                            raise ValueError(
                                "Expecting type before passing parameter!")
                    vardecChildren.append(argumentos)
                    Parser.tokens.selectNext()
                    funcBody = Parser.parseCommand()
                    vardecChildren.append(funcBody)
                    funcScript = FuncDec("FUNCTION", vardecChildren)
                else:
                    raise ValueError("Expecting LPAR before parameters!")
            else:
                raise ValueError("Expecting function name!")
        return funcScript

    @ staticmethod
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

    @ staticmethod
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
            nome = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "RECEBE"):
                Parser.tokens.selectNext()
                orexp = Parser.parseOrexpr()
                order = Atribuicao("RECEBE", [nome, orexp])
                if(Parser.tokens.actual.type == "ENDLINE"):
                    Parser.tokens.selectNext()
                    return order
                else:
                    raise ValueError("Expecting PONTO VIRGULA!")
            elif(Parser.tokens.actual.type == "LPAR"):
                Parser.tokens.selectNext()
                parameters = []
                while(Parser.tokens.actual.type != "RPAR"):
                    parameters.append(Parser.parseOrexpr())
                    if(Parser.tokens.actual.type == "VIRGULA"):
                        Parser.tokens.selectNext()
                order = FuncCall(nome, parameters)
                Parser.tokens.selectNext()
                if(Parser.tokens.actual.type == "ENDLINE"):
                    Parser.tokens.selectNext()
                    return order
            else:
                raise ValueError("Expecting um RECEBE ou LPAR!")
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
        elif(Parser.tokens.actual.type == "RETURN"):
            Parser.tokens.selectNext()
            orexp = Parser.parseOrexpr()
            order = Return("RETURN", [orexp])
            if(Parser.tokens.actual.type == "ENDLINE"):
                Parser.tokens.selectNext()
                return order
            else:
                raise ValueError("Expecting PONTO VIRGULA!")
        elif(Parser.tokens.actual.type == "WHILE"):
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "LPAR"):
                Parser.tokens.selectNext()
                condition = Parser.parseOrexpr()
                if isinstance(condition, StringVal):
                    raise ValueError("Condition must not be a string!")
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
                if isinstance(condition, StringVal):
                    raise ValueError("Condition must not be a string!")
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

    @ staticmethod
    def parseOrexpr():
        operadores = ["OR"]

        resultAndexpr = Parser.parseAndexpr()

        while(Parser.tokens.actual.type in operadores):
            if(Parser.tokens.actual.type == "OR"):
                Parser.tokens.selectNext()
                resultAndexpr = BinOp(
                    "OR", [resultAndexpr, Parser.parseAndexpr()])

        if Parser.tokens.actual.type == "ENDLINE" or Parser.tokens.actual.type == "RPAR" or Parser.tokens.actual.type == "VIRGULA":
            return resultAndexpr
        else:
            raise ValueError

    @ staticmethod
    def parseAndexpr():
        operadores = ["AND"]

        resultEqexpr = Parser.parseEqexpr()

        while(Parser.tokens.actual.type in operadores):
            if(Parser.tokens.actual.type == "AND"):
                Parser.tokens.selectNext()
                resultEqexpr = BinOp(
                    "AND", [resultEqexpr, Parser.parseEqexpr()])

        return resultEqexpr

    @ staticmethod
    def parseEqexpr():
        operadores = ["EQUAL"]

        resultRelexpr = Parser.parseRelexpr()

        while(Parser.tokens.actual.type in operadores):
            if(Parser.tokens.actual.type == "EQUAL"):
                Parser.tokens.selectNext()
                resultRelexpr = BinOp(
                    "EQUAL", [resultRelexpr, Parser.parseRelexpr()])

        return resultRelexpr

    @ staticmethod
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

    @ staticmethod
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

    @ staticmethod
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

    @ staticmethod
    def parseFactor():
        if(Parser.tokens.actual.type == "INT"):
            resultFactor = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            return IntVal(resultFactor)
        elif(Parser.tokens.actual.type == "BOOL"):
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
            if(Parser.tokens.actual.type == "LPAR"):
                Parser.tokens.selectNext()
                parameters = []
                while(Parser.tokens.actual.type != "RPAR"):
                    parameters.append(Parser.parseOrexpr())
                    if(Parser.tokens.actual.type == "RPAR"):
                        break
                    if(Parser.tokens.actual.type == "VIRGULA"):
                        Parser.tokens.selectNext()
                order = FuncCall(resultFactor, parameters)
                Parser.tokens.selectNext()
                return order
            else:
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
        elif(Parser.tokens.actual.type == "ASPAS"):
            Parser.tokens.selectNext()
            resultFactor = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "ASPAS"):
                Parser.tokens.selectNext()
                return StringVal(resultFactor)
            else:
                raise ValueError('Expecting closing "!')
        else:
            raise ValueError

    @ staticmethod
    def run(origin):
        Parser.tokens = Tokenizer(PrePro.filter(origin))
        functions = Parser.parseFunctions()
        dictTeste = {}
        functions.Evaluate(dictTeste)


class PrePro:
    @ staticmethod
    def filter(arg):
        new_arg = re.sub(r"\/\*.*?\*\/", " ", arg)
        return new_arg


class SymbolTable:
    # GETTER
    @ staticmethod
    def getter(dictTable, key):
        return dictTable[key]

    # SETTER TYPE
    @ staticmethod
    def setterType(dictTable, key, value=None, type_=None):
        dictTable[key] = [value, type_]

    # SETTER VALUE
    @ staticmethod
    def setterValue(dictTable, key, value):
        if dictTable[key][1] == "bool":
            dictTable[key][0] = int(bool(value))
        elif dictTable[key][1] == "int":
            dictTable[key][0] = int(value)
        elif dictTable[key][1] == "string":
            dictTable[key][0] = value


class FuncTable:
    # GETTER
    @ staticmethod
    def getter(key):
        return funcGlobal[key]

    # SETTER
    @ staticmethod
    def setter(key, args=None, type_=None, body=None):
        funcGlobal[key] = [args, type_, body]


if __name__ == "__main__":
    # with open("./teste000.c", "r") as f:
    with open(sys.argv[1], "r") as f:
        Parser.run(f.read())
