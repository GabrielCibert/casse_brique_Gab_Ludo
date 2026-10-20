'''
Programme de nos fonctions sous forme de classes
Fait par Gabriel CIBERT et Ludovic ANDERSON
Commencé le 13/10/2026
Reste à faire : lien entre le menu et le jeu
'''

from tkinter import Tk, Button, Canvas, LEFT, NW, PhotoImage
import random
import math
from classe_balle import Balle
from classe_raquette import Raquette
from classe_brique import Brique

class Jeu:
    LARGEUR = 1000
    HAUTEUR = 660
    DELAI = 20  # ms entre deux images

    def __init__(self):
        self.en_cours = False

        self.fenetre = Tk()
        self.fenetre.geometry('1000x750+160+0')
        self.fenetre.title('Casse brique')

        self.canvas = Canvas(self.fenetre, width=self.LARGEUR, height=self.HAUTEUR, bg='white')
        self.canvas.pack(padx=5, pady=5)

        # image d'arrière-plan (ignorée si le fichier est absent)
        try:
            self.image_fond = PhotoImage(file="casse_brique1.ppm")
            self.canvas.create_image(0, 0, anchor=NW, image=self.image_fond)
        except Exception:
            self.image_fond = None

        self.raquette = Raquette(self.canvas, self.LARGEUR / 2, 645, self.LARGEUR)
        self.briques = []
        self.creer_briques()
        self.balle = Balle(self.canvas)
        self.balle.placer_sur(self.raquette)
        self.texte = None

        self.canvas.focus_set()
        self.canvas.bind('<Key>', self.clavier)

        Button(self.fenetre, text='Go', command=self.go).pack(side=LEFT, padx=10, pady=10)
        Button(self.fenetre, text='Quitter', command=self.fenetre.destroy).pack(side=LEFT, padx=5, pady=5)

    def creer_briques(self):
        for i in range(8):
            for j in range(3):
                centre_x = self.LARGEUR / 2 - 420 + 120 * i
                centre_y = 50 + 50 * j
                self.briques.append(Brique(self.canvas, centre_x, centre_y))

    # --- événements ---

    def clavier(self, event):
        touche = event.keysym
        if touche in ('d', 'Right'):
            self.raquette.deplacer(+1)
        elif touche in ('q', 'Left'):
            self.raquette.deplacer(-1)
        # tant que le jeu n'est pas lancé, la balle suit la raquette
        if not self.en_cours:
            self.balle.x = self.raquette.x
            self.balle.afficher()

    def go(self):
        if not self.en_cours and self.briques:
            self.en_cours = True
            if self.texte:
                self.canvas.delete(self.texte)
                self.texte = None
            self.mettre_a_jour()

    # --- boucle de jeu ---

    def mettre_a_jour(self):
        balle = self.balle
        balle.avancer()
        balle.rebond_murs(self.LARGEUR)
        balle.rebond_raquette(self.raquette)

        # collision avec les briques (une seule par image)
        for brique in self.briques:
            if balle.touche(brique.coords()):
                balle.rebond_brique(brique)
                brique.detruire()
                self.briques.remove(brique)
                break

        # victoire
        if not self.briques:
            self.en_cours = False
            self.texte = self.canvas.create_text(self.LARGEUR / 2, self.HAUTEUR / 2,
                                                 text='Gagné !', font=('Arial', 40), fill='green')
            return

        # balle perdue en bas : retour sur la raquette, on attend « Go »
        if balle.y + balle.rayon > self.HAUTEUR:
            self.en_cours = False
            balle.placer_sur(self.raquette)
            return

        balle.afficher()
        self.fenetre.after(self.DELAI, self.mettre_a_jour)

    def lancer(self):
        self.fenetre.mainloop()


# PROGRAMME PRINCIPAL



