import tkinter as tk
from tkinter import messagebox  # Importer messagebox pour afficher des boîtes de dialogue

class Fenetre:
    def __init__(self, jeu):
        self.jeu = jeu
        self.root = tk.Tk()
        self.root.title("Fanoron-telo")
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack()
        self.positions_cercles = {}  # Associe les cercles graphiques à leurs positions logiques
        self.coordonnees_logiques = {}  # Associe les positions logiques aux cercles graphiques
        self.dessiner_plateau()
        self.canvas.bind("<Button-1>", self.clic_souris)

    def dessiner_plateau(self):
        """Dessine le plateau de jeu."""
        self.canvas.create_line(50, 50, 350, 50, width=2)  # Ligne horizontale 1
        self.canvas.create_line(50, 200, 350, 200, width=2)  # Ligne horizontale 2
        self.canvas.create_line(50, 350, 350, 350, width=2)  # Ligne horizontale 3
        self.canvas.create_line(50, 50, 50, 350, width=2)  # Ligne verticale 1
        self.canvas.create_line(200, 50, 200, 350, width=2)  # Ligne verticale 2
        self.canvas.create_line(350, 50, 350, 350, width=2)  # Ligne verticale 3
        self.canvas.create_line(50, 50, 350, 350, width=2)  # Diagonale 1
        self.canvas.create_line(350, 50, 50, 350, width=2)  # Diagonale 2

        # Associer les positions logiques aux coordonnées graphiques
        positions_logiques = [
            (0, 0), (0, 1), (0, 2),
            (1, 0), (1, 1), (1, 2),
            (2, 0), (2, 1), (2, 2)
        ]
        coordonnees_visuelles = [
            (50, 50), (200, 50), (350, 50),
            (50, 200), (200, 200), (350, 200),
            (50, 350), (200, 350), (350, 350)
        ]

        for position, (x, y) in zip(positions_logiques, coordonnees_visuelles):
            cercle = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="black")
            self.positions_cercles[cercle] = position
            self.coordonnees_logiques[position] = cercle

    def clic_souris(self, event):
        """Gère les clics de souris pour interagir avec le jeu."""
        x, y = event.x, event.y
        cercle_clique = self.canvas.find_closest(x, y)[0]
        if cercle_clique in self.positions_cercles:
            position = self.positions_cercles[cercle_clique]
            print(f"Utilisateur a cliqué sur la position logique : {position}")  # Debug
            resultat = self.jeu.jouer_tour_utilisateur(position)
            if resultat == "victoire_utilisateur":
                print("L'utilisateur a gagné !")
                messagebox.showinfo("Victoire", "Félicitations ! Vous avez gagné !")
                self.root.quit()
            elif resultat == "placement_reussi":
                self.canvas.itemconfig(cercle_clique, fill="red")
                self.jeu.verifier_phase()
                self.jouer_tour_ia()

    def jouer_tour_ia(self):
        """Gère le tour de l'IA."""
        # Vérifier que l'IA joue uniquement une fois
        if self.jeu.tour == "ia":
            resultat = self.jeu.jouer_tour_ia()
            if resultat == "victoire_ia":
                position = self.jeu.derniere_position_ia  # Nouvelle variable pour stocker la position choisie
                print(f"L'IA a choisi la position logique : {position}")  # Debug
                cercle = self.coordonnees_logiques[position]
                self.canvas.itemconfig(cercle, fill="blue")  # Afficher le dernier coup de l'IA
                messagebox.showinfo("Défaite", "L'IA a gagné !")
                self.root.quit()
            elif resultat == "placement_reussi":
                position = self.jeu.derniere_position_ia  # Nouvelle variable pour stocker la position choisie
                print(f"L'IA a choisi la position logique : {position}")  # Debug
                cercle = self.coordonnees_logiques[position]
                self.canvas.itemconfig(cercle, fill="blue")

    def demarrer(self):
        """Lance la fenêtre."""
        self.root.mainloop()