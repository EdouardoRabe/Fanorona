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

    def jouer_tour_utilisateur(self, position):
        """Gère le tour de l'utilisateur pour la phase de placement."""
        if self.phase == "placement":
            if self.table_de_jeu.est_position_valide(position):
                pion = self.pions_utilisateur.pop(0)
                self.table_de_jeu.placer_pion(position, pion)
                if self.table_de_jeu.verifier_victoire("rouge"):
                    return "victoire_utilisateur"
                self.tour = "ia"
                return "placement_reussi"
        return "placement_invalide"

    def jouer_tour_ia(self):
        """Gère le tour de l'IA pour la phase de placement."""
        if self.phase == "placement" and self.tour == "ia":
            position = self.minimax.meilleur_coup_placement("bleu", "rouge")
            self.derniere_position_ia = position  # Stocker la position choisie
            pion = self.pions_ia.pop(0)
            self.table_de_jeu.placer_pion(position, pion)
            if self.table_de_jeu.verifier_victoire("bleu"):
                return "victoire_ia"
            self.tour = "utilisateur"
        return "placement_reussi"

    def verifier_phase(self):
        """Passe à la phase de déplacement si tous les pions sont placés."""
        if self.phase == "placement" and not self.pions_utilisateur and not self.pions_ia:
            self.phase = "deplacement"