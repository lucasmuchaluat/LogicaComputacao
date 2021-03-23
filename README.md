# LogicaComputacao
Repositório para disciplina Lógica da Computação 2021.1

O projeto consiste em construir um programa que recebe como argumento uma cadeia de operações de números inteiros de múltiplos dígitos. Ao final, ele deve exibir o resultado da conta.

Para rodá-lo, basta passar o argumento na chamada do programa como string. Por exemplo:

```
python3 main.py "2+2"
```

EBNF:

```
EXPRESSION = TERM, {("+" | "-"), TERM} ;
TERM = FACTOR, {("*" | "/"), FACTOR} ;
FACTOR = ("+" | "-"), FACTOR | "(", EXPRESSION, ")" | NUMBER ; 
NUMBER = DIGIT, {DIGIT} ;
DIGIT = 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 ;
```

Além de parênteses, o programa suporta o uso de comentários na expressão também. Para inserir um basta usar a seguinte notação:

```
python3 main.py "(3+2)/5 /* comentário */"
```
