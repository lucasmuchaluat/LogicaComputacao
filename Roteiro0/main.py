import sys

sys.argv.pop(0)

pilha = []

for arg in sys.argv[0]:
    if not arg == ' ':
        pilha.append(arg)

pilha_certa = []
operadores = []
aux = 0

for contador in range(len(pilha)):
    if pilha[contador] in ['+', '-']:
        pilha_certa.append(''.join(map(str, pilha[aux:contador])))
        pilha_certa.append(pilha[contador])
        operadores.append(pilha[contador])
        aux = contador + 1

pilha_certa.append(''.join(map(str, pilha[aux:len(pilha)])))

if not operadores:
    sys.exit("Error message")

resultado = 0

for i in range(0, len(pilha_certa)):
    if pilha_certa[i] == "+":
        if i == 1:
            resultado = int(pilha_certa[i-1]) + int(pilha_certa[i+1])
        else:
            resultado += int(pilha_certa[i+1])
    if pilha_certa[i] == "-":
        if i == 1:
            resultado = int(pilha_certa[i-1]) - int(pilha_certa[i+1])
        else:
            resultado -= int(pilha_certa[i+1])

print(resultado)
