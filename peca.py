#coding: UTF-8

class Peca:
    def __init__(self, cor, coordenada):
        self.cor = cor
        #A coordenada dela é salva nela mesma para não precisar percorrer a matriz toda vez
        self.coordenada = coordenada
        #Movimentos possíveis, sendo falso para impossível e verdadeiro para possível, todos eles são na diagonal
        self.esquerdaCima = False
        self.direitaCima = False
        self.esquerdaBaixo = False
        self.direitaBaixo = False
        #Identifica se uma peça é uma dama
        self.dama = False
        #Peso para a árvore de decisão, caso seja feita
        self.peso = 1

    def viraDama(self):
        #Atualiza a peça para uma dama e aumenta o peso dela para a árvore de decisão
        self.dama = True
        self.peso = 2
