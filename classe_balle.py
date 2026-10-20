"""
Programme de la classe Brique du jeu casse-brique
Fait par Gabriel CIBERT et Ludovic ANDERSON
Le 20/10/2026
Reste à faire : fini
"""
import math
import random as rd

class Balle:

    def __init__(self, canvas, rayon=10):
        self.canvas = canvas
        self.rayon = rayon
        self.x = 0
        self.y = 0
        self.dx = 0
        self.dy = 0
        self.ancien_x = 0
        self.ancien_y = 0
        self.id = canvas.create_oval(0, 0, 0, 0, width = 1, outline = 'black', fill = 'yellow')

    def placer_sur(self, raquette):
        """Pose la balle sur la raquette et choisit une nouvelle direction vers le haut."""
        self.x = raquette.x
        self.y = raquette.y - raquette.demi_hauteur - self.rayon
        vitesse = rd.uniform(1.8, 2) * 7
        angle = rd.uniform(1.2 * math.pi, 1.8 * math.pi)  # sin < 0 : vers le haut
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