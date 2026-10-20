"""
Programme de la classe Raquette du jeu casse-brique
Fait par Gabriel CIBERT et Ludovic ANDERSON
Le 20/10/2026
Reste à faire : fini
"""

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
        self.x += direction * self.pas
        # pour que la raquette reste dans la fenêtre
        self.x = max(self.demi_largeur, min(self.largeur_zone - self.demi_largeur, self.x))
        self.afficher()

    def afficher(self):
        self.canvas.coords(self.id,
                           self.x - self.demi_largeur, self.y - self.demi_hauteur,
                           self.x + self.demi_largeur, self.y + self.demi_hauteur)

    def coords(self):
        return self.canvas.coords(self.id)