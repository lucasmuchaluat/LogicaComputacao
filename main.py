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
        else:
            raise ValueError("BinOp operation error")

        return int(valorOp)


class Atribuicao(Node):
    def Evaluate(self):
        child1 = self.children[0]
        child2 = self.children[1].Evaluate()

        if self.value == "EQUAL":
            SymbolTable.setter(child1, child2)


class UnOp(Node):
    def Evaluate(self):
        child1 = self.children[0].Evaluate()

        if self.value == "PLUS":
            valorOp = child1
        elif self.value == "MINUS":
            valorOp = -child1

        return int(valorOp)


class IntVal(Node):
    def Evaluate(self):
        valorInteiro = self.value
        return(valorInteiro)


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
        origin += "#"
        countPar = 0
        palavrasReservadas = ["println"]

        for caracter in origin:
            if identifier:
                if identifier[0] == "_":
                    raise ValueError("Variavel Não pode começar com _!")

            if(caracter.isdigit() and identifier == ""):
                numero += caracter

            elif(caracter == " "):
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        tokens_list.append(Token("PRINT", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""

            elif(caracter == "+"):
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        tokens_list.append(Token("PRINT", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("PLUS", "+"))

            elif(caracter == "-"):
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        tokens_list.append(Token("PRINT", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("MINUS", "-"))

            elif(caracter == "*"):
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        tokens_list.append(Token("PRINT", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("TIMES", "*"))

            elif(caracter == "/"):
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        tokens_list.append(Token("PRINT", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("OVER", "/"))

            elif(caracter == "("):
                countPar += 1
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        tokens_list.append(Token("PRINT", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("LPAR", "("))

            elif(caracter == ")"):
                countPar -= 1
                if countPar < 0:
                    raise ValueError("Desbalanceamento de parenteses!")
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        tokens_list.append(Token("PRINT", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("RPAR", ")"))

            elif(caracter == ";"):
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        tokens_list.append(Token("PRINT", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("ENDLINE", ";"))

            elif(caracter == "="):
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        tokens_list.append(Token("PRINT", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("EQUAL", "="))

            elif(caracter == "#"):
                if countPar != 0:
                    raise ValueError("Desbalanceamento de parenteses!")
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                if identifier:
                    if identifier in palavrasReservadas:
                        tokens_list.append(Token("PRINT", identifier))
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("EOF", "#"))
                break

            elif(caracter == "\n"):
                continue
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
        commandList = []
        while(Parser.tokens.actual.type != "EOF"):
            order = Parser.parseCommand()
            commandList.append(order)
            Parser.tokens.selectNext()
        return commandList

    @staticmethod
    def parseCommand():
        command = NoOp(None)
        if(Parser.tokens.actual.type == "IDENT"):
            variavel = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "EQUAL"):
                Parser.tokens.selectNext()
                exp = Parser.parseExpression()
                command = Atribuicao("EQUAL", [variavel, exp])
            else:
                raise ValueError("Expecting an EQUAL!")
        elif(Parser.tokens.actual.type == "PRINT"):
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == "LPAR"):
                Parser.tokens.selectNext()
                exp = Parser.parseExpression()
                if(Parser.tokens.actual.type == "RPAR"):
                    Parser.tokens.selectNext()
                    command = Println("PRINT", [exp])
                else:
                    raise ValueError("Expecting a RPAR!")
            else:
                raise ValueError("Expecting an LPAR!")
        if(Parser.tokens.actual.type == "ENDLINE"):
            return command
        else:
            raise ValueError("Expecting PONTO VIRGULA!")

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

            else:
                raise ValueError

        if Parser.tokens.actual.type == "ENDLINE" or Parser.tokens.actual.type == "RPAR":
            return resultTerm
        else:
            raise ValueError

    @staticmethod
    def parseTerm():
        operadores = ["TIMES", "OVER"]

        resultFactor = Parser.parseFactor()
        Parser.tokens.selectNext()

        while(Parser.tokens.actual.type in operadores):
            if(Parser.tokens.actual.type == "TIMES"):
                Parser.tokens.selectNext()
                resultFactor = BinOp(
                    "TIMES", [resultFactor, Parser.parseFactor()])

            elif(Parser.tokens.actual.type == "OVER"):
                Parser.tokens.selectNext()
                resultFactor = BinOp(
                    "OVER", [resultFactor, Parser.parseFactor()])

            Parser.tokens.selectNext()

        return resultFactor

    @staticmethod
    def parseFactor():
        if(Parser.tokens.actual.type == "INT"):
            resultFactor = Parser.tokens.actual.value
            return IntVal(resultFactor)
        elif(Parser.tokens.actual.type == "PLUS"):
            Parser.tokens.selectNext()
            return UnOp("PLUS", [Parser.parseFactor()])
        elif(Parser.tokens.actual.type == "MINUS"):
            Parser.tokens.selectNext()
            return UnOp("MINUS", [Parser.parseFactor()])
        elif(Parser.tokens.actual.type == "LPAR"):
            Parser.tokens.selectNext()
            expression = Parser.parseExpression()
            if(Parser.tokens.actual.type == "RPAR"):
                return expression
            else:
                raise ValueError
        elif(Parser.tokens.actual.type == "IDENT"):
            resultFactor = Parser.tokens.actual.value
            return Identific(resultFactor)
        else:
            raise ValueError

    @staticmethod
    def run(origin):
        Parser.tokens = Tokenizer(PrePro.filter(origin))
        commandList = Parser.parseBlock()
        for instruction in commandList:
            instruction.Evaluate()


class PrePro:
    @staticmethod
    def filter(arg):
        new_arg = re.sub(r"\/\*.*?\*\/", " ", arg)
        return new_arg


class SymbolTable:
    # GETTER
    @staticmethod
    def getter(key):
        return dictGlobal[key]

    # SETTER
    @staticmethod
    def setter(key, value):
        dictGlobal[key] = value


if __name__ == "__main__":
    # Parser.run("printlnn = 2;")
    # print(dictGlobal)
    with open(sys.argv[1], "r") as f:
        Parser.run(f.read())
