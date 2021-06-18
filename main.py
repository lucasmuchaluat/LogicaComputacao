import sys
import re

dictGlobal = {}
mem4 = 4

print('''
; constantes
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data

segment .bss  ; variaveis
  res RESB 1

section .text
  global _start

print:  ; subrotina print

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

  MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
  XOR ESI, ESI

print_dec: ; empilha todos os digitos
  MOV EDX, 0
  MOV EBX, 0x000A
  DIV EBX
  ADD EDX, '0'
  PUSH EDX
  INC ESI ; contador de digitos
  CMP EAX, 0
  JZ print_next ; quando acabar pula
  JMP print_dec

print_next:
  CMP ESI, 0
  JZ print_exit ; quando acabar de imprimir
  DEC ESI

  MOV EAX, SYS_WRITE
  MOV EBX, STDOUT

  POP ECX
  MOV [res], ECX
  MOV ECX, res

  MOV EDX, 1
  INT 0x80
  JMP print_next

print_exit:
  POP EBP
  RET

; subrotinas if/while
binop_je:
  JE binop_true
  JMP binop_false

binop_jg:
  JG binop_true
  JMP binop_false

binop_jl:
  JL binop_true
  JMP binop_false

binop_false:
  MOV EBX, False
  JMP binop_exit
binop_true:
  MOV EBX, True
binop_exit:
  RET

_start:

  PUSH EBP ; guarda o base pointer
  MOV EBP, ESP ; estabelece um novo base pointer

; codigo gerado pelo compilador''')


class Node:
    idNode = 0

    def __init__(self, valorNode, nodeList=[]):
        self.value = valorNode
        self.children = nodeList
        self.idNode = Node.idNode
        Node.idNode += 1

    def Evaluate(self):
        pass


class BinOp(Node):
    def Evaluate(self):
        child1 = self.children[0].Evaluate()
        print("PUSH EBX")
        child2 = self.children[1].Evaluate()

        print("; codigo gerado pelo BinOp")

        if self.value == "EQUAL":
            valorOp = bool(child1 == child2)
            print("POP EAX")
            print("CMP EAX, EBX")
            print("CALL binop_je")
        elif isinstance(child1, str) or isinstance(child2, str):
            raise ValueError("ERROR: Incompatible types!")
        elif self.value == "PLUS":
            valorOp = child1 + child2
            print("POP EAX")
            print("ADD EAX, EBX")
            print("MOV EBX, EAX")
        elif self.value == "MINUS":
            valorOp = child1 - child2
            print("POP EAX")
            print("SUB EAX, EBX")
            print("MOV EBX, EAX")
        elif self.value == "TIMES":
            valorOp = child1 * child2
            print("POP EAX")
            print("IMUL EBX")
            print("MOV EBX, EAX")
        elif self.value == "OVER":
            valorOp = child1 / child2
            print("POP EAX")
            print("IDIV EBX")
            print("MOV EBX, EAX")
        elif self.value == "MAIOR":
            valorOp = bool(child1 > child2)
            print("POP EAX")
            print("CMP EAX, EBX")
            print("CALL binop_jg")
        elif self.value == "MENOR":
            valorOp = bool(child1 < child2)
            print("POP EAX")
            print("CMP EAX, EBX")
            print("CALL binop_jl")
        elif self.value == "AND":
            valorOp = bool(child1 and child2)
            print("POP EAX")
            print("AND EAX, EBX")
            print("MOV EBX, EAX")
        elif self.value == "OR":
            valorOp = bool(child1 or child2)
            print("POP EAX")
            print("OR EAX, EBX")
            print("MOV EBX, EAX")
        else:
            raise ValueError("BinOp operation error")

        return int(valorOp)


class Atribuicao(Node):
    def Evaluate(self):
        global mem4
        child1 = self.children[0]

        if self.value == "ISTYPE":
            print(f"; Atribuicao de {child1}")
            print("PUSH DWORD 0")
            child2 = self.children[1]
            if child1 not in dictGlobal.keys():
                SymbolTable.setterType(child1, type_=child2, address=mem4)
                mem4 += 4
            else:
                raise ValueError("Variavel already exists!")

        if self.value == "RECEBE":
            child2 = self.children[1].Evaluate()
            SymbolTable.setterValue(child1, child2)
            addressVar = SymbolTable.getterAddress(child1)

            print(f"MOV [EBP-{addressVar}], EBX")


