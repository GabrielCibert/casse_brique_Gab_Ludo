'''
Programme de nos fonctions sous forme de classes
Fait par Gabriel CIBERT et Ludovic ANDERSON
Commencé le 13/10/2026
Reste à faire : TOUT !!!
'''

from tkinter import Tk, Button, Canvas, LEFT, NW, PhotoImage
import random
import math



class Raquette:

    def __init__(self, canvas, x, y, largeur_zone):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.demi_largeur = 50
        self.demi_hauteur = 5
        self.pas = 50
        self.largeur_zone = largeur_zone
        self.id = canvas.create_rectangle(0, 0, 0, 0, outline = 'black', fill = 'red')
        self.afficher()

    def deplacer(self, direction):
        """direction = -1 (gauche) ou +1 (droite)."""
        self.x += direction * self.pas
        # la raquette reste dans la fenêtre
        self.x = max(self.demi_largeur, min(self.largeur_zone - self.demi_largeur, self.x))
        self.afficher()

    def afficher(self):
        self.canvas.coords(self.id,
                           self.x - self.demi_largeur, self.y - self.demi_hauteur,
                           self.x + self.demi_largeur, self.y + self.demi_hauteur)

    def coords(self):
        return self.canvas.coords(self.id)


class Brique:
    """Une brique cassable."""

    def __init__(self, canvas, centre_x, centre_y):
        self.canvas = canvas
        self.id = canvas.create_rectangle(centre_x - 45, centre_y - 13,
                                          centre_x + 45, centre_y + 13,
                                          outline='black', fill='blue')

    def coords(self):
        return self.canvas.coords(self.id)

    def detruire(self):
        self.canvas.delete(self.id)


class Balle:
    """La balle : position, vitesse, rebonds."""

    def __init__(self, canvas, rayon=10):
        self.canvas = canvas
        self.rayon = rayon
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.ancien_x = 0
        self.ancien_y = 0
        self.id = canvas.create_oval(0, 0, 0, 0, width=1, outline='black', fill='yellow')

    def placer_sur(self, raquette):
        """Pose la balle sur la raquette et choisit une nouvelle direction vers le haut."""
        self.x = raquette.x
        self.y = raquette.y - raquette.demi_hauteur - self.rayon
        vitesse = random.uniform(1.8, 2) * 7
        angle = random.uniform(1.2 * math.pi, 1.8 * math.pi)  # sin < 0 : vers le haut
        self.dx = vitesse * math.cos(angle)
        self.dy = vitesse * math.sin(angle)
        self.afficher()

    def avancer(self):
        self.ancien_x = self.x
        self.ancien_y = self.y
        self.x += self.dx
        self.y += self.dy

    def rebond_murs(self, largeur):
        # droite
        if self.x + self.rayon > largeur:
            self.x = 2 * (largeur - self.rayon) - self.x
            self.dx = -self.dx
        # gauche
        if self.x - self.rayon < 0:
            self.x = 2 * self.rayon - self.x
            self.dx = -self.dx
        # haut
        if self.y - self.rayon < 0:
            self.y = 2 * self.rayon - self.y
            self.dy = -self.dy

    def touche(self, coords):
        x1, y1, x2, y2 = coords
        return (self.x + self.rayon > x1 and self.x - self.rayon < x2 and
                self.y + self.rayon > y1 and self.y - self.rayon < y2)

    def rebond_raquette(self, raquette):
        x1, y1, x2, y2 = raquette.coords()
        # seulement si la balle descend et touche le dessus de la raquette
        if self.dy > 0 and self.touche((x1, y1, x2, y2)) and self.ancien_y + self.rayon <= y1 + 1:
            self.y = y1 - self.rayon
            self.dy = -self.dy

    def rebond_brique(self, brique):
        """Rebond horizontal ou vertical selon le côté touché."""
        x1, y1, x2, y2 = brique.coords()
        if self.ancien_x + self.rayon <= x1 or self.ancien_x - self.rayon >= x2:
            self.dx = -self.dx
        else:
            self.dy = -self.dy

    def afficher(self):
        r = self.rayon
        self.canvas.coords(self.id, self.x - r, self.y - r, self.x + r, self.y + r)


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
if __name__ == '__main__':
    Jeu().lancer()



