#encoding: utf-8

import sys
from peca import Peca

class Tabuleiro:
    def __init__(self, cores):
        self.cores = cores
        self.casas = []
        self.altura = 10
        self.largura = 10

    def createPecas(self):
        min = 0
        max = 4
        restoMod = 1
        corAtual = self.cores[0]
        #Cria uma lista de listas para ser o conteúdo do tabuleiro e preeche todas as posições com nulo
        casas = [[None for j in range(self.largura)] for i in range(self.altura)]

        #Nesse laço existem dois passos, o primeiro que irá colocar as peças de forma casa sim e casa não para
        #o primeiro lado do tabuleiro, o lado de cima, nesse caso será preenchido com X.
        #O segundo passo preenche o outro lado do tabuleiro com as peças restantes, nesse caso será 0.
        #Esse laço não percorre o "meio" do tabuleiro, ele percorre primeiro de 0 a 3 e depois de 6 a 9.
        for n in range(2):
            for i in range(min, max):
                for j in range(self.largura):
                    if j % 2 == restoMod:
                        casas[i][j] = Peca(corAtual, [i, j])
                if restoMod == 1:
                    restoMod = 0
                else:
                    restoMod = 1
            min = 6
            max = 10
            corAtual = self.cores[1]

        #Atualiza o tabuleiro com o novo criado
        self.casas = casas

    def atualizaMobilidadePecas(self):
        #Faz uma cópia do tabuleiro para poder alterar ele com segurança
        casasAtualizadas = self.casas
        #Define o tamanho do laço de repetição
        max = len(casasAtualizadas)

        for i in range(max):
            for j in casasAtualizadas[i]:
                if j:
                    #Lista com todas as diagonais possíveis dependendo do tipo da peça
                    opts = []

                    #Definição de todos os possíveis movimentos para uma peça

                    #Esquerda Baixo
                    opts.append([j.coordenada[0] + 1, j.coordenada[1] - 1])
                    #Direita Baixo
                    opts.append([j.coordenada[0] + 1, j.coordenada[1] + 1])
                    #Esquerda Cima
                    opts.append([j.coordenada[0] - 1, j.coordenada[1] - 1])
                    #Direita Cima
                    opts.append([j.coordenada[0] - 1, j.coordenada[1] + 1])

                    max = len(opts)

                    #O laço abaixo percorre todas os movimentos possíveis definidos acima e verifica se eles
                    #estão dentro das regras do jogo, ou seja, se são movimentos dentro do tabuleiro
                    #e se não vão colidir com alguma outra peça.
                    #Caso exista uma peça em uma das suas diagonais e seja do oponente, é considerado um movimento válido,
                    #pois é possível passar sob essa peça

                    for i in range(max):
                        #Caso o movimento esteja fora dos limites das coordenadas do tabuleiro ou já exista uma peça
                        #nesse movimento, ele é descartado e marcado como inválido
                        if (opts[i][0] < 0 or opts[i][0] >= self.altura or opts[i][0] >= self.largura) or \
                           (opts[i][1] < 0 or opts[i][1] >= self.altura or opts[i][1] >= self.largura) or \
                           (casasAtualizadas[opts[i][0]][opts[i][1]] != None and \
                            casasAtualizadas[opts[i][0]][opts[i][1]].cor == j.cor):
                            opts[i] = False

                    #Atribuição das diagonais
                    j.esquerdaBaixo = opts[0]
                    j.direitaBaixo = opts[1]
                    j.esquerdaCima = opts[2]
                    j.direitaCima = opts[3]

        #Atualiza o tabuleiro
        self.casas = casasAtualizadas

    def pontoMedio(self, coordenada0, coordenada1):
        pontoMedio = [int((((coordenada0[0] + coordenada1[0]) / 2))),
                      int((((coordenada0[1] + coordenada1[1]) / 2)))]

        return pontoMedio

    def atualiza(self, peca, jogadas):
        #Faz uma cópia do tabuleiro para poder atualizar com segurança
        casasAtualizadas = self.casas
        #Coordenadas das peças a serem removidas do jogo
        removidas = []
        #Coordenada da peça
        coordenadaAtual = peca.coordenada
        #Diagonais da peça
        diagonaisAtuais = peca.getDiagonais()

        for i in jogadas:
            #Se a casa do tabuleiro tiver uma peça
            if casasAtualizadas[i[0]][i[1]]:
                #Ponto médio para ver o que existe entre a coordenada inicial e a coordenada final da jogada
                pontoMedio = self.pontoMedio(i, coordenadaAtual)

                #Se o que existe no ponto médio for uma peça e está no alcance da peça a ser movimentada,
                #a peça existente no ponto médio será marcada para remoção
                if pontoMedio in diagonaisAtuais and casasAtualizadas[pontoMedio[0]][pontoMedio[1]]:
                    removidas.append(pontoMedio)

                #Se a peça do jogador de baixo chegar no outro lado do tabuleiro, essa peça vira dama
                if i[1] == 0 and casasAtualizadas[coordenadaAtual[0]][coordenadaAtual[1]].cor == self.cores[1]:
                    casasAtualizadas[coordenadaAtual[0]][coordenadaAtual[1]].viraDama()
                #Se a peça do jogador de cima chegar no outro lado do tabuleiro, essa peça vira dama
                elif i[1] == (self.altura - 1) and casasAtualizadas[coordenadaAtual[0]][coordenadaAtual[1]].cor == self.cores[0]:
                    casasAtualizadas[coordenadaAtual[0]][coordenadaAtual[1]].viraDama()

            #Remove a peça da posição anterior dela
            casasAtualizadas[coordenadaAtual[0]][coordenadaAtual[1]] = None
            #Atualiza a posição da peça sendo jogada
            coordenadaAtual = i
            #Atualiza o tabuleiro com a coordenada da peça
            casasAtualizadas[coordenadaAtual[0]][coordenadaAtual[1]] = Peca(peca.cor, coordenadaAtual)

            #Atualiza todos as jogadas possíveis de todas as peças do tabuleiro
            self.atualizaMobilidadePecas()
            #self.printa()

            #Atualiza as jogadas possíveis da peça atual
            diagonaisAtuais = casasAtualizadas[coordenadaAtual[0]][coordenadaAtual[1]].getDiagonais()

        #Caso existam peças a serem removidas, elas serão subsitituidas por nulo
        if len(removidas) > 0:
            for i in removidas:
                casasAtualizadas[i[0]][i[1]] = None

        #Atualiza o tabuleiro
        self.casas = casasAtualizadas

    def pecasComJogadaPossivel(self, cor):
        #Nesse laço são adicionadas a uma lista as peças da cor desejada que podem se mover
        pecas = [j for i in self.casas for j in i
                 if j and j.cor == cor and (j.esquerdaBaixo or j.direitaBaixo or j.esquerdaCima or j.direitaCima)]

        return pecas

    def getPeca(self, x, y):
        return self.casas[x][y]

    def pontuacaoCasa(self, x, y):
        coordenada = self.casas[x][y]
        #Pontuações para a árvore de decisões
        #Casa vazia: 0
        #Casa com dama: 2
        #Casa com peça: 1

        if not coordenada:
            return 0
        elif coordenada.dama:
            return 2
        elif coordenada.cor == self.cores[0] or coordenada.cor == self.cores[1]:
            return 1

    def printa(self):
        #Imprime como o tabuleiro está atualmente
        for i in self.casas:
            for j in i:
                #Se a posição for nula, ele printa um espaço, só pra não ficar feio no terminal
                if j:
                    sys.stdout.write(j.cor)
                else:
                    sys.stdout.write(" ")
            sys.stdout.write("\n")
        sys.stdout.write("\n")