class UnOp(Node):
    def Evaluate(self):
        child1 = self.children[0].Evaluate()

        print("; codigo gerado pelo UnOp")

        if self.value == "PLUS":
            valorOp = child1
            print("PASS")
        elif self.value == "MINUS":
            valorOp = -child1
            print("POP EAX")
            print("NEG EBX")
            print("MOV EBX, EAX")
        elif self.value == "NOT":
            valorOp = not child1
            print("POP EAX")
            print("NOT EBX")
            print("MOV EBX, EAX")

        return int(valorOp)


class IntVal(Node):
    def Evaluate(self):
        valorInteiro = self.value

        print("; codigo gerado pelo IntVal")
        print(f"MOV EBX, {valorInteiro}")

        return(valorInteiro)


class BoolVal(Node):
    def Evaluate(self):
        valorBooleano = self.value
        inteiroBooleano = int(valorBooleano == "true")

        print("; codigo gerado pelo BoolVal")
        print(f"MOV EBX, {inteiroBooleano}")

        return(inteiroBooleano)


class StringVal(Node):
    def Evaluate(self):
        valorString = self.value
        return(valorString)


class Identific(Node):
    def Evaluate(self):
        valorVariavel = SymbolTable.getter(self.value)
        addressVar = SymbolTable.getterAddress(self.value)
        print(f"MOV EBX, [EBP-{addressVar}]")
        return(valorVariavel)


class NoOp(Node):
    def Evaluate(self):
        return


class Println(Node):
    def Evaluate(self):
        child1 = self.children[0].Evaluate()
        # print(child1)
        print("PUSH EBX")
        print("CALL print")
        print("POP EBX")


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
        # while self.children[0].Evaluate():
        #     self.children[1].Evaluate()
        print(f"LOOP_{Node.idNode}:")
        self.children[0].Evaluate()
        print("CMP EBX, False")
        print(f"JE EXIT_{Node.idNode}")
        self.children[1].Evaluate()
        print(f"JMP LOOP_{Node.idNode}")
        print(f"EXIT_{Node.idNode}:")


class If(Node):
    def Evaluate(self):
        # if self.children[0].Evaluate():
        #     self.children[1].Evaluate()
        # else:
        #     self.children[2].Evaluate()
        print(f"IF_{Node.idNode}:")
        self.children[0].Evaluate()
        print("CMP EBX, False")
        print(f"JE ELSE_{Node.idNode}")
        self.children[1].Evaluate()
        print(f"JMP EXIT_{Node.idNode}")
        print(f"ELSE_{Node.idNode}:")
        self.children[2].Evaluate()
        print(f"EXIT_{Node.idNode}")


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
        isString = 0
        stringText = ""
        palavrasReservadas = ["println", "readln",
                              "while", "if", "else", "int", "bool", "string", "true", "false"]
        operadoresDuplos = ["=", "&", "|"]

        for caracter in origin:
            if identifier:
                if identifier[0] == "_":
                    raise ValueError("Variavel Não pode começar com _!")

            if(caracter.isdigit() and identifier == "" and stringText == ""):
                numero += caracter

            elif(caracter == " " and isString == 0 and isString == 0):
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
                    else:
                        tokens_list.append(Token("IDENT", identifier))
                    identifier = ""
                tokens_list.append(Token("NOT", "!"))

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

    @staticmethod
    def getterAddress(key):
        return dictGlobal[key][2]

    # SETTER TYPE
    @staticmethod
    def setterType(key, value=None, type_=None, address=None):
        dictGlobal[key] = [value, type_, address]

    # SETTER VALUE
    @staticmethod
    def setterValue(key, value):
        if dictGlobal[key][1] == "bool":
            dictGlobal[key][0] = int(bool(value))
        elif dictGlobal[key][1] == "int":
            dictGlobal[key][0] = int(value)
        elif dictGlobal[key][1] == "string":
            dictGlobal[key][0] = value


if __name__ == "__main__":
    # with open("./teste000.c", "r") as f:
    with open(sys.argv[1], "r") as f:
        Parser.run(f.read())
        print(''' 
; interrupcao de saida
POP EBP
MOV EAX, 1
INT 0x80''')
