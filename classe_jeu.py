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
    VIES_DEPART = 3
    SCORES = 0

    def __init__(self):
        self.en_cours = False

        self.fenetre = Tk()
        self.fenetre.geometry('1000x750+160+0')
        self.fenetre.title('Casse brique')

        self.canvas = Canvas(self.fenetre, width = self.LARGEUR, height = self.HAUTEUR, bg = 'white')
        self.canvas.pack(padx = 5, pady = 5)

        # image d'arrière-plan (ignorée si le fichier est absent)
        try:
            self.image1 = PhotoImage(file = 'casse_brique1.ppm')
            self.canvas.create_image(0, 0, anchor = NW, image = self.image1)
        except Exception:
            self.image1 = None

        self.raquette = Raquette(self.canvas, self.LARGEUR / 2, 645, self.LARGEUR)
        self.briques = []
        self.creer_briques()
        self.balle = Balle(self.canvas)
        self.balle.placer_sur(self.raquette)
        self.texte = None

        # score
        self.score = self.SCORES
        self.texte_score = self.canvas.create_text(10, 10, anchor = 'nw', text = 'Scores : ' + str(self.score), font = ('Arial', 16), fill = 'red')
        

        # Système de vies
        self.vies = self.VIES_DEPART
        self.texte_vies = self.canvas.create_text(self.LARGEUR - 10, 10, anchor = 'ne', text = 'Vies : ' + str(self.vies), font = ('Arial', 16), fill = 'red')

        self.canvas.focus_set()
        self.canvas.bind('<Key>', self.clavier)

        Button(self.fenetre, text = 'Go', command = self.go).pack(side = LEFT, padx = 10, pady = 10)
        Button(self.fenetre, text = 'Quitter', command = self.fenetre.destroy).pack(side = LEFT, padx = 5, pady = 5)

    def creer_briques(self):
        for i in range(8):
            for j in range(3):
                centre_x = self.LARGEUR / 2 - 420 + 120 * i
                centre_y = 50 + 50 * j
                self.briques.append(Brique(self.canvas, centre_x, centre_y))

    def afficher_vies(self):
        self.canvas.itemconfig(self.texte_vies, text = 'Vies : ' + str(self.vies))

    def afficher_score(self):
        self.canvas.itemconfig(self.texte_score, text = 'Scores : ' + str(self.score))

    def clavier(self, event):
        touche = event.keysym
        if touche == 'd':
            self.raquette.deplacer(+1)
        elif touche == 'q':
            self.raquette.deplacer(-1)
        elif touche == 'space':
            self.go()
        # tant que le jeu n'est pas lancé, la balle suit la raquette
        if not self.en_cours:
            self.balle.x = self.raquette.x
            self.balle.afficher()

    def go(self):
        if self.en_cours:
            return
        if self.vies == 0 or not self.briques:
            self.vies = self.VIES_DEPART
            self.afficher_vies()
            for brique in self.briques:
                brique.detruire()
            self.briques = []
            self.creer_briques()
        self.en_cours = True
        if self.texte:
            self.canvas.delete(self.texte)
            self.texte = None
        self.mettre_a_jour()

    # boucle de jeu

    def mettre_a_jour(self):
        balle = self.balle
        balle.avancer()
        balle.rebond_murs(self.LARGEUR)
        balle.rebond_raquette(self.raquette)
        self.afficher_score()

        # collision avec les briques (une seule par image)
        for brique in self.briques:
            if balle.touche(brique.coords()):
                balle.rebond_brique(brique)
                brique.detruire()
                self.briques.remove(brique)
                self.score += 50
                self.afficher_score()
                break

        # victoire
        if not self.briques:
            self.en_cours = False
            self.texte = self.canvas.create_text(self.LARGEUR / 2, self.HAUTEUR / 2, text = 'Gagné !', font = ('Arial', 40), fill = 'green')
            return

        # balle perdue en bas : retour sur la raquette, on attend « Go »
        if balle.y + balle.rayon > self.HAUTEUR:
            self.en_cours = False
            self.vies -= 1
            self.afficher_vies()
            if self.vies == 0:
                self.texte = self.canvas.create_text(self.LARGEUR / 2, self.HAUTEUR / 2, text = 'GAME OVER', font = ('Arial', 40), fill = 'red')
                self.score = 0
            
            balle.placer_sur(self.raquette)
            return
        
        balle.afficher()
        self.fenetre.after(self.DELAI, self.mettre_a_jour)

    def lancer(self):
        self.fenetre.mainloop()



if __name__ == '__main__':
    Jeu().lancer()