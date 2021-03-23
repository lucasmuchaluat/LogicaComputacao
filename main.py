import sys
import re


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

        resultTerm, token = Parser.parseTerm()
        resultExpression = resultTerm

        while(token.type in operadores):
            if(token.type == "PLUS"):
                Parser.tokens.selectNext()
                resultTerm, token = Parser.parseTerm()
                resultExpression += resultTerm
            elif(token.type == "MINUS"):
                Parser.tokens.selectNext()
                resultTerm, token = Parser.parseTerm()
                resultExpression -= resultTerm
            else:
                raise ValueError
        if token.type == "EOF" or token.type == "RPAR":
            return int(resultExpression)
        else:
            raise ValueError

    @staticmethod
    def parseTerm():
        operadores = ["TIMES", "OVER"]

        resultFactor = Parser.parseFactor()
        resultTerm = resultFactor
        Parser.tokens.selectNext()

        while(Parser.tokens.actual.type in operadores):
            if(Parser.tokens.actual.type == "TIMES"):
                Parser.tokens.selectNext()
                resultFactor = Parser.parseFactor()
                resultTerm *= resultFactor
            elif(Parser.tokens.actual.type == "OVER"):
                Parser.tokens.selectNext()
                resultFactor = Parser.parseFactor()
                resultTerm /= resultFactor
            Parser.tokens.selectNext()

        return int(resultTerm), Parser.tokens.actual

    @staticmethod
    def parseFactor():
        if(Parser.tokens.actual.type == "INT"):
            resultFactor = Parser.tokens.actual.value
            return resultFactor
        elif(Parser.tokens.actual.type == "PLUS"):
            Parser.tokens.selectNext()
            return Parser.parseFactor()
        elif(Parser.tokens.actual.type == "MINUS"):
            Parser.tokens.selectNext()
            return -Parser.parseFactor()
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
        return Parser.parseExpression()


class PrePro:
    @staticmethod
    def filter(arg):
        new_arg = re.sub(r"\/\*.*?\*\/", " ", arg)
        return new_arg


if __name__ == "__main__":
    print(Parser.run(sys.argv[1]))
