import tkinter as tk
from tkinter import messagebox
import math

class Fenetre:
    USER_COLOR = "#2ecc40"  
    IA_COLOR = "#e74c3c"   
    SUGGEST_COLOR = "#f1c40f" 

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
        self.mode_joueur2 = False
        self.suggestion_cercle = None 
        self.dessiner_plateau()
        self.canvas.bind("<Button-1>", self.clic_souris)  
        self.canvas.bind("<Button-3>", self.bannir_position)  
        self.canvas.bind("<B1-Motion>", self.drag_pion)
        self.canvas.bind("<ButtonRelease-1>", self.relacher_pion)
        self.root.bind("<Key>", self.key_press)

    def key_press(self, event):
        if event.char.lower() == 'x' and self.jeu.phase == "deplacement" and self.jeu.tour == "utilisateur":
            print("Le joueur a passé son tour. L'IA joue.")
            self.jeu.tour = "ia"
            self.jouer_tour_ia()
        elif event.char.lower() == 'j':
            print("Mode Joueur vs Joueur activé : le joueur 2 remplace l'IA.")
            self.mode_joueur2 = True
        elif event.char.lower() == 'i':
            print("Mode Joueur vs IA activé : l'IA reprend le contrôle du joueur 2.")
            self.mode_joueur2 = False
        elif event.char.lower() == 'a' and (self.mode_joueur2 or self.jeu.tour == "utilisateur"):
            if self.suggestion_cercle is not None:
                self.canvas.itemconfig(self.suggestion_cercle, fill="black")
                self.suggestion_cercle = None
            if self.jeu.phase == "placement":
                couleur = self.USER_COLOR if self.jeu.tour == "utilisateur" else self.IA_COLOR
                autre = self.IA_COLOR if self.jeu.tour == "utilisateur" else self.USER_COLOR
                coup = self.jeu.minimax.meilleur_coup_placement(couleur, autre)
                if coup is not None:
                    print(f"Suggestion IA pour {'Joueur 1' if self.jeu.tour == 'utilisateur' else 'Joueur 2'} (placement): placez à {coup}")
                    for cercle, pos in self.positions_cercles.items():
                        if pos == coup:
                            self.canvas.itemconfig(cercle, fill=self.SUGGEST_COLOR)
                            self.suggestion_cercle = cercle
                            break
                else:
                    print("Aucune suggestion IA possible pour ce placement.")
            elif self.jeu.phase == "deplacement":
                couleur = self.USER_COLOR if self.jeu.tour == "utilisateur" else self.IA_COLOR
                autre = self.IA_COLOR if self.jeu.tour == "utilisateur" else self.USER_COLOR
                coup = self.jeu.minimax.meilleur_coup_deplacement(couleur, autre)
                if coup is not None:
                    print(f"Suggestion IA pour {'Joueur 1' if self.jeu.tour == 'utilisateur' else 'Joueur 2'} (déplacement): déplacez de {coup[0]} vers {coup[1]}")
                    for cercle, pos in self.positions_cercles.items():
                        if pos == coup[1]:
                            self.canvas.itemconfig(cercle, fill=self.SUGGEST_COLOR)
                            self.suggestion_cercle = cercle
                            break
                else:
                    print("Aucune suggestion IA possible pour ce déplacement.")

    def bannir_position(self, event):
        x, y = event.x, event.y
        cercle_clique = self.canvas.find_closest(x, y)[0]
        if cercle_clique in self.positions_cercles:
            position = self.positions_cercles[cercle_clique]
            print(f"Utilisateur a cliqué droit sur la position logique : {position}")
            if self.jeu.table_de_jeu.est_position_valide(position):
                if self.jeu.table_de_jeu.bannir_position(position):
                    print(f"Position bannie : {position}")
                    self.canvas.itemconfig(cercle_clique, fill="gray")  
                else:
                    print(f"Impossible de bannir la position : {position} (déjà occupée ou bannie).")
            else:
                print(f"Position invalide pour le bannissement : {position}.")

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
        if self.suggestion_cercle is not None:
            self.canvas.itemconfig(self.suggestion_cercle, fill="black")
            self.suggestion_cercle = None
        x, y = event.x, event.y
        cercle_clique = self.canvas.find_closest(x, y)[0]
        if cercle_clique not in self.positions_cercles:
            return
        position = self.positions_cercles[cercle_clique]
        print(f"Utilisateur a cliqué sur la position logique : {position}")
        if self.mode_joueur2:
            if self.jeu.phase == "placement":
                couleur = self.USER_COLOR if self.jeu.tour == "utilisateur" else self.IA_COLOR
                pions_places = sum(1 for pion in self.jeu.table_de_jeu.plateau.values() if pion is not None and pion.couleur == couleur)
                if pions_places == 0 and position == (1, 1):
                    print("Placement invalide : le premier pion ne peut pas être placé au centre.")
                    return
                if position in self.jeu.table_de_jeu.positions_bannies:
                    print("Placement invalide : la position est bannie.")
                    return
                pion = self.jeu.pions_utilisateur[0] if self.jeu.tour == "utilisateur" else self.jeu.pions_ia[0]
                if self.jeu.table_de_jeu.placer_pion(position, pion):
                    if self.jeu.tour == "utilisateur":
                        self.jeu.pions_utilisateur.pop(0)
                    else:
                        self.jeu.pions_ia.pop(0)
                    x1, y1, x2, y2 = self.canvas.coords(cercle_clique)
                    color = self.USER_COLOR if self.jeu.tour == "utilisateur" else self.IA_COLOR
                    pion_graph = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=color)
                    self.pions_graphiques[pion_graph] = position
                    if self.jeu.table_de_jeu.verifier_victoire(couleur):
                        print(f"{'Joueur 1' if self.jeu.tour == "utilisateur" else 'Joueur 2'} a gagné !")
                        messagebox.showinfo("Victoire", f"Félicitations ! {'Joueur 1' if self.jeu.tour == "utilisateur" else 'Joueur 2'} a gagné !")
                        self.root.quit()
                    self.jeu.verifier_phase()
                    self.jeu.tour = "ia" if self.jeu.tour == "utilisateur" else "utilisateur"
            return
        if self.jeu.phase == "deplacement":
            print("Phase de déplacement : utilisez le drag-and-drop pour déplacer un pion.")
            return
        pions_places_joueur = sum(1 for pion in self.jeu.table_de_jeu.plateau.values() if pion is not None and pion.couleur == self.USER_COLOR)
        if self.jeu.phase == "placement" and self.jeu.tour == "utilisateur" and pions_places_joueur == 0 and position == (1, 1):
            print("Placement invalide : le premier pion ne peut pas être placé au centre.")
            return
        if position in self.jeu.table_de_jeu.positions_bannies:
            print("Placement invalide : la position est bannie.")
            return
        if self.jeu.phase == "placement":
            resultat = self.jeu.jouer_tour_utilisateur(position)
            if resultat == "victoire_utilisateur":
                print("L'utilisateur a gagné !")
                messagebox.showinfo("Victoire", "Félicitations ! Vous avez gagné !")
                self.root.quit()
            elif resultat == "placement_reussi":
                x1, y1, x2, y2 = self.canvas.coords(cercle_clique)
                pion = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=self.USER_COLOR)
                self.pions_graphiques[pion] = position
                self.jeu.verifier_phase()
                self.jouer_tour_ia()

    def drag_pion(self, event):
        if self.jeu.phase == "placement":
            print("Phase de placement : utilisez le clic")
            return
        if self.mode_joueur2:
            if self.cercle_selectionne is None:
                x, y = event.x, event.y
                pion_clique = self.canvas.find_closest(x, y)[0]
                if pion_clique in self.pions_graphiques:
                    position = self.pions_graphiques[pion_clique]
                    pion_plateau = self.jeu.table_de_jeu.plateau.get(position)
                    if pion_plateau is not None and (pion_plateau.couleur == self.USER_COLOR or pion_plateau.couleur == self.IA_COLOR):
                        print("Pion sélectionné pour le déplacement.")
                        self.cercle_selectionne = pion_clique
                        self.position_selectionnee = position
            else:
                self.canvas.coords(self.cercle_selectionne, event.x - 10, event.y - 10, event.x + 10, event.y + 10)
        else:
            if self.cercle_selectionne is None:
                x, y = event.x, event.y
                pion_clique = self.canvas.find_closest(x, y)[0]
                if pion_clique in self.pions_graphiques:
                    position = self.pions_graphiques[pion_clique]
                    pion_plateau = self.jeu.table_de_jeu.plateau.get(position)
                    if pion_plateau is not None and pion_plateau.couleur != self.USER_COLOR:
                        print("Vous ne pouvez pas déplacer un pion de l'IA.")
                        return
                    print("Pion sélectionné pour le déplacement.")
                    self.cercle_selectionne = pion_clique
                    self.position_selectionnee = position
            else:
                self.canvas.coords(self.cercle_selectionne, event.x - 10, event.y - 10, event.x + 10, event.y + 10)

    def relacher_pion(self, event):
        if self.suggestion_cercle is not None:
            self.canvas.itemconfig(self.suggestion_cercle, fill="black")
            self.suggestion_cercle = None
        if self.mode_joueur2:
            if self.cercle_selectionne:
                print("Relâchement du pion.")
                x, y = event.x, event.y
                cercle_clique = self.trouver_cercle_noir_proche(x, y)
                if cercle_clique:
                    position_arrivee = self.positions_cercles[cercle_clique]
                    print(f"Position cible : {position_arrivee}")
                    if position_arrivee in self.jeu.table_de_jeu.positions_bannies:
                        print("Déplacement invalide : la position cible est bannie.")
                        cercle_origine = [c for c, pos in self.positions_cercles.items() if pos == self.position_selectionnee][0]
                        x1, y1, x2, y2 = self.canvas.coords(cercle_origine)
                        self.canvas.coords(self.cercle_selectionne, x1 + 5, y1 + 5, x2 - 5, y2 - 5)
                    else:
                        print(f"Déplacement du pion de {self.position_selectionnee} à {position_arrivee}.")
                        couleur = self.USER_COLOR if self.jeu.tour == "utilisateur" else self.IA_COLOR
                        resultat = self.jeu.table_de_jeu.deplacer_pion(self.position_selectionnee, position_arrivee)
                        if resultat:
                            if self.jeu.table_de_jeu.verifier_victoire(couleur):
                                print(f"{'Joueur 1' if self.jeu.tour == 'utilisateur' else 'Joueur 2'} a gagné !")
                                messagebox.showinfo("Victoire", f"Félicitations ! {'Joueur 1' if self.jeu.tour == 'utilisateur' else 'Joueur 2'} a gagné !")
                                self.root.quit()
                            self.pions_graphiques[self.cercle_selectionne] = position_arrivee
                            x1, y1, x2, y2 = self.canvas.coords(cercle_clique)
                            self.canvas.coords(self.cercle_selectionne, x1 + 5, y1 + 5, x2 - 5, y2 - 5)
                            self.jeu.tour = "ia" if self.jeu.tour == "utilisateur" else "utilisateur"
                        else:
                            print("Déplacement invalide. Retour à la position d'origine.")
                            cercle_origine = [c for c, pos in self.positions_cercles.items() if pos == self.position_selectionnee][0]
                            x1, y1, x2, y2 = self.canvas.coords(cercle_origine)
                            self.canvas.coords(self.cercle_selectionne, x1 + 5, y1 + 5, x2 - 5, y2 - 5)
                else:
                    print("Aucun cercle noir trouvé. Déplacement annulé.")
                    cercle_origine = [c for c, pos in self.positions_cercles.items() if pos == self.position_selectionnee][0]
                    x1, y1, x2, y2 = self.canvas.coords(cercle_origine)
                    self.canvas.coords(self.cercle_selectionne, x1 + 5, y1 + 5, x2 - 5, y2 - 5)
                self.cercle_selectionne = None
                self.position_selectionnee = None
            return
        if self.cercle_selectionne:
            print("Relâchement du pion.")
            x, y = event.x, event.y
            cercle_clique = self.trouver_cercle_noir_proche(x, y)
            if cercle_clique:
                position_arrivee = self.positions_cercles[cercle_clique]
                print(f"Position cible : {position_arrivee}")
                if position_arrivee in self.jeu.table_de_jeu.positions_bannies:
                    print("Déplacement invalide : la position cible est bannie.")
                    cercle_origine = [c for c, pos in self.positions_cercles.items() if pos == self.position_selectionnee][0]
                    x1, y1, x2, y2 = self.canvas.coords(cercle_origine)
                    self.canvas.coords(self.cercle_selectionne, x1 + 5, y1 + 5, x2 - 5, y2 - 5)
                else:
                    print(f"Déplacement du pion de {self.position_selectionnee} à {position_arrivee}.")
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
                        cercle_origine = [c for c, pos in self.positions_cercles.items() if pos == self.position_selectionnee][0]
                        x1, y1, x2, y2 = self.canvas.coords(cercle_origine)
                        self.canvas.coords(self.cercle_selectionne, x1 + 5, y1 + 5, x2 - 5, y2 - 5)
            else:
                print("Aucun cercle noir trouvé. Déplacement annulé.")
                cercle_origine = [c for c, pos in self.positions_cercles.items() if pos == self.position_selectionnee][0]
                x1, y1, x2, y2 = self.canvas.coords(cercle_origine)
                self.canvas.coords(self.cercle_selectionne, x1 + 5, y1 + 5, x2 - 5, y2 - 5)
            self.cercle_selectionne = None
            self.position_selectionnee = None

    def jouer_tour_ia(self):
        if self.jeu.tour == "ia":
            print("Tour de l'IA.") 
            resultat = self.jeu.jouer_tour_ia()
            if resultat == "victoire_ia":
                if self.jeu.phase == "placement":
                    position = self.jeu.derniere_position_ia
                    cercle_clique = [c for c, pos in self.positions_cercles.items() if pos == position][0]
                    x1, y1, x2, y2 = self.canvas.coords(cercle_clique)
                    pion = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=self.IA_COLOR)
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
                pion = self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=self.IA_COLOR)
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