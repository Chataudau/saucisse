from tkinter import *
from tkinter import simpledialog, messagebox
from board import Board, WIDTH, HEIGHT

# Variables globales pour stocker le vainqueur et le perdant
vainqueur = ""
perdant = ""

# Lecture des noms des joueurs
with open("noms.txt", "r", encoding="utf-8") as f:
    joueurs = f.readlines()[1:]  # Ignorer la première ligne "Liste des joueurs:"
    joueurs = [nom.strip() for nom in joueurs]
    joueurs_str = " | ".join(joueurs)  # Mettre les noms sur une seule ligne séparés par " | "

class GameInterface:
    def __init__(self, myWindow):
        self.myWindow = myWindow
        self.myWindow.title("Jeu de Plateau")
        
        # Création du cadre principal
        self.main_frame = Frame(myWindow)
        self.main_frame.pack()
        
        # Affichage de la liste des joueurs
        self.players_frame = Frame(self.main_frame)
        self.players_frame.pack(side=LEFT, padx=10, pady=10)
        self.players_label = Label(self.players_frame, text=f"Joueurs: {joueurs_str}", wraplength=300, justify=LEFT)
        self.players_label.pack()
        
        # Ajout de la phrase d'instruction sous la liste des joueurs
        self.instruction_label = Label(self.players_frame, text="Au moment de faire remonter le nom des joueurs, vérifier à ce qu'il corresponde bien à un nom dans la liste.", wraplength=300, justify=LEFT, fg="red")
        self.instruction_label.pack(pady=5)
        
        # Création du canevas
        self.myCanvas = Canvas(self.main_frame, width=WIDTH, height=HEIGHT, bg="white")
        self.myCanvas.pack(side=LEFT)
        
        # Création du plateau de jeu
        self.board = Board(self.myCanvas)
        
        # Frame pour les boutons
        self.button_frame = Frame(self.main_frame)
        self.button_frame.pack(side=RIGHT, padx=10, pady=10)
        
        # Bouton Quitter
        self.quit_button = Button(self.button_frame, text="Quitter", command=self.quit_game)
        self.quit_button.pack(pady=5)
        
        # Bouton Recommencer
        self.restart_button = Button(self.button_frame, text="Recommencer", command=self.restart_game)
        self.restart_button.pack(pady=5)
        
        # Bouton Abandonner / Résultat
        self.result_button = Button(self.button_frame, text="Abandonner / Résultat", command=self.show_result)
        self.result_button.pack(pady=5)
    
    def quit_game(self):
        """Quitte proprement le jeu"""
        self.myWindow.destroy()
    
    def restart_game(self):
        """Réinitialise le plateau de jeu"""
        self.myCanvas.delete("all")
        self.board = Board(self.myCanvas)
    
    def show_result(self):
        """Demande le vainqueur et le perdant, vérifie leur validité et redémarre le jeu"""
        global vainqueur, perdant
        
        while True:
            vainqueur = simpledialog.askstring("Résultat", "Nom du vainqueur :")
            perdant = simpledialog.askstring("Résultat", "Nom du perdant :")
            
            if vainqueur in joueurs and perdant in joueurs:
                break  # Les noms sont corrects, on sort de la boucle
            else:
                messagebox.showerror("Erreur", "Un des noms saisis est incorrect. Vérifiez l'orthographe et réessayez.")
        
        self.restart_game()

if __name__ == "__main__":
    myWindow = Tk()
    app = GameInterface(myWindow)
    myWindow.mainloop()
