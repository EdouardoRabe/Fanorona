class TableDeJeu:
    def __init__(self):
        self.plateau = {
            (0, 0): None, (0, 1): None, (0, 2): None,
            (1, 0): None, (1, 1): None, (1, 2): None,
            (2, 0): None, (2, 1): None, (2, 2): None
        }
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
        return position in self.plateau and self.plateau[position] is None

    def placer_pion(self, position, pion):
        if self.est_position_valide(position):
            self.plateau[position] = pion
            return True
        return False

    def deplacer_pion(self, position_depart, position_arrivee):
        if position_depart in self.plateau and position_arrivee in self.connexions[position_depart]:
            if self.plateau[position_depart] is not None and self.plateau[position_arrivee] is None:
                self.plateau[position_arrivee] = self.plateau[position_depart]
                self.plateau[position_depart] = None
                return True
        return False

    def calculer_mouvements_legaux(self, position):
        mouvements = []
        if position not in self.plateau or self.plateau[position] is None:
            return mouvements
        for voisin in self.connexions[position]:
            if self.plateau[voisin] is None:  
                mouvements.append(voisin)
        return mouvements

    def verifier_victoire(self, couleur):
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
            if all(self.plateau[pos] is not None and self.plateau[pos].couleur == couleur for pos in ligne):
                return True
        return False