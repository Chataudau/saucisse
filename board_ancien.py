from tkinter import *

# Définition des constantes
RADIUS = 5
XMIN = 20
YMIN = 20
DIST = 50
WIDTH = 2 * XMIN + 8 * DIST
HEIGHT = 2 * YMIN + 6 * DIST

class Board:
    def __init__(self, canvas):
        self.canvas = canvas
        self.point = [[None for _ in range(7)] for _ in range(9)]              #ça crée une matrice
        self.selected_points = []                                              # Liste des points sélectionnés
        self.sausages = []                                                     # Liste des saucisses déjà posées
        self.occupied_points = set()                                           # Points déjà utilisés dans une saucisse
        self.current_player = 1                                                # Joueur 1 commence
        self.draw_board()
        
        self.canvas.bind("<Button-1>", self.on_click)                          # Associer un événement de clic sur le canevas
    
    def draw_board(self):
        """Dessine le plateau avec les points. pour les lignes 5 points avec 4 vides = 9
        pour les colonnes 4 points avec 3 vides = 7. Pour (i+j % 2) le prof l'a mis 
        en TD 3 j'aurais jamais trouvé sans. Faire dessin c'est obvious """
        for i in range(9):
            for j in range(7):
                if (i + j) % 2 == 0:                                           # Point 
                    idPoint = self.canvas.create_oval(
                        XMIN + i * DIST - RADIUS, YMIN + j * DIST - RADIUS,
                        XMIN + i * DIST + RADIUS, YMIN + j * DIST + RADIUS,
                        fill="blue", tags=f"point_{i}_{j}"
                    )
                    self.point[i][j] = (idPoint, i, j)
                else:                                                          # vide
                    self.point[i][j] = None
    
    def on_click(self, event):
        """Gère le clic sur un point."""
        x, y = event.x, event.y
        for i in range(9):
            for j in range(7):
                if self.point[i][j] is not None:
                    idPoint, px, py = self.point[i][j]
                    coords = self.canvas.coords(idPoint)
                    x1, y1, x2, y2 = coords
                    if x1 <= x <= x2 and y1 <= y <= y2:                        # en gros on teste si on clique bien sur un point.On regarde si le clic il est dans le carré car il sera pas pile poil au milieux edgar
                        self.select_point(px, py)
                        return                                                 #des qu'on a le bon point on return sinon ils testent d'autres point ce con
    
    def select_point(self, i, j):
        """Ajoute un point sélectionné et gère la création de saucisses."""
        if (i, j) in self.occupied_points:
            return                                                             # Empêcher de sélectionner un point déjà utilisé

        if (i, j) not in self.selected_points:
            self.selected_points.append((i, j))
            color = "red" if self.current_player == 1 else "green"
            self.canvas.itemconfig(self.point[i][j][0], fill=color)
            
        if len(self.selected_points) == 3:
            if self.is_valid_sausage():
                self.draw_sausage()
                self.occupied_points.update(self.selected_points)              # Ajouter ces points comme occupés
                self.current_player = (self.current_player % 2) + 1            # Alterne entre 1 et 2
            else:
                                                                               # Réinitialiser la couleur des points invalides
                for px, py in self.selected_points:
                    self.canvas.itemconfig(self.point[px][py][0], fill="blue")
            self.selected_points = []
    
    def is_valid_sausage(self):
        """Vérifie si les 3 points sélectionnés forment une saucisse valide."""
        x_values = [p[0] for p in self.selected_points]
        y_values = [p[1] for p in self.selected_points]
        return max(x_values) - min(x_values) <= 2 and max(y_values) - min(y_values) <= 2
    
    def draw_sausage(self):
        """Dessine une saucisse entre les points sélectionnés."""
        if self.current_player == 1:                                           # j'ai pas trouvé mieux que de split en 2. On peut pas mettre de il dasn le fill
            for i in range(2):                                                 # besoin que de deux boucles car seulement 2 segments
                self.canvas.create_line(
                    XMIN + self.selected_points[i][0] * DIST,
                    YMIN + self.selected_points[i][1] * DIST,                  #PAS oublier XMIN et YMIN 
                    XMIN + self.selected_points[i+1][0] * DIST,
                    YMIN + self.selected_points[i+1][1] * DIST,
                    width=5, fill="red")
        else: 
            for i in range(2):
                self.canvas.create_line(
                    XMIN + self.selected_points[i][0] * DIST,
                    YMIN + self.selected_points[i][1] * DIST,
                    XMIN + self.selected_points[i+1][0] * DIST,
                    YMIN + self.selected_points[i+1][1] * DIST,
                    width=5, fill="green")
            
