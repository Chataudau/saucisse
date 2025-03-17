from tkinter import *
from tkinter import simpledialog, messagebox
from board import Board, WIDTH, HEIGHT

vainqueur = ""
perdant = ""
joueur1 = ""                                                                   # Les variables globales pour stocker vainqueur/perdant/joeur 1 et joueur 2
joueur2 = ""

with open("noms.txt", "r", encoding="utf-8") as f:
    joueurs = f.readlines()[1:]                                                # Ignore la première ligne du fichier noms.txt
    joueurs = [nom.strip() for nom in joueurs]                                 #Supprime les espaces et caracteres de retour a la ligne 
    joueurs_lower = {nom.lower(): nom for nom in joueurs}                      # Dictionnaire pour gérer la separation
    joueurs_str = " | ".join(joueurs)                                          # Mettre les noms sur une seule ligne séparés par  | 

class GameInterface:
    def __init__(self, myWindow):
        self.myWindow = myWindow
        self.myWindow.title("Jeu de Plateau")
        
        self.main_frame = Frame(myWindow)                                      #creer le cadre principale
        self.main_frame.pack()
         
        self.players_frame = Frame(self.main_frame)                            # Affiche la liste des joueurs sur le cote
        self.players_frame.pack(side=LEFT, padx=10, pady=10)                   # padx / pady permet de laisser 10 pixel de chaque cote de l'objet
        self.players_label = Label(self.players_frame, text=f"Joueurs: {joueurs_str}", wraplength=300, justify=LEFT)  #wraplength et justify permettent de bien faire afficher les noms
        self.players_label.pack()
        
        self.instruction_label = Label(self.players_frame, text="Au moment de faire remonter le nom des joueurs, vérifier à ce qu'il corresponde bien à un nom dans la liste.", wraplength=300, justify=LEFT, fg="red")
        self.instruction_label.pack(pady=5)                                    # Ajoute la phrase sous la liste des joueurs
        
        self.myCanvas = Canvas(self.main_frame, width=WIDTH, height=HEIGHT, bg="white")     # Creer le canvas
        self.myCanvas.pack(side=LEFT)
        
        self.board = Board(self.myCanvas)                                      # Creer le plateau de jeu
        
        self.button_frame = Frame(self.main_frame)
        self.button_frame.pack(side=RIGHT, padx=10, pady=10)                   #frame pour les boutons
        
        self.quit_button = Button(self.button_frame, text="Quitter", command=self.quit_game)   #bouton quitter
        self.quit_button.pack(pady=5)
        
        self.restart_button = Button(self.button_frame, text="Recommencer avec de nouveaux joueurs", command=self.restart_game)   #bouton recommencer
        self.restart_button.pack(pady=5)
        
        self.result_button = Button(self.button_frame, text="Abandonner / Résultat", command=self.show_result)  #bouton abandonner
        self.result_button.pack(pady=5)
        
        self.ask_player_names()                                                # Demande les noms des joueurs apres que l'interface soit chargee
    
    def ask_player_names(self):
        """Demande les noms des joueurs au début du jeu en gérant les espaces et la separation."""
        global joueur1, joueur2
        while True:
            joueur1_input = simpledialog.askstring("Nom du Joueur 1", "Entrez le nom du Joueur 1:")
            joueur2_input = simpledialog.askstring("Nom du Joueur 2", "Entrez le nom du Joueur 2:")
            
            joueur1_clean = joueurs_lower.get(joueur1_input.strip().lower())
            joueur2_clean = joueurs_lower.get(joueur2_input.strip().lower())
            
            if joueur1_clean and joueur2_clean and joueur1_clean != joueur2_clean:
                joueur1, joueur2 = joueur1_clean, joueur2_clean
                break
            else:
                messagebox.showerror("Erreur", "Les noms des joueurs doivent être dans la liste et ne pas être identiques.")
    
    def quit_game(self):
        """Quitte le jeu"""
        self.myWindow.destroy()
    
    def restart_game(self, demander_noms=True):
        """Réinitialise le plateau de jeu et redemande les noms si nécessaire"""
        self.myCanvas.delete("all")
        self.board = Board(self.myCanvas)
        if demander_noms:
            self.ask_player_names()
    
    def show_result(self):
        """Attribue la victoire au dernier joueur ayant joué et affiche le résultat"""
        global vainqueur, perdant
        dernier_joueur = joueur1 if self.board.current_player == 2 else joueur2
        perdant = joueur2 if dernier_joueur == joueur1 else joueur1
        vainqueur = dernier_joueur
        
        messagebox.showinfo("Résultat", f"Le vainqueur est {vainqueur}!")
        self.restart_game(demander_noms=False)                                 # ne redemande pas les noms apres abandon

if __name__ == "__main__":
    myWindow = Tk()
    app = GameInterface(myWindow)
    myWindow.mainloop()
