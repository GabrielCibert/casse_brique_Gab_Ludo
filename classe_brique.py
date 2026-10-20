"""
Programme de la classe Brique du jeu casse-brique
Fait par Gabriel CIBERT et Ludovic ANDERSON
Le 20/10/2026
Reste à faire : fini
"""


class Brique:

    def __init__(self, canvas, centre_x, centre_y):
        self.canvas = canvas
        self.id = canvas.create_rectangle(centre_x - 45, centre_y - 13,
                                          centre_x + 45, centre_y + 13,
                                          outline = 'black', fill = 'blue')

    def coords(self):
        return self.canvas.coords(self.id)

    def detruire(self):
        self.canvas.delete(self.id)