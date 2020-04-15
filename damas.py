#coding: UTF-8

import sys

from node import Node
from tree import Tree
from peca import Peca

class Damas:
    def __init__(self, cores):
        self.cores = cores
        #Tabuleiro, não tem muito oq falar, é o tabuleiro mesmo, usa nulo para casas vazias
        self.tabuleiro = []
        self.altura = 10
        self.largura = 10
        #-1: jogo em andamento, 0: vitória do jogador 2, 1: vitória do jogador 1, 3: empate
        self.estado = -1

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
                for j in range(self.largura):
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
                    #Lista com todas as diagonais possíveis dependendo do tipo da peça
                    opts = []

                    #Nesses próximos if, serão definidos todos os possíveis movimentos para uma peça,
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
                    sys.stdout.write(j.cor)
                else:
                    sys.stdout.write(" ")
            sys.stdout.write("\n")
        sys.stdout.write("\n")

    def contaPecas(self, jogador):
        count = 0

        #Conta o número de peças de um jogador
        for i in self.tabuleiro:
            for j in i:
                if j and j.cor == jogador:
                    count += 1

        return count

    def contaDamas(self, jogador):
        count = 0

        #Conta o número de damas de um jogador
        for i in self.tabuleiro:
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

    def pecasComJogadaPossivel(self, cor):
        #Nesse laço são adicionadas a uma lista as peças da cor desejada que podem se mover
        pecas = [j for i in self.tabuleiro for j in i
                 if j and j.cor == cor and (j.esquerdaBaixo or j.direitaBaixo or j.esquerdaCima or j.direitaCima)]

        return pecas

    def pontoMedio(self, coordenada0, coordenada1):
        pontoMedio = [int((((coordenada0[0] + coordenada1[0]) / 2))),
                      int((((coordenada0[1] + coordenada1[1]) / 2)))]

        return pontoMedio

    def atualizaTabuleiro(self, peca, jogadas):
        #Faz uma cópia do tabuleiro para poder atualizar com segurança
        tabuleiroAtualizado = self.tabuleiro
        #Coordenadas das peças a serem removidas do jogo
        removidas = []
        #Coordenada da peça
        coordenadaAtual = peca.coordenada
        #Diagonais da peça
        diagonaisAtuais = peca.getDiagonais()

        for i in jogadas:
            #Se a casa do tabuleiro tiver uma peça
            if tabuleiroAtualizado[i[0]][i[1]]:
                #Ponto médio para ver o que existe entre a coordenada inicial e a coordenada final da jogada
                pontoMedio = self.pontoMedio(i, coordenadaAtual)

                #Se o que existe no ponto médio for uma peça e está no alcance da peça a ser movimentada,
                #a peça existente no ponto médio será marcada para remoção
                if pontoMedio in diagonaisAtuais and tabuleiroAtualizado[pontoMedio[0]][pontoMedio[1]]:
                    removidas.append(pontoMedio)

                #Se a peça do jogador de baixo chegar no outro lado do tabuleiro, essa peça vira dama
                if i[1] == 0 and tabuleiroAtualizado[coordenadaAtual[0]][coordenadaAtual[1]].cor == self.cores[1]:
                    tabuleiroAtualizado[coordenadaAtual[0]][coordenadaAtual[1]].viraDama()
                #Se a peça do jogador de cima chegar no outro lado do tabuleiro, essa peça vira dama
                elif i[1] == (self.altura - 1) and tabuleiroAtualizado[coordenadaAtual[0]][coordenadaAtual[1]].cor == self.cores[0]:
                    tabuleiroAtualizado[coordenadaAtual[0]][coordenadaAtual[1]].viraDama()

            #Remove a peça da posição anterior dela
            tabuleiroAtualizado[coordenadaAtual[0]][coordenadaAtual[1]] = None
            #Atualiza a posição da peça sendo jogada
            coordenadaAtual = i
            #Atualiza o tabuleiro com a coordenada da peça
            tabuleiroAtualizado[coordenadaAtual[0]][coordenadaAtual[1]] = Peca(peca.cor, coordenadaAtual)

            #Atualiza todos as jogadas possíveis de todas as peças do tabuleiro
            self.atualizaMobilidadePecas()
            self.printa()

            #Atualiza as jogadas possíveis da peça atual
            diagonaisAtuais = tabuleiroAtualizado[coordenadaAtual[0]][coordenadaAtual[1]].getDiagonais()

        #Caso existam peças a serem removidas, elas serão subsitituidas por nulo
        if len(removidas) > 0:
            for i in removidas:
                tabuleiroAtualizado[i[0]][i[1]] = None

        #Atualiza o tabuleiro
        self.tabuleiro = tabuleiroAtualizado

    def melhorJogada(self, jogadas):
        #Define qual será a melhor jogada, deverá retornar a peça a ser movida e as coordenadas dos movimentos numa lista
        arvores = []

        peca = self.tabuleiro[3][2]
        coordenadasMovimentosPeca = [[4, 1], [5, 0]]

        return peca, coordenadasMovimentosPeca

    def joga(self):
        #Loop para jogar o jogo
        #Como o jogador de baixo começa, a última posição da lista de cores será o primeiro jogador
        #O jogadorAtual é o índice da lista de cores
        jogadorAtual = 1

        self.atualizaMobilidadePecas()
        self.printa()

        while True:
            print("Vez do jogador: " + self.cores[jogadorAtual])
            #Lista com todas as peças que o jogador pode mover
            jogadasJogadorAtual = self.pecasComJogadaPossivel(self.cores[jogadorAtual])
            #Peça escolhida pela I.A e coordenadas por onde a peça irá se mover
            pecaMovida, coordenadasMovimento = self.melhorJogada(jogadasJogadorAtual)

            #Atualiza o tabuleiro com as variáveis obtidas acima
            self.atualizaTabuleiro(pecaMovida, coordenadasMovimento)
            #self.printa()

            if self.verificaEstadoJogo():
                self.printa()
                #Retorna o jogador vencedor
                return self.cores[self.estado]

            #Passa a vez para o outro jogador
            if jogadorAtual == 1:
                jogadorAtual = 0
            else:
                jogadorAtual = 1

            return self.cores[self.estado]
