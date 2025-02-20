# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 20:55:23 2025

@author: utilisateur
"""

from tkinter import *
from board import Board, WIDTH, HEIGHT


class GameInterface:
    def __init__(self, myWindow):
        self.myWindow = myWindow
        self.myWindow.title("Jeu de Plateau")
        
        # Création du canevas
        self.myCanvas = Canvas(myWindow, width=WIDTH, height=HEIGHT, bg="white")
        self.myCanvas.pack()
        
        # Création du plateau de jeu
        self.board = Board(self.myCanvas)

if __name__ == "__main__":
    myWindow = Tk()
    app = GameInterface(myWindow)
    myWindow.mainloop()
