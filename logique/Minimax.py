from logique.Pion import Pion

class Minimax:
    def __init__(self, table_de_jeu):
        self.table_de_jeu = table_de_jeu

    def meilleur_coup_placement(self, couleur_ia, couleur_joueur):
        """
        Calcule le meilleur coup pour la phase de placement.
        L'algorithme explore toutes les positions possibles et retourne la meilleure.
        """
        meilleur_score = float("-inf")  # Initialiser le meilleur score à une valeur très basse
        meilleur_coup = None  # Initialiser le meilleur coup à None

        # Parcourir toutes les positions du plateau
        for position in self.table_de_jeu.plateau:
            if self.table_de_jeu.est_position_valide(position):  # Vérifier si la position est libre
                # Simuler le placement de l'IA
                self.table_de_jeu.plateau[position] = Pion(couleur_ia)
                # Appeler Minimax pour évaluer ce placement
                score = self.minimax(
                    maximiser=False,
                    profondeur=0,
                    couleur_ia=couleur_ia,
                    couleur_joueur=couleur_joueur,
                    phase="placement",
                    pions_restants_joueur=len(self.table_de_jeu.plateau) - len(self.table_de_jeu.plateau.values())
                )
                # Annuler le placement (backtracking)
                self.table_de_jeu.plateau[position] = None

                # Log pour le débogage
                print(f"Position testée : {position}, Score calculé : {score}")

                # Mettre à jour le meilleur score et le meilleur coup
                if score > meilleur_score:
                    meilleur_score = score
                    meilleur_coup = position

        # Log pour le débogage
        print(f"Meilleur coup choisi : {meilleur_coup}, Meilleur score : {meilleur_score}")
        return meilleur_coup
    
    def meilleur_coup_deplacement(self, couleur_ia, couleur_joueur):
        """
        Calcule le meilleur déplacement pour la phase de déplacement.
        Retourne une paire (position_depart, position_arrivee).
        """
        meilleur_score = float("-inf")
        meilleur_deplacement = None

        # Parcourir toutes les positions du plateau
        for position_depart, pion in self.table_de_jeu.plateau.items():
            if pion is not None and pion.couleur == couleur_ia:  # Vérifier si le pion appartient à l'IA
                mouvements_legaux = self.table_de_jeu.calculer_mouvements_legaux(position_depart)
                for position_arrivee in mouvements_legaux:
                    # Simuler le déplacement
                    pion_original = self.table_de_jeu.plateau[position_arrivee]
                    self.table_de_jeu.plateau[position_arrivee] = pion
                    self.table_de_jeu.plateau[position_depart] = None

                    # Appeler Minimax pour évaluer ce déplacement
                    score = self.minimax(
                        maximiser=False,
                        profondeur=0,
                        couleur_ia=couleur_ia,
                        couleur_joueur=couleur_joueur,
                        phase="deplacement",
                        pions_restants_joueur=0  # Pas de pions restants à placer en phase de déplacement
                    )

                    # Annuler le déplacement (backtracking)
                    self.table_de_jeu.plateau[position_depart] = pion
                    self.table_de_jeu.plateau[position_arrivee] = pion_original

                    # Mettre à jour le meilleur score et le meilleur déplacement
                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_deplacement = (position_depart, position_arrivee)

        return meilleur_deplacement

    def minimax(self, maximiser, profondeur, couleur_ia, couleur_joueur, phase, pions_restants_joueur):
        """
        Algorithme Minimax pour les phases de placement et de déplacement.
        maximiser : True si c'est au tour de l'IA, False si c'est au tour de l'utilisateur.
        profondeur : Nombre de tours simulés.
        phase : "placement" ou "deplacement".
        pions_restants_joueur : Nombre de pions restants à placer pour le joueur.
        """
        # Limiter la profondeur en fonction du nombre de pions restants à placer
        if phase == "placement":
            if pions_restants_joueur == 3:
                profondeur_max = 5
            elif pions_restants_joueur == 2:
                profondeur_max = 3
            elif pions_restants_joueur == 1:
                profondeur_max = 1
            else:
                profondeur_max = 0  # Plus de placements possibles
        else:
            profondeur_max = 3  # Par défaut pour la phase de déplacement

        # Vérifier si une victoire est atteinte
        if self.table_de_jeu.verifier_victoire(couleur_ia):
            return 10  # Score élevé pour une victoire de l'IA
        if self.table_de_jeu.verifier_victoire(couleur_joueur):
            return -10  # Score bas pour une victoire de l'utilisateur

        # Si la profondeur maximale est atteinte, évaluer l'état du plateau
        if profondeur >= profondeur_max:
            return self.evaluation_plateau(couleur_ia, couleur_joueur,phase)

        if maximiser:
            # Tour de l'IA (maximiser le score)
            meilleur_score = float("-inf")
            for position_depart, pion in self.table_de_jeu.plateau.items():
                if phase == "placement" and self.table_de_jeu.est_position_valide(position_depart):
                    # Simuler le placement de l'IA
                    self.table_de_jeu.plateau[position_depart] = Pion(couleur_ia)
                    score = self.minimax(False, profondeur + 1, couleur_ia, couleur_joueur, phase, pions_restants_joueur)
                    self.table_de_jeu.plateau[position_depart] = None
                    meilleur_score = max(meilleur_score, score)
                elif phase == "deplacement" and pion is not None and pion.couleur == couleur_ia:
                    mouvements_legaux = self.table_de_jeu.calculer_mouvements_legaux(position_depart)
                    for position_arrivee in mouvements_legaux:
                        # Simuler le déplacement
                        pion_original = self.table_de_jeu.plateau[position_arrivee]
                        self.table_de_jeu.plateau[position_arrivee] = pion
                        self.table_de_jeu.plateau[position_depart] = None
                        score = self.minimax(False, profondeur + 1, couleur_ia, couleur_joueur, phase, pions_restants_joueur)
                        self.table_de_jeu.plateau[position_depart] = pion
                        self.table_de_jeu.plateau[position_arrivee] = pion_original
                        meilleur_score = max(meilleur_score, score)
            return meilleur_score
        else:
            # Tour de l'utilisateur (minimiser le score)
            meilleur_score = float("inf")
            for position_depart, pion in self.table_de_jeu.plateau.items():
                if phase == "placement" and self.table_de_jeu.est_position_valide(position_depart):
                    # Simuler le placement de l'utilisateur
                    self.table_de_jeu.plateau[position_depart] = Pion(couleur_joueur)
                    score = self.minimax(True, profondeur + 1, couleur_ia, couleur_joueur, phase, pions_restants_joueur - 1)
                    self.table_de_jeu.plateau[position_depart] = None
                    meilleur_score = min(meilleur_score, score)
                elif phase == "deplacement" and pion is not None and pion.couleur == couleur_joueur:
                    mouvements_legaux = self.table_de_jeu.calculer_mouvements_legaux(position_depart)
                    for position_arrivee in mouvements_legaux:
                        # Simuler le déplacement
                        pion_original = self.table_de_jeu.plateau[position_arrivee]
                        self.table_de_jeu.plateau[position_arrivee] = pion
                        self.table_de_jeu.plateau[position_depart] = None
                        score = self.minimax(True, profondeur + 1, couleur_ia, couleur_joueur, phase, pions_restants_joueur)
                        self.table_de_jeu.plateau[position_depart] = pion
                        self.table_de_jeu.plateau[position_arrivee] = pion_original
                        meilleur_score = min(meilleur_score, score)
            return meilleur_score

    def evaluation_plateau(self, couleur_ia, couleur_joueur,phase):
        """
        Évalue l'état actuel du plateau.
        Retourne un score basé sur les positions stratégiques et les alignements partiels.
        """
        score = 0

        # Ajouter des points pour les positions stratégiques
        if phase == "placement":
            positions_strategiques = [(1, 1)]  # Le centre est stratégique
            for position in positions_strategiques:
                if self.table_de_jeu.plateau[position] is not None:
                    if self.table_de_jeu.plateau[position].couleur == couleur_ia:
                        score += 2  # Bonus pour l'IA
                    elif self.table_de_jeu.plateau[position].couleur == couleur_joueur:
                        score -= 2  # Malus pour l'utilisateur

        # Ajouter des points pour les alignements partiels
        lignes_gagnantes = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]
        for ligne in lignes_gagnantes:
            ia_count = sum(1 for pos in ligne if self.table_de_jeu.plateau[pos] is not None and self.table_de_jeu.plateau[pos].couleur == couleur_ia)
            joueur_count = sum(1 for pos in ligne if self.table_de_jeu.plateau[pos] is not None and self.table_de_jeu.plateau[pos].couleur == couleur_joueur)

            if ia_count > 0 and joueur_count == 0:
                score += ia_count  # Bonus pour l'IA
            elif joueur_count > 0 and ia_count == 0:
                score -= joueur_count  # Malus pour l'utilisateur

        return score