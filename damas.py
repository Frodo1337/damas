#coding: UTF-8

import sys

from peca import Peca

class Damas:
    def __init__(self, cores):
        self.cores = cores
        #Tabuleiro, não tem muito oq falar, é o tabuleiro mesmo, usa nulo para casas vazias
        self.tabuleiro = []
        self.altura = 10
        self.largura = 10

    def createPecas(self):
        min = 0
        max = 4
        restoMod = 1
        corAtual = self.cores[0]
        #Cria uma lista de listas para ser o tabuleiro e preeche todas as posições com nulo
        tabuleiro = [[None for j in range(self.largura)] for i in range(self.altura)]

        #Nesse laço existem dois passos, o primeiro que irá colocar as peças de forma casa sim e casa não para
        #o primeiro lado do tabuleiro, o lado de cima, nesse caso será preenchido com X.
        #O segundo passo preenche o outro lado do tabuleiro com as peças restantes, nesse caso será 0.
        #Esse laço não percorre o "meio" do tabuleiro, ele percorre primeiro de 0 a 3 e depois de 6 a 9.
        for n in range(2):
            for i in range(min, max):
                for j in range(self.altura):
                    if j % 2 == restoMod:
                        tabuleiro[i][j] = Peca(corAtual, [i, j])
                if restoMod == 1:
                    restoMod = 0
                else:
                    restoMod = 1
            min = 6
            max = 10
            corAtual = self.cores[1]

        #Atualiza o tabuleiro com o novo criado
        self.tabuleiro = tabuleiro

    def atualizaMobilidadePecas(self):
        #Faz uma cópia do tabuleiro para poder alterar ele com segurança
        posicoesAtualizadas = self.tabuleiro
        #Define o tamanho do laço de repetição
        max = len(posicoesAtualizadas)

        for i in range(max):
            for j in posicoesAtualizadas[i]:
                if j:
                    opts = []

                    #Nesses próximos if, será definido todos os possíveis movimentos para uma peça,
                    #ou seja, ele vai adicionar todas as diagonais dependendo do tipo da peça

                    #Se for uma dama, todas as diagonais são adicionadas como movimentos possíveis
                    if j.dama:
                        #Esquerda Baixo
                        opts.append([j.coordenada[0] + 1, j.coordenada[1] - 1])
                        #Direita Baixo
                        opts.append([j.coordenada[0] + 1, j.coordenada[1] + 1])
                        #Esquerda Cima
                        opts.append([j.coordenada[0] - 1, j.coordenada[1] - 1])
                        #Direita Cima
                        opts.append([j.coordenada[0] - 1, j.coordenada[1] + 1])
                    #Se a peça for da primeira cor, "X" nesse caso, somente as diagonais abaixo da peça são
                    #marcadas como movimentos possíveis
                    elif j.cor == self.cores[0]:
                        #Esquerda Baixo
                        opts.append([j.coordenada[0] + 1, j.coordenada[1] - 1])
                        #Direita Baixo
                        opts.append([j.coordenada[0] + 1, j.coordenada[1] + 1])
                    #Se a peça for da segunda cor, "O" nesse caso, somente as diagonais acima da peça são
                    #marcadas como movimentos possíveis
                    elif j.cor == self.cores[1]:
                        #Esquerda Cima
                        opts.append([j.coordenada[0] - 1, j.coordenada[1] - 1])
                        #Direita Cima
                        opts.append([j.coordenada[0] - 1, j.coordenada[1] + 1])

                    max = len(opts)

                    #O laço abaixo percorre todas os movimentos possíveis definidos acima e verifica se eles
                    #estão dentro das regras do jogo, ou seja, se são movimentos dentro do tabuleiro
                    #e se não vão colidir com alguma outra peça

                    for i in range(max):
                        #Caso o movimento esteja fora dos limites das coordenadas do tabuleiro ou já exista uma peça
                        #nesse movimento, ele é descartado e marcado como inválido
                        if (opts[i][0] < 0 or opts[i][0] >= self.altura or opts[i][0] >= self.largura) or \
                           (opts[i][1] < 0 or opts[i][1] >= self.altura or opts[i][1] >= self.largura) or \
                           (posicoesAtualizadas[opts[i][0]][opts[i][1]] != None):
                            opts[i] = False

                    #Aqui foi preciso fazer vários if por causa das diagonais,
                    #aqui é atualizado em quais diagonais a peça pode se mover,
                    #caso seja uma peça normal, ela só pode ir para frente, caso
                    #seja uma dama, ela pode tanto ir para frente quanto para trás
                    if j.cor == self.cores[0]:
                        j.esquerdaBaixo = opts[0]
                        j.direitaBaixo = opts[1]
                    elif j.cor == self.cores[1]:
                        j.esquerdaCima = opts[0]
                        j.direitaCima = opts[1]
                    elif max == 4:
                        j.esquerdaBaixo = opts[0]
                        j.direitaBaixo = opts[1]
                        j.esquerdaCima = opts[2]
                        j.direitaCima = opts[3]

        #Atualiza o tabuleiro
        self.tabuleiro = posicoesAtualizadas

    def printa(self):
        #Imprime como o tabuleiro está atualmente
        for i in self.tabuleiro:
            for j in i:
                #Se a posição for nula, ele printa um espaço, só pra não ficar feio no terminal
                if j:
                    sys.stdout.write(j.cor + " ")
                else:
                    sys.stdout.write(" ")
            sys.stdout.write("\n")
