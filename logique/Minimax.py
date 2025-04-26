from logique.Pion import Pion

class Minimax:
    def __init__(self, table_de_jeu):
        self.table_de_jeu = table_de_jeu

    def meilleur_coup_placement(self, couleur_ia, couleur_joueur):
        meilleur_score = float("-inf")
        meilleur_coup = None
        pions_places_ia = sum(1 for pion in self.table_de_jeu.plateau.values() if pion is not None and pion.couleur == couleur_ia)
        pions_places_joueur = sum(1 for pion in self.table_de_jeu.plateau.values() if pion is not None and pion.couleur == couleur_joueur)
        bannies_existent = bool(self.table_de_jeu.positions_bannies)
        for position in self.table_de_jeu.plateau:
            # if pions_places_ia == 0 and position == (1, 1):
            #     continue
            if self.table_de_jeu.est_position_valide(position):
                self.table_de_jeu.plateau[position] = Pion(couleur_ia)
                score = self.minimax(
                    maximiser=False,
                    profondeur=0,
                    couleur_ia=couleur_ia,
                    couleur_joueur=couleur_joueur,
                    phase="placement",
                    pions_places_joueur=pions_places_joueur
                )
                self.table_de_jeu.plateau[position] = None
                print(f"Position testée : {position}, Score calculé : {score}")
                if score > meilleur_score and score != float("-inf") and score != float("inf"):
                    meilleur_score = score
                    meilleur_coup = position
        print(f"Meilleur coup choisi : {meilleur_coup}, Meilleur score : {meilleur_score}")
        return meilleur_coup

    def meilleur_coup_deplacement(self, couleur_ia, couleur_joueur):
        meilleur_score = float("-inf")
        meilleur_deplacement = None
        bannies_existent = bool(self.table_de_jeu.positions_bannies)
        for position_depart, pion in self.table_de_jeu.plateau.items():
            if pion is not None and pion.couleur == couleur_ia:
                mouvements_legaux = self.table_de_jeu.calculer_mouvements_legaux(position_depart)
                for position_arrivee in mouvements_legaux:
                    if position_arrivee in self.table_de_jeu.positions_bannies:
                        continue
                    pion_original = self.table_de_jeu.plateau[position_arrivee]
                    self.table_de_jeu.plateau[position_arrivee] = pion
                    self.table_de_jeu.plateau[position_depart] = None
                    score = self.minimax(
                        maximiser=False,
                        profondeur=0,
                        couleur_ia=couleur_ia,
                        couleur_joueur=couleur_joueur,
                        phase="deplacement",
                        pions_places_joueur=0
                    )
                    self.table_de_jeu.plateau[position_depart] = pion
                    self.table_de_jeu.plateau[position_arrivee] = pion_original
                    print(f"Déplacement testé : {position_depart} -> {position_arrivee}, Score calculé : {score}")
                    if score > meilleur_score and score != float("-inf") and score != float("inf"):
                        meilleur_score = score
                        meilleur_deplacement = (position_depart, position_arrivee)
        print(f"Meilleur déplacement choisi : {meilleur_deplacement}, Meilleur score : {meilleur_score}")
        return meilleur_deplacement

    def minimax(self, maximiser, profondeur, couleur_ia, couleur_joueur, phase, pions_places_joueur):
        if phase == "placement":
            profondeur_max = 3
            pions_places_ia = sum(1 for pion in self.table_de_jeu.plateau.values() if pion is not None and pion.couleur == couleur_ia)
            pions_places_joueur = sum(1 for pion in self.table_de_jeu.plateau.values() if pion is not None and pion.couleur == couleur_joueur)
            if pions_places_ia >= 3 and pions_places_joueur >= 3:
                phase = "deplacement"
        else:
            profondeur_max = 7
        victoire_score = 100 - profondeur * 10  
        defaite_score = -100 + profondeur * 10  
        if self.table_de_jeu.verifier_victoire(couleur_ia):
            return victoire_score + self.evaluation_plateau(couleur_ia, couleur_joueur, phase, profondeur)
        if self.table_de_jeu.verifier_victoire(couleur_joueur):
            return defaite_score + self.evaluation_plateau(couleur_ia, couleur_joueur, phase, profondeur)
        if profondeur >= profondeur_max:
            return self.evaluation_plateau(couleur_ia, couleur_joueur, phase, profondeur)

        if maximiser:
            meilleur_score = float("-inf")
            coup_trouve = False
            for position_depart, pion in self.table_de_jeu.plateau.items():
                if phase == "placement" and self.table_de_jeu.est_position_valide(position_depart):
                    self.table_de_jeu.plateau[position_depart] = Pion(couleur_ia)
                    score = self.minimax(False, profondeur + 1, couleur_ia, couleur_joueur, phase, pions_places_joueur)
                    self.table_de_jeu.plateau[position_depart] = None
                    meilleur_score = max(meilleur_score, score)
                    coup_trouve = True
                elif phase == "deplacement" and pion is not None and pion.couleur == couleur_ia:
                    mouvements_legaux = self.table_de_jeu.calculer_mouvements_legaux(position_depart)
                    for position_arrivee in mouvements_legaux:
                        if position_arrivee in self.table_de_jeu.positions_bannies:
                            continue
                        pion_original = self.table_de_jeu.plateau[position_arrivee]
                        self.table_de_jeu.plateau[position_arrivee] = pion
                        self.table_de_jeu.plateau[position_depart] = None
                        score = self.minimax(False, profondeur + 1, couleur_ia, couleur_joueur, phase, pions_places_joueur)
                        self.table_de_jeu.plateau[position_depart] = pion
                        self.table_de_jeu.plateau[position_arrivee] = pion_original
                        meilleur_score = max(meilleur_score, score)
                        coup_trouve = True
            if not coup_trouve:
                return self.evaluation_plateau(couleur_ia, couleur_joueur, phase, profondeur)
            return meilleur_score
        else:
            meilleur_score = float("inf")
            coup_trouve = False
            for position_depart, pion in self.table_de_jeu.plateau.items():
                if phase == "placement" and self.table_de_jeu.est_position_valide(position_depart):
                    self.table_de_jeu.plateau[position_depart] = Pion(couleur_joueur)
                    score = self.minimax(True, profondeur + 1, couleur_ia, couleur_joueur, phase, pions_places_joueur)
                    self.table_de_jeu.plateau[position_depart] = None
                    meilleur_score = min(meilleur_score, score)
                    coup_trouve = True
                elif phase == "deplacement" and pion is not None and pion.couleur == couleur_joueur:
                    mouvements_legaux = self.table_de_jeu.calculer_mouvements_legaux(position_depart)
                    for position_arrivee in mouvements_legaux:
                        if position_arrivee in self.table_de_jeu.positions_bannies:
                            continue
                        pion_original = self.table_de_jeu.plateau[position_arrivee]
                        self.table_de_jeu.plateau[position_arrivee] = pion
                        self.table_de_jeu.plateau[position_depart] = None
                        score = self.minimax(True, profondeur + 1, couleur_ia, couleur_joueur, phase, pions_places_joueur)
                        self.table_de_jeu.plateau[position_depart] = pion
                        self.table_de_jeu.plateau[position_arrivee] = pion_original
                        meilleur_score = min(meilleur_score, score)
                        coup_trouve = True
            if not coup_trouve:
                return self.evaluation_plateau(couleur_ia, couleur_joueur, phase, profondeur)
            return meilleur_score

    def evaluation_plateau(self, couleur_ia, couleur_joueur, phase, profondeur):
        score = 0

        if phase == "placement":
            centre = (1, 1)
            positions_centrales = [(0, 1), (1, 0), (1, 2), (2, 1)]
            coins = [(0, 0), (0, 2), (2, 0), (2, 2)]
            if self.table_de_jeu.plateau[centre] is not None:
                if self.table_de_jeu.plateau[centre].couleur == couleur_ia:
                    score += 3
                elif self.table_de_jeu.plateau[centre].couleur == couleur_joueur:
                    score -= 3
            else:
                score += 2
            for position in positions_centrales:
                if position in self.table_de_jeu.positions_bannies: 
                    continue
                if self.table_de_jeu.plateau[position] is not None:
                    if self.table_de_jeu.plateau[position].couleur == couleur_ia:
                        score += 2
                    elif self.table_de_jeu.plateau[position].couleur == couleur_joueur:
                        score -= 2
                else:
                    score += 1
            for position in coins:
                if position in self.table_de_jeu.positions_bannies:  
                    continue
                if self.table_de_jeu.plateau[position] is not None:
                    if self.table_de_jeu.plateau[position].couleur == couleur_ia:
                        score -= 1
                    elif self.table_de_jeu.plateau[position].couleur == couleur_joueur:
                        score += 1

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
            if any(pos in self.table_de_jeu.positions_bannies for pos in ligne):  
                continue
            ia_count = sum(1 for pos in ligne if self.table_de_jeu.plateau[pos] is not None and self.table_de_jeu.plateau[pos].couleur == couleur_ia)
            joueur_count = sum(1 for pos in ligne if self.table_de_jeu.plateau[pos] is not None and self.table_de_jeu.plateau[pos].couleur == couleur_joueur)
            if ia_count > 0 and joueur_count == 0:
                score += ia_count
            elif joueur_count > 0 and ia_count == 0:
                score -= joueur_count

        return score