class TableDeJeu:
    def __init__(self):
        # Représentation du plateau sous forme de dictionnaire
        self.plateau = {
            (0, 0): None, (0, 1): None, (0, 2): None,
            (1, 0): None, (1, 1): None, (1, 2): None,
            (2, 0): None, (2, 1): None, (2, 2): None
        }
        # Connexions entre les positions (graphes)
        self.connexions = {
            (0, 0): [(0, 1), (1, 0), (1, 1)],
            (0, 1): [(0, 0), (0, 2), (1, 1)],
            (0, 2): [(0, 1), (1, 1), (1, 2)],
            (1, 0): [(0, 0), (1, 1), (2, 0)],
            (1, 1): [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)],
            (1, 2): [(0, 2), (1, 1), (2, 2)],
            (2, 0): [(1, 0), (1, 1), (2, 1)],
            (2, 1): [(2, 0), (1, 1), (2, 2)],
            (2, 2): [(1, 2), (1, 1), (2, 1)],
        }

    def est_position_valide(self, position):
        """Vérifie si une position est valide et libre."""
        return position in self.plateau and self.plateau[position] is None

    def placer_pion(self, position, pion):
        """Place un pion sur le plateau."""
        if self.est_position_valide(position):
            self.plateau[position] = pion
            return True
        return False

    def deplacer_pion(self, position_depart, position_arrivee):
        """Déplace un pion d'une position à une autre."""
        if position_depart in self.plateau and position_arrivee in self.connexions[position_depart]:
            if self.plateau[position_depart] is not None and self.plateau[position_arrivee] is None:
                self.plateau[position_arrivee] = self.plateau[position_depart]
                self.plateau[position_depart] = None
                return True
        return False

    def calculer_mouvements_legaux(self, position, couleur):
        """
        Calcule les mouvements légaux pour un pion à une position donnée.
        Retourne une liste des positions accessibles.
        """
        mouvements = []
        if position not in self.plateau or self.plateau[position] is None:
            return mouvements

        # Déplacements possibles (haut, bas, gauche, droite, diagonales)
        for voisin in self.connexions[position]:
            if self.plateau[voisin] is None:  # Vérifier si la position voisine est libre
                mouvements.append(voisin)

        return mouvements

    def verifier_victoire(self, couleur):
        """Vérifie si un joueur a aligné 3 pions."""
        lignes_gagnantes = [
            [(0, 0), (0, 1), (0, 2)],  # Ligne horizontale 1
            [(1, 0), (1, 1), (1, 2)],  # Ligne horizontale 2
            [(2, 0), (2, 1), (2, 2)],  # Ligne horizontale 3
            [(0, 0), (1, 0), (2, 0)],  # Ligne verticale 1
            [(0, 1), (1, 1), (2, 1)],  # Ligne verticale 2
            [(0, 2), (1, 2), (2, 2)],  # Ligne verticale 3
            [(0, 0), (1, 1), (2, 2)],  # Diagonale 1
            [(0, 2), (1, 1), (2, 0)],  # Diagonale 2
        ]
        for ligne in lignes_gagnantes:
            if all(self.plateau[pos] is not None and self.plateau[pos].couleur == couleur for pos in ligne):
                return True
        return False