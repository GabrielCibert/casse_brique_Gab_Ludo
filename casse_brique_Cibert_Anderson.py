"""
Programme de jeu du casse-brique
Fait par Gabriel CIBERT et Ludivic ANDERSON
Commencé le 06/10/2026
Reste à faire : - faire en sorte que la colision balle-raquette se fasse bien 
- transformer le programme en Programation Orientée Objet avec des classes

"""

from tkinter import Tk, Button, Canvas, LEFT
import random
import math



# direction initiale aléatoire
vitesse = random.uniform(1.8, 2) * 5
angle = random.uniform(math.pi,  2 * math.pi)
# angle = 0

DX = vitesse * math.cos(angle)
DY = vitesse * math.sin(angle)

# Dimension de la fenetre
LARGEUR = 750 
HAUTEUR = 600

# rayon de la balle
RAYON = 15  

# Position initiale de la raquette
PosX = 375
PosY = 575



# position initiale de la balle : au milieu
X = LARGEUR / 2
Y = 554

def déplacement():
    #Déplacement de la balle
    global X, Y, DX, DY, RAYON, LARGEUR, HAUTEUR

    # rebond à droite
    if X + RAYON + DX > LARGEUR:
        X = 2 * (LARGEUR - RAYON) - X
        DX = -DX

    # rebond à gauche
    if X - RAYON + DX < 0:
        X = 2 * RAYON - X
        DX = -DX

    #  pas de rebond en bas
    if Y + RAYON + DY > HAUTEUR:
        return Mafenetre.destroy
       # Y = 2 * (HAUTEUR - RAYON) - Y     --> rebond du bas 
       # DY = -DY

    # rebond en haut
    if Y - RAYON + DY < 0:
        Y = 2 * RAYON - Y
        DY = -DY

    X = X + DX
    Y = Y + DY

    # affichage
    canvas.coords(Balle, X-RAYON, Y-RAYON, X+RAYON, Y+RAYON)

    # mise à jour toutes les 20 ms
    Mafenetre.after(20, déplacement)

# Gestion de l'événement : appui sur une touche du clavier
def clavier(event):
    global PosX, PosY

    touche = event.keysym
    print(touche)

    # déplacement vers le haut
    #if touche == 'z':
    #    PosY -= 20

    # déplacement vers le bas
    #if touche == 's':
    #    PosY += 20

    # déplacement vers la droite
    if touche == 'd':
        PosX += 20

    # déplacement vers la gauche
    if touche == 'q':
        PosX -= 20

    # on dessine la raquette à sa nouvelle position
    canvas.coords(Raquette, PosX - 30, PosY - 5, PosX + 30, PosY + 5) 


# Création de la fenêtre principale (main window)
Mafenetre = Tk()
Mafenetre.title('Casse brique')

# Création d'un widget Canvas (zone graphique)
canvas = Canvas(Mafenetre, width = LARGEUR, height = HAUTEUR, bg = 'white')
canvas.pack(padx = 5, pady = 5)

# Création du pion
Raquette = canvas.create_rectangle( PosX - 30, PosY - 5, PosX + 30, PosY + 5, outline = 'black', fill = 'red' )


# Création d'un objet graphique
Balle = canvas.create_oval( X-RAYON, Y-RAYON, X+RAYON, Y+RAYON, width = 1, outline = 'black', fill = 'blue')

# Permet au Canvas de recevoir les touches du clavier
canvas.focus_set()
canvas.bind('<Key>', clavier)



# Création d'un widget Button (bouton Go)
BoutonGo = Button(Mafenetre, text = 'Go', command = déplacement)
BoutonGo.pack(side = LEFT, padx = 10, pady = 10)


# Création d'un widget Button
BoutonQuitter = Button(Mafenetre, text = 'Quitter', command = Mafenetre.destroy)
BoutonQuitter.pack(side=LEFT, padx=5, pady=5)


Mafenetre.mainloop()