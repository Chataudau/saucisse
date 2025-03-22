from tkinter import *

# Définition des constantes
RADIUS = 20
XMIN = 20
YMIN = 20
DIST = 50
COLONNES = 9 
LIGNES = 7   
WIDTH = 2 * XMIN + 8 * DIST
HEIGHT = 2 * YMIN + 6 * DIST



class Board:
    def __init__(self, canvas):
        self.canvas = canvas
        self.point = [[None for _ in range(LIGNES)] for _ in range(COLONNES)]  # Création de la matrice
        self.selected_points = []  # Liste des points sélectionnés
        self.sausages = []         # Liste des saucisses déjà posées
        self.occupied_points = set()  # Points déjà utilisés dans une saucisse
        self.current_player = 1    # Le joueur 1 commence
        self.draw_board()          # Dessiner le plateau

    def draw_board(self):
        """Dessine le plateau avec les points."""
        for col in range(COLONNES):
            for ligne in range(LIGNES):
                if (col + ligne) % 2 == 0:  
                    idPoint = self.canvas.create_oval(
                        XMIN + col * DIST - RADIUS, YMIN + ligne * DIST - RADIUS,
                        XMIN + col * DIST + RADIUS, YMIN + ligne * DIST + RADIUS,
                        fill="blue", tags=f"point_{col}_{ligne}"
                    )
                    self.point[col][ligne] = (idPoint, col, ligne)
                    self.canvas.tag_bind(idPoint, "<Button-1>", lambda event, col=col, ligne=ligne: self.select_point(col, ligne))
                else:  
                    self.point[col][ligne] = None

    def select_point(self, col, ligne):
        """Ajoute un point sélectionné et gère la création de saucisses."""
        if (col, ligne) in self.occupied_points:
            return  # Empêcher de sélectionner un point déjà utilisé

        if (col, ligne) not in self.selected_points:
            self.selected_points.append((col, ligne))
            color = "red" if self.current_player == 1 else "green"
            self.canvas.itemconfig(self.point[col][ligne][0], fill=color)
        
        if len(self.selected_points) == 3:
            if self.is_valid_sausage():
                self.draw_sausage()
                self.occupied_points.update(self.selected_points)  # Ajouter ces points comme occupés
                self.current_player = (self.current_player % 2) + 1  # Alterne entre 1 et 2
            else:
                # Réinitialiser la couleur des points invalides
                for col, ligne in self.selected_points:
                    self.canvas.itemconfig(self.point[col][ligne][0], fill="blue")
            self.selected_points = []

    def point_bloque(self, col, ligne):
        """Marque un point comme bloqué s'il n'a pas au moins deux voisins valides dans un rayon de 2 colonnes ou 2 lignes max."""
        directions = [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (-2, 2), (2, -2), (2, 2),                                                #certains cas ou ça ne marche pas
                 (1, 1), (-1, -1), (1, -1), (-1, 1)]  # Diagonales immédiates à 1 unité

        valid_neighbors = 0  # Compte le nombre de voisins valides

        # Vérifier si le point a des voisins valides dans les directions possibles
        for dx, dy in directions:
            new_col = col + dx
            new_ligne = ligne + dy
        
            # Vérifier si les nouvelles coordonnées sont valides et à l'intérieur du plateau
            if 0 <= new_col < COLONNES and 0 <= new_ligne < LIGNES:
                # Si le voisin est valide et n'est pas déjà occupé (bloqué)
                if (new_col, new_ligne) not in self.occupied_points:
                    valid_neighbors += 1
        
        # Si on a trouvé 2 voisins valides, le point n'est pas bloqué
            if valid_neighbors >= 2:
                return

    # Si moins de 2 voisins valides sont trouvés, on marque le point comme bloqué
        self.canvas.itemconfig(self.point[col][ligne][0], fill="black")  # Change la couleur du point en noir
        self.occupied_points.add((col, ligne))  # Ajouter le point à l'ensemble des points bloqués



    def end_turn(self):
        """Fin de tour, vérifie et marque les points bloqués sur le plateau."""
        # Appeler point_bloque pour chaque point après chaque tour
        for col in range(COLONNES):
            for ligne in range(LIGNES):
                if (col, ligne) not in self.occupied_points:  # Ne vérifier que les points non occupés
                    self.point_bloque(col, ligne)  # Vérifie et marque les points bloqués

    def is_valid_sausage(self):
        """Vérifie si les 3 points sélectionnés forment une saucisse valide."""
        col_values = [p[0] for p in self.selected_points]
        ligne_values = [p[1] for p in self.selected_points]
        return max(col_values) - min(col_values) <= 2 and max(ligne_values) - min(ligne_values) <= 2

    def draw_sausage(self):
        """Dessine une saucisse entre les points sélectionnés."""
        color = "red" if self.current_player == 1 else "green"
        for i in range(2):  # Besoin de deux boucles pour dessiner seulement deux segments
            self.canvas.create_line(
                XMIN + self.selected_points[i][0] * DIST,
                YMIN + self.selected_points[i][1] * DIST,
                XMIN + self.selected_points[i+1][0] * DIST,
                YMIN + self.selected_points[i+1][1] * DIST,
                width=5, fill=color)
        


