# LogicaComputacao
Repositório para disciplina Lógica da Computação 2021.1

O projeto consiste em construir um programa que recebe como argumento uma cadeia de operações de números inteiros de múltiplos dígitos. Ao final, ele deve exibir o resultado da conta.

Para rodá-lo, basta passar o argumento na chamada do programa como string. Por exemplo:

```
python3 main.py "2+2"
```

EBNF:

```
EXPRESSION = NUMBER, {("+" | "-" | "*" | "/"), NUMBER} ; 
```

O programa suporta o uso de comentários na expressão também. Para inserir um basta usar a seguinte notação:

```
python3 main.py "11+22-33 /* comentário */"
```
