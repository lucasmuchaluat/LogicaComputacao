import sys


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
        countSpace = 0
        origin += "#"

        for caracter in origin:
            if not caracter == " ":
                if(caracter.isdigit()):
                    if countSpace == 0:
                        numero += caracter
                    else:
                        raise ValueError("Espaço entre números!")

                elif(caracter == "+"):
                    tokens_list.append(Token("INT", int(numero)))
                    tokens_list.append(Token("PLUS", "+"))
                    numero = ""
                    countSpace = 0
                elif(caracter == "-"):
                    tokens_list.append(Token("INT", int(numero)))
                    tokens_list.append(Token("MINUS", "-"))
                    numero = ""
                    countSpace = 0
                elif(caracter == "*"):
                    tokens_list.append(Token("INT", int(numero)))
                    tokens_list.append(Token("TIMES", "*"))
                    numero = ""
                    countSpace = 0
                elif(caracter == "/"):
                    tokens_list.append(Token("INT", int(numero)))
                    tokens_list.append(Token("OVER", "/"))
                    numero = ""
                    countSpace = 0
                elif(caracter == "#"):
                    tokens_list.append(Token("INT", int(numero)))
                    tokens_list.append(Token("EOF", "#"))
                    numero = ""
                    countSpace = 0
                    break
            else:
                if numero:
                    countSpace += 1

        return tokens_list


class Parser:
    def __init__(self):
        self.tokens = None

    @staticmethod
    def parseExpression():
        operadores = ["PLUS", "MINUS", "TIMES", "OVER"]
        if(Parser.tokens.actual.type == "INT"):
            resultado = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            while(Parser.tokens.actual.type in operadores):
                if(Parser.tokens.actual.type == "PLUS"):
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual.type == "INT"):
                        resultado += Parser.tokens.actual.value
                    else:
                        raise ValueError
                elif(Parser.tokens.actual.type == "MINUS"):
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual.type == "INT"):
                        resultado -= Parser.tokens.actual.value
                    else:
                        raise ValueError
                elif(Parser.tokens.actual.type == "TIMES"):
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual.type == "INT"):
                        resultado *= Parser.tokens.actual.value
                    else:
                        raise ValueError
                elif(Parser.tokens.actual.type == "OVER"):
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual.type == "INT"):
                        resultado /= Parser.tokens.actual.value
                    else:
                        raise ValueError
                Parser.tokens.selectNext()
            return int(resultado)
        else:
            raise ValueError

    @staticmethod
    def run(origin):
        Parser.tokens = Tokenizer(origin)
        return Parser.parseExpression()


if __name__ == "__main__":
    print(Parser.run(sys.argv[1]))
