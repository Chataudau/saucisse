from tkinter import *
from tkinter import messagebox
from board import Board
import time

RADIUS = 20
XMIN = 20
YMIN = 20
DIST = 50
COLONNES = 9 
LIGNES = 7   
WIDTH = 2 * XMIN + 8 * DIST
HEIGHT = 2 * YMIN + 6 * DIST


class Game:
    def __init__(self, canvas):
        self.board = Board(canvas)  # Créer une instance de la classe Board
        self.current_player = 1  # Le joueur Rouge commence (1 = Rouge, 2 = Vert)
        self.game_over = False   # Variable pour savoir si la partie est terminée
        self.turn_completed = [False, False]  # Liste pour suivre si chaque joueur a terminé son tour
        self.game_active = True  # Indicateur pour savoir si le joueur peut encore jouer

        # Temps de départ pour chaque joueur (en secondes) par coup
        self.turn_time = 15
        self.start_time = {1: None, 2: None}  # Heure de début du tour de chaque joueur
        self.remaining_time = {1: self.turn_time, 2: self.turn_time}  # Temps restant pour chaque joueur

        # Crée un label pour afficher le temps
        self.time_label = Label(root, text=f"Temps Rouge: {self.format_time(self.remaining_time[1])}   Temps Vert: {self.format_time(self.remaining_time[2])}", font=("Helvetica", 14))
        self.time_label.pack()

        # Démarrer immédiatement le décompte du temps pour le joueur Rouge
        self.start_timer()

    def format_time(self, seconds):
        """Formate le temps en minutes:secondes et arrondi à la seconde."""
        seconds = int(seconds)  # Arrondi à la seconde
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def start_timer(self):
        """Démarre le timer pour le joueur Rouge et Vert (10 secondes par coup)."""
        self.start_time[1] = time.time()  # Démarre le timer pour le joueur Rouge
        self.update_time()

    def update_time(self):
        """Met à jour le temps restant pour chaque joueur."""
        if not self.game_over:
            if self.start_time[self.current_player] is not None:
                elapsed_time = time.time() - self.start_time[self.current_player]
                self.remaining_time[self.current_player] = max(0, self.turn_time - elapsed_time)  # Le temps restant pour le joueur

            # Si le temps est écoulé pour un joueur, il a perdu
            if self.remaining_time[self.current_player] <= 0:
                self.game_over = True
                messagebox.showinfo("Fin de la partie", f"Le joueur {'Rouge' if self.current_player == 1 else 'Vert'} a perdu !")
                return

            # Mise à jour de l'affichage du temps
            self.time_label.config(text=f"Temps Rouge: {self.format_time(self.remaining_time[1])}   Temps Vert: {self.format_time(self.remaining_time[2])}")

            # Continuer le décompte du temps à chaque intervalle de 100ms
            root.after(100, self.update_time)

    def play_turn(self):
        """Gère un tour de jeu, change de joueur et vérifie l'état des points."""
        if self.game_over:
            return  # Si la partie est terminée, on ne joue plus

        # Si le joueur a déjà fait une saucisse, il ne peut pas en refaire jusqu'à ce qu'il passe son tour
        if self.turn_completed[self.current_player - 1]:
            messagebox.showinfo("Tour du joueur", f"Le joueur {'Rouge' if self.current_player == 1 else 'Vert'} doit attendre son tour.")
            return  # Le joueur ne peut pas jouer tant qu'il a déjà fait une saucisse

        # Appelle end_turn pour vérifier les points bloqués
        self.board.end_turn()

        # Marquer le tour comme complété pour ce joueur
        self.turn_completed[self.current_player - 1] = True

        # Change de joueur automatiquement après avoir créé une saucisse
        self.current_player = 1 if self.current_player == 2 else 2

        # Permet au nouvel autre joueur de jouer
        self.turn_completed[self.current_player - 1] = False  # Le joueur qui vient de passer son tour peut maintenant jouer

        # Redémarre le timer pour l'autre joueur (reset du temps de 10 secondes)
        self.start_time[self.current_player] = time.time()  # Définir l'heure de début pour le joueur suivant

        # Afficher un message indiquant que le tour est terminé
        print(f"Joueur {'Rouge' if self.current_player == 1 else 'Vert'} a joué.")
        self.update_time_display()

    def update_time_display(self):
        """Met à jour l'affichage du temps restant pour les deux joueurs."""
        self.time_label.config(text=f"Temps Rouge: {self.format_time(self.remaining_time[1])}   Temps Vert: {self.format_time(self.remaining_time[2])}")
        if self.remaining_time[1] <= 0 or self.remaining_time[2] <= 0:
            self.game_over = True
            winner = 2 if self.remaining_time[1] <= 0 else 1
            messagebox.showinfo("Fin de la partie", f"Le joueur {'Rouge' if winner == 1 else 'Vert'} a gagné !")

    def quit_game(self):
        """Ferme la fenêtre du jeu."""
        print("Le jeu est fermé.")
        root.quit()

    def surrender(self):
        """Abandonne la partie et affiche qui a gagné."""
        if self.current_player == 1:
            winner = 2
        else:
            winner = 1
        
        messagebox.showinfo("Fin de la partie", f"Le joueur {'Rouge' if winner == 1 else 'Vert'} a gagné !")
        self.game_over = True  # Marquer la fin de la partie pour empêcher d'autres tours


# Configuration de l'interface utilisateur
root = Tk()
root.title("Jeu de Plateau")

# Création du canvas
canvas = Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

# Créer une instance du jeu
game = Game(canvas)

# Bouton pour quitter le jeu
quit_button = Button(root, text="Quitter", command=game.quit_game)
quit_button.pack(pady=5)

# Bouton pour abandonner et afficher le gagnant
surrender_button = Button(root, text="Abandonner", command=game.surrender)
surrender_button.pack(pady=5)

# Bouton pour jouer un tour (juste pour tester)
play_button = Button(root, text="Jouer un tour", command=game.play_turn)
play_button.pack(pady=5)

root.mainloop()







