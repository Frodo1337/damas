#coding: UTF-8

import sys
import math
from copy import deepcopy
from tree import Tree
from peca import Peca
from tabuleiro import Tabuleiro

class Damas:
    def __init__(self, cores, inter):
        self.cores = cores
        #Tabuleiro, não tem muito oq falar, é o tabuleiro mesmo, usa nulo para casas vazias
        self.tabuleiro = Tabuleiro(cores)
        #-1: jogo em andamento, 0: vitória do jogador 2, 1: vitória do jogador 1, 3: empate
        self.estado = -1
        #Posiciona as peças no tabuleiro
        self.inter = inter
        self.tabuleiro.criarTabuleiro(self.inter)
        self.tabuleiro.createPecas(self.inter)


    def contaPecas(self, jogador):
        count = 0

        #Conta o número de peças de um jogador
        for i in self.tabuleiro.casas:
            for j in i:
                if j and j.cor == jogador:
                    count += 1

        return count

    def contaDamas(self, jogador):
        count = 0

        #Conta o número de damas de um jogador
        for i in self.tabuleiro.casas:
            for j in i:
                if j and j.cor == jogador and j.dama:
                    count += 1

        return count

    def verificaFimDeJogo(self):
        #Verifica se o jogo foi ganho ou empatou
        #Como o jogador de baixo começa, a última posição da lista de cores será o primeiro jogador
        pecasJogador1 = self.contaPecas(self.cores[1])
        pecasJogador2 = self.contaPecas(self.cores[0])

        if pecasJogador1 == 0:
            self.estado = 1
        if pecasJogador2 == 0:
            self.estado = 0

    def verificaEstadoJogo(self):
        self.verificaFimDeJogo()

        if self.estado != -1:
            return True
        else:
            return False

    #Preenchimento da game tree
    #node: nó atual
    #cor: cor da peça
    #tabuleiro: tabuleiro do jogo, SEMPRE precisa ser uma cópia
    #deepth: nível atual na árvore
    #maxDeepth: altura da árvore, tem como padrão tamanho 3, sempre considerar
    #que com a raíz, o tamanho da árvore é maxDeepth + 1
    def preencheGameTree(self, node, cor, tabuleiro, arvore, deepth, maxDeepth=3):
        if deepth < maxDeepth:
            #Altera o tipo do nível do nó entre min e max
            if deepth % 2 == 0:
                nivelAtual = "min"
            else:
                nivelAtual = "max"

            #Se não existem nós filhos no raíz atual, aqui são inseridos como nó cada peça que
            #pode se movimentar no estado atual do jogo
            if not node.adjacencias and deepth == 0:
                #Faz uma cópia do tabuleiro
                copiaTabuleiro = deepcopy(tabuleiro)
                jogadas = tabuleiro.pecasComJogadaPossivel(cor)

                for i in jogadas:
                    copiaTabuleiro.atualiza(i, [i.coordenada])
                    #Cria nós filhos na raíz
                    arvore.criaAdjacencia(node.valor, i.coordenada, copiaTabuleiro,
                                          copiaTabuleiro.pontuacaoCasa(i.coordenada[0], i.coordenada[1]),
                                          nivelAtual)
            elif not node.adjacencias:
                peca = tabuleiro.getPeca(node.valor[0], node.valor[1])
                diagonais = peca.getDiagonais()

                for i in diagonais:
                    if i:
                        #Copia o tabuleiro
                        copiaTabuleiro = deepcopy(tabuleiro)

                        copiaTabuleiro.atualiza(peca, [i])
                        arvore.criaAdjacencia(node.valor, i, copiaTabuleiro,
                                              copiaTabuleiro.pontuacaoCasa(i[0], i[1]),
                                              nivelAtual)

                arvore.printa()
                print(arvore.getAdjNivel(deepth))

                #Troca o jogador
                cor = self.cores[0] if cor == self.cores[1] else self.cores[1]

            #Pega todas as adjacencias do nível atual da árvore
            adj = arvore.getAdjNivel(deepth)

            for i in adj:
                #Desce um nível na árvore
                deepth += 1
                self.preencheGameTree(i, cor, copiaTabuleiro, arvore, deepth)

            '''
            for i in adj:
                for j in jogadas:
                    diagonais = j.getDiagonais()

                    for k in diagonais:
                        if k:
                            copiaTabuleiro = deepcopy(tabuleiro)
                            peca = copiaTabuleiro.getPeca(j.coordenada[0], j.coordenada[1])

                            copiaTabuleiro.atualiza(peca, [k])
                            arvore.criaAdjacencia(i.valor, k, copiaTabuleiro,
                                                  copiaTabuleiro.pontuacaoCasa(k[0], k[1]),
                                                  nivelAtual)
            deepth += 1
            cor = self.cores[0] if cor == self.cores[1] else self.cores[1]
            self.preencheGameTree(node, cor, tabuleiro, arvore, deepth)
            '''

    def melhorJogada(self, pecas):
        #Faz uma cópia do tabuleiro para não alterar o tabuleiro atual
        copiaTabuleiro = deepcopy(self.tabuleiro)
        arvore = Tree(None, copiaTabuleiro, float("inf"), max=True)

        self.preencheGameTree(arvore, pecas[0].cor, copiaTabuleiro, arvore, 0)

        #arvore.printa()

    def joga(self):
        #Loop para jogar o jogo
        #Como o jogador de baixo começa, a última posição da lista de cores será o primeiro jogador
        #O jogadorAtual é o índice da lista de cores
        jogadorAtual = 1

        self.tabuleiro.atualizaMobilidadePecas()
        #self.tabuleiro.printa()

        while True:
            print("Vez do jogador: " + self.cores[jogadorAtual])
            #Lista com todas as peças que o jogador pode mover
            possiveisPecas = self.tabuleiro.pecasComJogadaPossivel(self.cores[jogadorAtual])
            #Peça escolhida pela I.A e coordenadas por onde a peça irá se mover
            self.melhorJogada(possiveisPecas)

            #Atualiza o tabuleiro com as variáveis obtidas acima
            #self.atualizaTabuleiro(pecaMovida, coordenadasMovimento)
            #self.printa()

            if self.verificaEstadoJogo():
                #self.printa()
                #Retorna o jogador vencedor
                return self.cores[self.estado]

            #Passa a vez para o outro jogador
            if jogadorAtual == 1:
                jogadorAtual = 0
            else:
                jogadorAtual = 1

            return self.cores[self.estado]
