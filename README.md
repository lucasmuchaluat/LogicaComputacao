# LogicaComputacao
Repositório para disciplina Lógica da Computação 2021.1

O projeto consiste em construir um programa que recebe como argumento uma cadeia de operações de números inteiros de múltiplos dígitos. Ao final, ele deve exibir o resultado da conta.

Para rodá-lo, basta inserir a operação a ser realizada em um ```arquivo.c``` a sua escolha. Ele deve conter uma expressão (soma, multiplicação, parênteses, comentários, etc), sem aspas, disposta somente em uma linha (não serão testadas múltiplas expressões em um único arquivo).

Feito isso, é possível chamar o programa passando o nome do arquivo via linha de comando. Por exemplo:

```
python3 main.py {nome do seu arquivo}.c
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
"(3+2)/5 /* comentário */"
```
