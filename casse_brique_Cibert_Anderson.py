"""
Programme de jeu du casse-brique
Fait par Gabriel CIBERT et Ludivic ANDERSON
Commencé le 06/10/2026
Reste à faire : - faire en sorte que la colision balle-raquette se fasse bien 
- transformer le programme en Programation Orientée Objet avec des classes
- faire les briques cassables

"""

from tkinter import Tk, Button, Canvas, LEFT, NW, PhotoImage
import random
import math


#FONCTIONS

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
    if Y + RAYON + DY > HAUTEUR + 30:
        return Mafenetre.destroy
       # Y = 2 * (HAUTEUR - RAYON) - Y     --> rebond du bas 
       # DY = -DY

    # rebond en haut
    if Y - RAYON + DY < 0:
        Y = 2 * RAYON - Y
        DY = -DY

    #rebond sur la raquette
    if Y + RAYON + DY == canvas.coords(Raquette):
        Y = 2 * (HAUTEUR - RAYON) - Y    
        DY = -DY

    NX = X + DX
    NY = Y + DY

    for brique in Brique:
        x1, y1, x2, y2 = canvas.coords(brique)
 
        # la balle touche-t-elle la brique ?
        if NX + RAYON > x1 and NX - RAYON < x2 and NY + RAYON > y1 and NY - RAYON < y2:
 
            # si la balle était à côté de la brique : rebond horizontal
            if X + RAYON <= x1 or X - RAYON >= x2:
                DX = -DX
            # sinon elle venait du dessus ou du dessous : rebond vertical
            else:
                DY = -DY
 
            # on casse la brique : on l'efface du canvas et de la liste
            canvas.delete(brique)
            Brique.remove(brique)
 
            # une seule brique cassée par déplacement
            break
 
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
        PosX += 50

    # déplacement vers la gauche
    if touche == 'q':
        PosX -= 50

    # on dessine la raquette à sa nouvelle position
    canvas.coords(Raquette, PosX - 50, PosY - 5, PosX + 50, PosY + 5) 

    









#PROGRAMME PRINCIPAL

# direction initiale aléatoire
vitesse = random.uniform(1.8, 2) * 5
angle = random.uniform(math.pi,  2 * math.pi)
# angle = 0

DX = vitesse * math.cos(angle)
DY = vitesse * math.sin(angle)

# Dimension de la fenetre
LARGEUR = 1000
HAUTEUR = 700

# rayon de la balle
RAYON = 10  

# Position initiale de la raquette
PosX = LARGEUR / 2
PosY = 675

# position initiale de la balle : au milieu
X = LARGEUR / 2
Y = 660

# Création de la fenêtre principale (main window)
Mafenetre = Tk()
Mafenetre.geometry('1370x960+160+0')
Mafenetre.title('Casse brique')

# Création d'un widget Canvas (zone graphique)
canvas = Canvas(Mafenetre, width = LARGEUR, height = HAUTEUR, bg = 'white')
canvas.pack(padx = 5, pady = 5)


# Création de la raquette 
Raquette = canvas.create_rectangle( PosX - 50, PosY - 5, PosX + 50, PosY + 5, outline = 'black', fill = 'red' )


# Création d'un objet graphique
Balle = canvas.create_oval( X-RAYON, Y-RAYON, X+RAYON, Y+RAYON, width = 1, outline = 'black', fill = 'yellow')

# Création de la brique
Brique=[]
for i in range(8):
    for j in range(3):
        brique=canvas.create_rectangle((LARGEUR/2 - 420+120*i) - 45, (50 + 50*j) - 13, (LARGEUR/2 - 420 + 120*i) + 45, (50 + 50*j) + 13,  outline = 'black', fill = 'blue') 
        Brique.append(brique)



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