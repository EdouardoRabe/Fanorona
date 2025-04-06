from logique.TableDeJeu import TableDeJeu
from logique.Pion import Pion
from logique.Minimax import Minimax

class Jeu:
    def __init__(self):
        self.table_de_jeu = TableDeJeu()
        self.minimax = Minimax(self.table_de_jeu)
        self.pions_utilisateur = [Pion("rouge") for _ in range(3)]
        self.pions_ia = [Pion("bleu") for _ in range(3)]
        self.phase = "placement"  # Phase actuelle du jeu
        self.tour = "utilisateur"  # Tour actuel : "utilisateur" ou "ia"
        self.derniere_position_ia = None  # Stocke la dernière position choisie par l'IA
        self.position_selectionnee = None  # Stocke la position logique du pion sélectionné
        self.pion_selectionne = None  # Stocke le pion temporairement retiré du plateau

    def jouer_tour_utilisateur(self, position_depart=None, position_arrivee=None):
        """Gère le tour de l'utilisateur pour la phase de placement ou de déplacement."""
        if self.phase == "placement":
            if self.table_de_jeu.est_position_valide(position_depart):
                pion = self.pions_utilisateur.pop(0)
                self.table_de_jeu.placer_pion(position_depart, pion)
                if self.table_de_jeu.verifier_victoire("rouge"):
                    return "victoire_utilisateur"
                self.verifier_phase()  # Vérifier le changement de phase après le placement
                self.tour = "ia"
                return "placement_reussi"
        elif self.phase == "deplacement":
            if self.position_selectionnee is None:
                # Sélectionner un pion
                if self.table_de_jeu.plateau[position_depart] is not None and self.table_de_jeu.plateau[position_depart].couleur == "rouge":
                    self.position_selectionnee = position_depart
                    self.pion_selectionne = self.table_de_jeu.plateau[position_depart]
                    self.table_de_jeu.plateau[position_depart] = None  # Retirer temporairement le pion
                    return "pion_selectionne"
            else:
                # Déplacer le pion sélectionné
                if self.table_de_jeu.deplacer_pion(self.position_selectionnee, position_arrivee):
                    self.table_de_jeu.plateau[position_arrivee] = self.pion_selectionne  # Placer le pion
                    self.pion_selectionne = None  # Réinitialiser le pion temporaire
                    if self.table_de_jeu.verifier_victoire("rouge"):
                        return "victoire_utilisateur"
                    self.position_selectionnee = None
                    self.tour = "ia"
                    return "deplacement_reussi"
                else:
                    # Annuler le déplacement en cas d'échec
                    self.table_de_jeu.plateau[self.position_selectionnee] = self.pion_selectionne
                    self.pion_selectionne = None
                    self.position_selectionnee = None
                    return "deplacement_invalide"
        return "action_invalide"

    def jouer_tour_ia(self):
        """Gère le tour de l'IA pour la phase de placement ou de déplacement."""
        if self.phase == "placement" and self.tour == "ia":
            position = self.minimax.meilleur_coup_placement("bleu", "rouge")
            self.derniere_position_ia = position
            pion = self.pions_ia.pop(0)
            self.table_de_jeu.placer_pion(position, pion)
            if self.table_de_jeu.verifier_victoire("bleu"):
                return "victoire_ia"
            self.verifier_phase()  # Vérifier le changement de phase après le placement
            self.tour = "utilisateur"
            return "placement_reussi"
        elif self.phase == "deplacement" and self.tour == "ia":
            deplacement = self.minimax.meilleur_coup_deplacement("bleu", "rouge")
            if deplacement:
                position_depart, position_arrivee = deplacement
                self.table_de_jeu.deplacer_pion(position_depart, position_arrivee)
                self.derniere_position_ia = (position_depart, position_arrivee)
                if self.table_de_jeu.verifier_victoire("bleu"):
                    return "victoire_ia"
                self.tour = "utilisateur"
                return "deplacement_reussi"
        return "action_invalide"

    def verifier_phase(self):
        """Passe à la phase de déplacement si tous les pions sont placés."""
        if self.phase == "placement" and not self.pions_utilisateur and not self.pions_ia:
            print("Changement de phase : déplacement.")  # Debug
            self.phase = "deplacement"