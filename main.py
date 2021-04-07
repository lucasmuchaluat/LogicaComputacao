import sys
import re


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


class NoOp(Node):
    def Evaluate(self):
        return


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
        origin += "#"
        countPar = 0

        for caracter in origin:
            if(caracter.isdigit()):
                numero += caracter

            elif(caracter == " "):
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""

            elif(caracter == "+"):
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                tokens_list.append(Token("PLUS", "+"))

            elif(caracter == "-"):
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                tokens_list.append(Token("MINUS", "-"))

            elif(caracter == "*"):
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                tokens_list.append(Token("TIMES", "*"))

            elif(caracter == "/"):
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                tokens_list.append(Token("OVER", "/"))

            elif(caracter == "("):
                countPar += 1
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                tokens_list.append(Token("LPAR", "("))

            elif(caracter == ")"):
                countPar -= 1
                if countPar < 0:
                    raise ValueError("Desbalanceamento de parenteses!")
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                tokens_list.append(Token("RPAR", ")"))

            elif(caracter == "#"):
                if countPar != 0:
                    raise ValueError("Desbalanceamento de parenteses!")
                if numero:
                    tokens_list.append(Token("INT", int(numero)))
                    numero = ""
                tokens_list.append(Token("EOF", "#"))

                break

        return tokens_list


class Parser:
    def __init__(self):
        self.tokens = None

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

        if Parser.tokens.actual.type == "EOF" or Parser.tokens.actual.type == "RPAR":
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

    @staticmethod
    def run(origin):
        Parser.tokens = Tokenizer(PrePro.filter(origin))
        finalValue = Parser.parseExpression()
        return finalValue.Evaluate()


class PrePro:
    @staticmethod
    def filter(arg):
        new_arg = re.sub(r"\/\*.*?\*\/", " ", arg)
        return new_arg


if __name__ == "__main__":
    # print(Parser.run("(2 + 3) / ( 5 * 1)"))
    with open(sys.argv[1], "r") as f:
        print(Parser.run(f.read()))
