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
                score = self.minimax(False, 0, couleur_ia, couleur_joueur)
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

    def minimax(self, maximiser, profondeur, couleur_ia, couleur_joueur):
        """
        Algorithme Minimax pour la phase de placement.
        maximiser : True si c'est au tour de l'IA, False si c'est au tour de l'utilisateur.
        profondeur : Nombre de tours simulés.
        """
        # Vérifier si l'IA a gagné
        if self.table_de_jeu.verifier_victoire(couleur_ia):
            return 10  # Score élevé pour une victoire de l'IA
        # Vérifier si l'utilisateur a gagné
        if self.table_de_jeu.verifier_victoire(couleur_joueur):
            return -10  # Score bas pour une victoire de l'utilisateur

        # Si la profondeur maximale est atteinte, évaluer l'état du plateau
        if profondeur == 3:
            return self.evaluation_plateau(couleur_ia, couleur_joueur)

        if maximiser:
            # Tour de l'IA (maximiser le score)
            meilleur_score = float("-inf")
            for position in self.table_de_jeu.plateau:
                if self.table_de_jeu.est_position_valide(position):  # Vérifier si la position est libre
                    # Simuler le placement de l'IA
                    self.table_de_jeu.plateau[position] = Pion(couleur_ia)
                    # Appeler Minimax pour le tour suivant
                    score = self.minimax(False, profondeur + 1, couleur_ia, couleur_joueur)
                    # Annuler le placement (backtracking)
                    self.table_de_jeu.plateau[position] = None
                    # Mettre à jour le meilleur score
                    meilleur_score = max(meilleur_score, score)
            return meilleur_score
        else:
            # Tour de l'utilisateur (minimiser le score)
            meilleur_score = float("inf")
            for position in self.table_de_jeu.plateau:
                if self.table_de_jeu.est_position_valide(position):  # Vérifier si la position est libre
                    # Simuler le placement de l'utilisateur
                    self.table_de_jeu.plateau[position] = Pion(couleur_joueur)
                    # Appeler Minimax pour le tour suivant
                    score = self.minimax(True, profondeur + 1, couleur_ia, couleur_joueur)
                    # Annuler le placement (backtracking)
                    self.table_de_jeu.plateau[position] = None
                    # Mettre à jour le meilleur score
                    meilleur_score = min(meilleur_score, score)
            return meilleur_score

    def evaluation_plateau(self, couleur_ia, couleur_joueur):
        """
        Évalue l'état actuel du plateau.
        Retourne un score basé sur les positions stratégiques et les alignements partiels.
        """
        score = 0

        # Ajouter des points pour les positions stratégiques
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