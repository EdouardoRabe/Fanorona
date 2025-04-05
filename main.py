from logique.Jeu import Jeu
from interface.Fenetre import Fenetre

def main():
    jeu = Jeu()
    fenetre = Fenetre(jeu)
    fenetre.demarrer()

if __name__ == "__main__":
    main()