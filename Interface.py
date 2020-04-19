from tkinter import *

class Interface:

    def __init__(self, root, largura, altura):
        self.root = root
        self.largura = largura
        self.altura = altura
    def criarTabuleiroI(self):
        inverte = 1
        for j in range(self.largura):
            for i in range(self.altura):
                if(inverte % 2 == 0 ):
                    if(i % 2 == 0):
                        quadrado = Label(self.root,text ="", fg="white", bg="black", width="10", height="5")
                    else:
                        quadrado = Label(self.root, text="", fg="black", bg="white", width="10", height="5")
                else:
                    if (i % 2 != 0):
                        quadrado = Label(self.root, text="", fg="white", bg="black", width="10", height="5")
                    else:
                        quadrado = Label(self.root, text="", fg="black", bg="white", width="10", height="5")

                quadrado.grid(row=j,column=i)
            inverte = inverte + 1

    def pula(self,bool):
        if(bool == True):
            return False
        else:
            return True

    def colocar_pecas_player1(self):
        inverte = 1
        apoio = False
        for j in range(4):
            for i in range(self.largura):
                if (inverte % 2 == 0):
                    if (apoio == False):
                        peca = Label(self.root, width="4", height="2", bg="red" )
                        peca.grid(row=j, column=i)
                else:
                    if (apoio == True):
                        peca = Label(self.root, width="4", height="2", bg="red")
                        peca.grid(row=j, column=i)

                apoio = self.pula(apoio)

            inverte = inverte + 1

    def colocar_pecas_player2(self):
        inverte = 1
        apoio = False
        for j in range(6,10):
            for i in range(self.largura):
                if (inverte % 2 == 0):
                    if (apoio == False):
                        peca = Label(self.root, width="4", height="2", bg="blue")
                        peca.grid(row=j, column=i)
                else:
                    if (apoio == True):
                        peca = Label(self.root, width="4", height="2", bg="blue")
                        peca.grid(row=j, column=i)

                apoio = self.pula(apoio)

            inverte = inverte + 1

    def removerPeca(self, linha, coluna):
        remove = self.root.grid_slaves(linha,coluna)
        remove[0].grid_forget()

    def plotarInterface(self):
        self.root.update()




