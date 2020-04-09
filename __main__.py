#FEITO POR: GUSTAVO RAPOSO, RICARDO NAOKI, JOÃO FELIPE SCHWAB E MATHEUS SIQUEIRA

#coding: UTF-8

from damas import Damas

if __name__ == "__main__":
    #Definição das cores das peças, usei "X" e "O" para printar melhor no terminal
    cores = ["X", "O"]
    #Instancia um tabuleiro com as peças definidas acima
    jogoDamas = Damas(cores)

    #Posiciona as peças no tabuleiro
    jogoDamas.createPecas()
    #Printa o tabuleiro
    jogoDamas.printa()
    #Atualiza para todas as peças as possíveis direções de movimento
    jogoDamas.atualizaMobilidadePecas()
