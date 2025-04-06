import tkinter as tk
from tkinter import messagebox 
import math 
class Fenetre:
    def __init__(self, jeu):
        self.jeu = jeu
        self.root = tk.Tk()
        self.root.title("Fanoron-telo")
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="white")
        self.canvas.pack()
        self.positions_cercles = {}  
        self.cercles_noirs = []  
        self.pions_graphiques = {}  
        self.cercle_selectionne = None 
        self.position_selectionnee = None  
        self.dessiner_plateau()
        self.canvas.bind("<Button-1>", self.clic_souris)
        self.canvas.bind("<B1-Motion>", self.drag_pion)
        self.canvas.bind("<ButtonRelease-1>", self.relacher_pion)

    def dessiner_plateau(self):
        self.canvas.create_line(50, 50, 350, 50, width=2) 
        self.canvas.create_line(50, 200, 350, 200, width=2) 
        self.canvas.create_line(50, 350, 350, 350, width=2)  
        self.canvas.create_line(50, 50, 50, 350, width=2)  
        self.canvas.create_line(200, 50, 200, 350, width=2)  
        self.canvas.create_line(350, 50, 350, 350, width=2)  
        self.canvas.create_line(50, 50, 350, 350, width=2)  
        self.canvas.create_line(350, 50, 50, 350, width=2)  
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
            self.cercles_noirs.append(cercle)  

    def trouver_cercle_noir_proche(self, x, y):
        cercle_proche = None
        distance_min = float('inf')  
        tolerance = 20  
        for cercle in self.cercles_noirs:
            x1, y1, x2, y2 = self.canvas.coords(cercle)
            centre_x = (x1 + x2) / 2
            centre_y = (y1 + y2) / 2
            distance = math.sqrt((x - centre_x) ** 2 + (y - centre_y) ** 2)  
            if distance < distance_min and distance <= tolerance:
                distance_min = distance
                cercle_proche = cercle
        return cercle_proche


    def clic_souris(self, event):
        if self.jeu.phase == "deplacement":
            print("Phase de déplacement : utilisez le drag-and-drop pour déplacer un pion.")  
            return 
        x, y = event.x, event.y
        cercle_clique = self.canvas.find_closest(x, y)[0]
        if cercle_clique in self.positions_cercles:
            position = self.positions_cercles[cercle_clique]
            print(f"Utilisateur a cliqué sur la position logique : {position}")  
            if self.jeu.phase == "placement":
                resultat = self.jeu.jouer_tour_utilisateur(position)
                if resultat == "victoire_utilisateur":
                    print("L'utilisateur a gagné !")
                    messagebox.showinfo("Victoire", "Félicitations ! Vous avez gagné !")
                    self.root.quit()
                elif resultat == "placement_reussi":
                    x1, y1, x2, y2 = self.canvas.coords(cercle_clique)
                    pion = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="red")
                    self.pions_graphiques[pion] = position
                    self.jeu.verifier_phase()
                    self.jouer_tour_ia()

    def drag_pion(self, event):
        if self.jeu.phase == "placement":
            print("Phase de placement : utilisez le clic")  
            return  
        if self.cercle_selectionne is None:
            x, y = event.x, event.y
            pion_clique = self.canvas.find_closest(x, y)[0]
            if pion_clique in self.pions_graphiques:
                print("Pion sélectionné pour le déplacement.")  
                self.cercle_selectionne = pion_clique
                self.position_selectionnee = self.pions_graphiques[pion_clique]
        else:
            print(f"Déplacement en cours : position souris ({event.x}, {event.y})")  
            self.canvas.coords(self.cercle_selectionne, event.x - 10, event.y - 10, event.x + 10, event.y + 10)

    def relacher_pion(self, event):
        if self.cercle_selectionne:
            print("Relâchement du pion.")  
            x, y = event.x, event.y
            cercle_clique = self.trouver_cercle_noir_proche(x, y)
            if cercle_clique:
                position_arrivee = self.positions_cercles[cercle_clique]
                print(f"Position cible : {position_arrivee}")  
                resultat = self.jeu.jouer_tour_utilisateur(position_depart=self.position_selectionnee, position_arrivee=position_arrivee)
                if resultat == "deplacement_reussi":
                    print("Déplacement validé.")  
                    self.pions_graphiques[self.cercle_selectionne] = position_arrivee
                    x1, y1, x2, y2 = self.canvas.coords(cercle_clique)
                    self.canvas.coords(self.cercle_selectionne, x1 + 5, y1 + 5, x2 - 5, y2 - 5)
                    self.jouer_tour_ia()  
                elif resultat == "victoire_utilisateur":
                    print("L'utilisateur a gagné !")
                    messagebox.showinfo("Victoire", "Félicitations ! Vous avez gagné !")
                    self.root.quit()
                else:
                    print("Déplacement invalide. Retour à la position d'origine.")  
                    x_orig, y_orig = self.canvas.coords(self.cercle_selectionne)[:2]
                    self.canvas.coords(self.cercle_selectionne, x_orig - 10, y_orig - 10, x_orig + 10, y_orig + 10)
            else:
                print("Aucun cercle noir trouvé. Déplacement annulé.")  
            self.cercle_selectionne = None
            self.position_selectionnee = None

    def jouer_tour_ia(self):
        if self.jeu.tour == "ia":
            print("Tour de l'IA.")  
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
        print("Démarrage de la fenêtre.")  
        self.root.mainloop()

    def clic_souris(self, event):
        if self.jeu.phase == "deplacement":
            print("Phase de déplacement : utilisez le drag-and-drop pour déplacer un pion.")  
            return  
        x, y = event.x, event.y
        cercle_clique = self.canvas.find_closest(x, y)[0]
        if cercle_clique in self.positions_cercles:
            position = self.positions_cercles[cercle_clique]
            print(f"Utilisateur a cliqué sur la position logique : {position}")  
            if self.jeu.phase == "placement":
                resultat = self.jeu.jouer_tour_utilisateur(position)
                if resultat == "victoire_utilisateur":
                    print("L'utilisateur a gagné !")
                    messagebox.showinfo("Victoire", "Félicitations ! Vous avez gagné !")
                    self.root.quit()
                elif resultat == "placement_reussi":
                    x1, y1, x2, y2 = self.canvas.coords(cercle_clique)
                    pion = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="red")
                    self.pions_graphiques[pion] = position
                    self.jeu.verifier_phase()
                    self.jouer_tour_ia()

    def drag_pion(self, event):
        if self.jeu.phase == "placement":
            print("Phase de placement : le drag-and-drop est désactivé.")  
            return

        if self.cercle_selectionne is None:
            x, y = event.x, event.y
            pion_clique = self.canvas.find_closest(x, y)[0]
            if pion_clique in self.pions_graphiques:
                position = self.pions_graphiques[pion_clique]
                if self.jeu.table_de_jeu.plateau[position].couleur == "rouge":  
                    print("Pion sélectionné pour le déplacement.") 
                    self.cercle_selectionne = pion_clique
                    self.position_selectionnee = position
                    self.coords_orig = self.canvas.coords(self.cercle_selectionne)
                else:
                    print("Vous ne pouvez pas déplacer un pion de l'IA.")  
        else:
            print(f"Déplacement en cours : position souris ({event.x}, {event.y})")  
            self.canvas.coords(self.cercle_selectionne, event.x - 10, event.y - 10, event.x + 10, event.y + 10)

    def relacher_pion(self, event):
        if self.cercle_selectionne:
            print("Relâchement du pion.")  
            x, y = event.x, event.y
            cercle_clique = self.trouver_cercle_noir_proche(x, y)
            if cercle_clique:
                position_arrivee = self.positions_cercles[cercle_clique]
                print(f"Position cible : {position_arrivee}")  
                resultat = self.jeu.jouer_tour_utilisateur(position_depart=self.position_selectionnee, position_arrivee=position_arrivee)
                if resultat == "deplacement_reussi":
                    print("Déplacement validé.")  
                    self.pions_graphiques[self.cercle_selectionne] = position_arrivee
                    x1, y1, x2, y2 = self.canvas.coords(cercle_clique)
                    self.canvas.coords(self.cercle_selectionne, x1 + 5, y1 + 5, x2 - 5, y2 - 5)
                    self.jouer_tour_ia()
                elif resultat == "victoire_utilisateur":
                    print("L'utilisateur a gagné !")
                    messagebox.showinfo("Victoire", "Félicitations ! Vous avez gagné !")
                    self.root.quit()
                else:
                    print("Déplacement invalide. Retour à la position d'origine.")  
                    self.canvas.coords(self.cercle_selectionne, *self.coords_orig)
            else:
                print("Aucun cercle noir trouvé. Déplacement annulé.")  
                self.canvas.coords(self.cercle_selectionne, *self.coords_orig)
            self.cercle_selectionne = None
            self.position_selectionnee = None
            self.coords_orig = None

    def jouer_tour_ia(self):
        if self.jeu.tour == "ia":
            print("Tour de l'IA.") 
            resultat = self.jeu.jouer_tour_ia()
            if resultat == "victoire_ia":
                if self.jeu.phase == "placement":
                    position = self.jeu.derniere_position_ia
                    cercle_clique = [c for c, pos in self.positions_cercles.items() if pos == position][0]
                    x1, y1, x2, y2 = self.canvas.coords(cercle_clique)
                    pion = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill="blue")
                    self.pions_graphiques[pion] = position
                else:
                    position_depart, position_arrivee = self.jeu.derniere_position_ia
                    pion = [p for p, pos in self.pions_graphiques.items() if pos == position_depart][0]
                    self.pions_graphiques[pion] = position_arrivee
                    x1, y1, x2, y2 = self.canvas.coords([c for c, pos in self.positions_cercles.items() if pos == position_arrivee][0])
                    self.canvas.coords(pion, x1 + 5, y1 + 5, x2 - 5, y2 - 5)
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
        print("Démarrage de la fenêtre.")  
        self.root.mainloop()