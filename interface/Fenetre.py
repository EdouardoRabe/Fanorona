import tkinter as tk
from tkinter import messagebox  # Importer messagebox pour afficher des boîtes de dialogue
import math 
class Fenetre:
    def __init__(self, jeu):
        self.jeu = jeu
        self.root = tk.Tk()
        self.root.title("Fanoron-telo")
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack()
        self.positions_cercles = {}  # Associe les cercles noirs aux positions logiques
        self.cercles_noirs = []  # Liste des identifiants des cercles noirs
        self.pions_graphiques = {}  # Associe les pions graphiques aux positions logiques
        self.cercle_selectionne = None  # Stocke le pion sélectionné pour le drag-and-drop
        self.position_selectionnee = None  # Stocke la position logique du pion sélectionné
        self.dessiner_plateau()
        self.canvas.bind("<Button-1>", self.clic_souris)
        self.canvas.bind("<B1-Motion>", self.drag_pion)
        self.canvas.bind("<ButtonRelease-1>", self.relacher_pion)

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
            cercle = self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="black")
            self.positions_cercles[cercle] = position
            self.cercles_noirs.append(cercle)  # Ajouter l'identifiant du cercle noir à la liste

    def trouver_cercle_noir_proche(self, x, y):
        """Trouve le cercle noir le plus proche des coordonnées (x, y) avec une tolérance."""
        cercle_proche = None
        distance_min = float('inf')  # Initialiser avec une distance infinie
        tolerance = 20  # Tolérance pour considérer un cercle comme "proche"

        for cercle in self.cercles_noirs:
            x1, y1, x2, y2 = self.canvas.coords(cercle)
            centre_x = (x1 + x2) / 2
            centre_y = (y1 + y2) / 2
            distance = math.sqrt((x - centre_x) ** 2 + (y - centre_y) ** 2)  # Distance euclidienne

            if distance < distance_min and distance <= tolerance:
                distance_min = distance
                cercle_proche = cercle

        return cercle_proche


    def clic_souris(self, event):
        """Gère la sélection d'un pion uniquement en phase de placement."""
        if self.jeu.phase == "deplacement":
            print("Phase de déplacement : utilisez le drag-and-drop pour déplacer un pion.")  # Debug
            return  # Désactiver les clics en phase de déplacement

        x, y = event.x, event.y
        cercle_clique = self.canvas.find_closest(x, y)[0]
        if cercle_clique in self.positions_cercles:
            position = self.positions_cercles[cercle_clique]
            print(f"Utilisateur a cliqué sur la position logique : {position}")  # Debug
            if self.jeu.phase == "placement":
                resultat = self.jeu.jouer_tour_utilisateur(position)
                if resultat == "victoire_utilisateur":
                    print("L'utilisateur a gagné !")
                    messagebox.showinfo("Victoire", "Félicitations ! Vous avez gagné !")
                    self.root.quit()
                elif resultat == "placement_reussi":
                    # Ajouter un pion graphique au-dessus du cercle noir
                    x1, y1, x2, y2 = self.canvas.coords(cercle_clique)
                    pion = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="red")
                    self.pions_graphiques[pion] = position
                    self.jeu.verifier_phase()
                    self.jouer_tour_ia()

    def drag_pion(self, event):
        """Gèrer le deplacement unique quand on drag."""
        if self.jeu.phase == "placement":
            print("Phase de placement : utilisez le clic")  # Debug
            return  # Désactiver les clics en phase de déplacement
        
        """Gère le déplacement du pion avec la souris."""
        if self.cercle_selectionne is None:
            # Sélectionner un pion pour le drag
            x, y = event.x, event.y
            pion_clique = self.canvas.find_closest(x, y)[0]
            if pion_clique in self.pions_graphiques:
                print("Pion sélectionné pour le déplacement.")  # Debug
                self.cercle_selectionne = pion_clique
                self.position_selectionnee = self.pions_graphiques[pion_clique]
        else:
            # Déplacer le pion avec la souris
            print(f"Déplacement en cours : position souris ({event.x}, {event.y})")  # Debug
            self.canvas.coords(self.cercle_selectionne, event.x - 10, event.y - 10, event.x + 10, event.y + 10)

    def relacher_pion(self, event):
        """Gère le relâchement du pion pour valider le déplacement."""
        if self.cercle_selectionne:
            print("Relâchement du pion.")  # Debug
            x, y = event.x, event.y

            # Trouver le cercle noir le plus proche
            cercle_clique = self.trouver_cercle_noir_proche(x, y)
            if cercle_clique:
                position_arrivee = self.positions_cercles[cercle_clique]
                print(f"Position cible : {position_arrivee}")  # Debug

                # Valider le déplacement
                if self.jeu.table_de_jeu.deplacer_pion(self.position_selectionnee, position_arrivee):
                    print("Déplacement validé.")  # Debug
                    self.pions_graphiques[self.cercle_selectionne] = position_arrivee
                else:
                    print("Déplacement invalide. Retour à la position d'origine.")  # Debug
                    x_orig, y_orig = self.canvas.coords(self.cercle_selectionne)[:2]
                    self.canvas.coords(self.cercle_selectionne, x_orig - 10, y_orig - 10, x_orig + 10, y_orig + 10)
            else:
                print("Aucun cercle noir trouvé. Déplacement annulé.")  # Debug

            # Réinitialiser les variables
            self.cercle_selectionne = None
            self.position_selectionnee = None

    def jouer_tour_ia(self):
        """Gère le tour de l'IA."""
        if self.jeu.tour == "ia":
            print("Tour de l'IA.")  # Debug
            resultat = self.jeu.jouer_tour_ia()
            if resultat == "victoire_ia":
                messagebox.showinfo("Défaite", "L'IA a gagné !")
                self.root.quit()
            elif resultat == "placement_reussi":
                position = self.jeu.derniere_position_ia
                cercle_clique = [c for c, pos in self.positions_cercles.items() if pos == position][0]
                x1, y1, x2, y2 = self.canvas.coords(cercle_clique)
                pion = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="blue")
                self.pions_graphiques[pion] = position
            elif resultat == "deplacement_reussi":
                position_depart, position_arrivee = self.jeu.derniere_position_ia
                pion = [p for p, pos in self.pions_graphiques.items() if pos == position_depart][0]
                self.pions_graphiques[pion] = position_arrivee
                x1, y1, x2, y2 = self.canvas.coords([c for c, pos in self.positions_cercles.items() if pos == position_arrivee][0])
                self.canvas.coords(pion, x1 + 5, y1 + 5, x2 - 5, y2 - 5)

    def demarrer(self):
        """Lance la fenêtre."""
        print("Démarrage de la fenêtre.")  # Debug
        self.root.mainloop()

    def clic_souris(self, event):
        """Gère la sélection d'un pion uniquement en phase de placement."""
        if self.jeu.phase == "deplacement":
            print("Phase de déplacement : utilisez le drag-and-drop pour déplacer un pion.")  # Debug
            return  # Désactiver les clics en phase de déplacement

        x, y = event.x, event.y
        cercle_clique = self.canvas.find_closest(x, y)[0]
        if cercle_clique in self.positions_cercles:
            position = self.positions_cercles[cercle_clique]
            print(f"Utilisateur a cliqué sur la position logique : {position}")  # Debug
            if self.jeu.phase == "placement":
                resultat = self.jeu.jouer_tour_utilisateur(position)
                if resultat == "victoire_utilisateur":
                    print("L'utilisateur a gagné !")
                    messagebox.showinfo("Victoire", "Félicitations ! Vous avez gagné !")
                    self.root.quit()
                elif resultat == "placement_reussi":
                    # Ajouter un pion graphique au-dessus du cercle noir
                    x1, y1, x2, y2 = self.canvas.coords(cercle_clique)
                    pion = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="red")
                    self.pions_graphiques[pion] = position
                    self.jeu.verifier_phase()
                    self.jouer_tour_ia()

    def drag_pion(self, event):
        """Gère le déplacement du pion avec la souris."""
        # Désactiver le drag-and-drop pendant la phase de placement
        if self.jeu.phase == "placement":
            print("Phase de placement : le drag-and-drop est désactivé.")  # Debug
            return

        if self.cercle_selectionne is None:
            # Sélectionner un pion pour le drag
            x, y = event.x, event.y
            pion_clique = self.canvas.find_closest(x, y)[0]
            if pion_clique in self.pions_graphiques:
                print("Pion sélectionné pour le déplacement.")  # Debug
                self.cercle_selectionne = pion_clique
                self.position_selectionnee = self.pions_graphiques[pion_clique]
        else:
            # Déplacer le pion avec la souris
            print(f"Déplacement en cours : position souris ({event.x}, {event.y})")  # Debug
            self.canvas.coords(self.cercle_selectionne, event.x - 10, event.y - 10, event.x + 10, event.y + 10)

    def relacher_pion(self, event):
        """Gère le relâchement du pion pour valider le déplacement."""
        if self.cercle_selectionne:
            print("Relâchement du pion.")  # Debug
            x, y = event.x, event.y

            # Trouver le cercle noir le plus proche
            cercle_clique = self.trouver_cercle_noir_proche(x, y)
            if cercle_clique:
                position_arrivee = self.positions_cercles[cercle_clique]
                print(f"Position cible : {position_arrivee}")  # Debug

                # Valider le déplacement
                if self.jeu.table_de_jeu.deplacer_pion(self.position_selectionnee, position_arrivee):
                    print("Déplacement validé.")  # Debug
                    self.pions_graphiques[self.cercle_selectionne] = position_arrivee
                else:
                    print("Déplacement invalide. Retour à la position d'origine.")  # Debug
                    x_orig, y_orig = self.canvas.coords(self.cercle_selectionne)[:2]
                    self.canvas.coords(self.cercle_selectionne, x_orig - 10, y_orig - 10, x_orig + 10, y_orig + 10)
            else:
                print("Aucun cercle noir trouvé. Déplacement annulé.")  # Debug

            # Réinitialiser les variables
            self.cercle_selectionne = None
            self.position_selectionnee = None

    def jouer_tour_ia(self):
        """Gère le tour de l'IA."""
        if self.jeu.tour == "ia":
            print("Tour de l'IA.")  # Debug
            resultat = self.jeu.jouer_tour_ia()
            if resultat == "victoire_ia":
                messagebox.showinfo("Défaite", "L'IA a gagné !")
                self.root.quit()
            elif resultat == "placement_reussi":
                position = self.jeu.derniere_position_ia
                cercle_clique = [c for c, pos in self.positions_cercles.items() if pos == position][0]
                x1, y1, x2, y2 = self.canvas.coords(cercle_clique)
                pion = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="blue")
                self.pions_graphiques[pion] = position
            elif resultat == "deplacement_reussi":
                position_depart, position_arrivee = self.jeu.derniere_position_ia
                pion = [p for p, pos in self.pions_graphiques.items() if pos == position_depart][0]
                self.pions_graphiques[pion] = position_arrivee
                x1, y1, x2, y2 = self.canvas.coords([c for c, pos in self.positions_cercles.items() if pos == position_arrivee][0])
                self.canvas.coords(pion, x1 + 5, y1 + 5, x2 - 5, y2 - 5)

    def demarrer(self):
        """Lance la fenêtre."""
        print("Démarrage de la fenêtre.")  # Debug
        self.root.mainloop()