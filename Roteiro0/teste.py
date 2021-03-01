import sys

sys.argv.pop(0)

pilha = []

for arg in sys.argv[0]:
    if not arg == ' ':
        pilha.append(arg)

resultado = 0

print(pilha)

pilha_certa = []
aux = 0

for contador in range(len(pilha)):
    if pilha[contador] in ['+', '-']:
        pilha_certa.append(''.join(map(str, pilha[aux:contador])))
        pilha_certa.append(pilha[contador])
        aux = contador + 1

pilha_certa.append(''.join(map(str, pilha[aux:len(pilha)])))

print(pilha_certa)
