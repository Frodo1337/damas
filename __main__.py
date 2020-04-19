#encoding: utf-8
#FEITO POR: GUSTAVO RAPOSO, RICARDO NAOKI, JOÃO FELIPE SCHWAB E MATHEUS SIQUEIRA

import time
from damas import Damas
from tkinter import *
from Interface import Interface

if __name__ == "__main__":
    # iniciando interface
    root = Tk()
    inter = Interface(root, 10, 10)
    #Definição das cores das peças, usei "X" e "O" para printar melhor no terminal
    cores = ["X", "O"]
    #Instancia um tabuleiro com as peças definidas acima
    jogoDamas = Damas(cores, inter)
    #Cria o tabuleiro e posiciona as peças
    #inter.removerPeca()
    inter.plotarInterface()
    time.sleep(5)

    vencedor = jogoDamas.joga()

    #print("O jogador " + str(vencedor) + " ganhou o jogo")

    root.mainloop()

