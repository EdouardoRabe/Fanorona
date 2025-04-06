from logique.TableDeJeu import TableDeJeu
from logique.Pion import Pion
from logique.Minimax import Minimax

class Jeu:
    def __init__(self):
        self.table_de_jeu = TableDeJeu()
        self.minimax = Minimax(self.table_de_jeu)
        self.pions_utilisateur = [Pion("rouge") for _ in range(3)]
        self.pions_ia = [Pion("bleu") for _ in range(3)]
        self.phase = "placement"  
        self.tour = "utilisateur"  
        self.derniere_position_ia = None  
        self.position_selectionnee = None  
        self.pion_selectionne = None  

    def jouer_tour_utilisateur(self, position_depart=None, position_arrivee=None):
        if self.phase == "placement":
            if self.table_de_jeu.est_position_valide(position_depart):
                pion = self.pions_utilisateur.pop(0)
                self.table_de_jeu.placer_pion(position_depart, pion)
                if self.table_de_jeu.verifier_victoire("rouge"):
                    return "victoire_utilisateur"
                self.verifier_phase()  
                self.tour = "ia"
                return "placement_reussi"
        elif self.phase == "deplacement":
            if self.phase == "deplacement":
                if self.table_de_jeu.deplacer_pion(position_depart, position_arrivee):
                    if self.table_de_jeu.verifier_victoire("rouge"):
                        return "victoire_utilisateur"
                    self.verifier_phase() 
                    self.tour = "ia" 
                    return "deplacement_reussi"
                else:
                    return "deplacement_invalide"
        return "action_invalide"

    def jouer_tour_ia(self):
        if self.phase == "placement" and self.tour == "ia":
            position = self.minimax.meilleur_coup_placement("bleu", "rouge")
            self.derniere_position_ia = position
            pion = self.pions_ia.pop(0)
            self.table_de_jeu.placer_pion(position, pion)
            if self.table_de_jeu.verifier_victoire("bleu"):
                return "victoire_ia"
            self.verifier_phase()  
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
        if self.phase == "placement" and not self.pions_utilisateur and not self.pions_ia:
            print("Changement de phase : déplacement.")  
            self.phase = "deplacement"