#encoding: utf-8

class Tree:
    def __init__(self, raiz):
        self.raiz = raiz

    def setProximo(self, no):
        atual = self.raiz

        while atual != None:
            if atual.proximo == None
                atual.proximo = no
            else:
                atual = atual.proximo
                
