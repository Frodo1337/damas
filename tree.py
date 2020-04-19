#encoding: utf-8

import sys

class Tree:
    def __init__(self, valor, gameState, peso, min=False, max=False):
        self.valor = valor
        self.gameState = gameState
        self.peso = peso
        self.min = min
        self.max = max
        self.adjacencias = None

    #Cria uma adjacência de um nó x até um nó y
    #x: primeiro ponto da adjacência
    #y: segundo ponto da adjacência
    #gameState: cópia do tabuleiro
    #peso: peso da jogada
    #nivel: nível do nó, se ele é min ou max
    def criaAdjacencia(self, x, y, gameState, peso, nivel):
        if self.valor == x:
            #Se ainda não existirem adjacências, ela recebe uma lista
            if not self.adjacencias:
                self.adjacencias = []
            if nivel == "max":
                self.adjacencias.append(Tree(y, gameState, peso, max=True))
            elif nivel == "min":
                self.adjacencias.append(Tree(y, gameState, peso, min=True))
        else:
            if self.adjacencias:
                for i in self.adjacencias:
                    i.criaAdjacencia(x, y, gameState, peso, nivel)

    #Retorna todas as adjacencias de um nível da árvore
    #nivel: número da "profundidade" do nó, sendo 0 a raíz
    def getAdjNivel(self, nivel, atual=0):
        if nivel != atual:
            atual += 1
            self.getAdjNivel(nivel, atual=atual)
        else:
            return self.adjacencias

    #imprime a árvore
    def printa(self):
        nivel = "min" if self.min else "max"

        sys.stdout.write(str(self.valor) + " - " + nivel + ", " + str(self.peso) + ":\n")
        self.gameState.printa()

        if self.adjacencias:
            for i in self.adjacencias:
                i.printa()
