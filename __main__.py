#encoding: utf-8
#FEITO POR: GUSTAVO RAPOSO, RICARDO NAOKI, JOÃO FELIPE SCHWAB E MATHEUS SIQUEIRA

from damas import Damas

if __name__ == "__main__":
    #Definição das cores das peças, usei "X" e "O" para printar melhor no terminal
    cores = ["X", "O"]
    #Instancia um tabuleiro com as peças definidas acima
    jogoDamas = Damas(cores)

    vencedor = jogoDamas.joga()

    print("O jogador " + str(vencedor) + " ganhou o jogo")

    #jogoDamas.tabuleiro.printa()
