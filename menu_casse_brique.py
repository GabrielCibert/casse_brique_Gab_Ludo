'''
Programme du menu principal du jeu
Fait par Gabriel CIBERT et Ludovic ANDERSON
Commencé le 17/10/2026
Reste à faire : TOUT !!!
'''

from tkinter import Tk, Button, Canvas, LEFT, NW, PhotoImage, Label, Menu, Frame
from classe_jeu import Jeu

# Fenêtre du menu
Menu_principal = Tk()
Menu_principal.geometry('1002x668+160+0')
Menu_principal.title('Menu Casse Brique')
Menu_principal['bg'] = 'darkviolet'
Menu_principal.border = 1




# Canvas du menu principal
canvas_menu = Canvas(Menu_principal, width = 1000, height = 670, bg = 'darkviolet', highlightbackground = 'darkviolet')
canvas_menu.grid(padx = 0, pady = 0)

# aide
#frame = Frame(Menu_principal)
#labelf = Label(frame, text = "Aide")
#menu_aide = Menu(Menu_principal)
#aide = Menu(menu_aide, tearoff = 0)
#menu_aide.add_cascade(label = "Aide", menu = aide)
#menu_aide.pack()





# Bouton Jouer
bouton_jouer = Button(Menu_principal, text = 'Jouer', command = Menu_principal.destroy, relief = 'sunken', bg = 'darkviolet', width = 10, height = 2)
canvas_menu.create_window(500, 300, window = bouton_jouer)

# Bouton Options
bouton_options = Button(Menu_principal, text = 'Options', command = Menu_principal.destroy, relief = 'sunken', bg = 'darkviolet', width = 10, height = 2)
canvas_menu.create_window(500, 370, window = bouton_options)

#Bouton Quitter
bouton_quitter = Button(Menu_principal, text = 'Quitter', command = Menu_principal.destroy, relief = 'sunken', bg = 'darkviolet', width = 10, height = 2)
canvas_menu.create_window(500, 440, window = bouton_quitter)





# Label du jeu
label_jeu = Label(Menu_principal, text = 'Casse Brique !!!', bg = 'darkviolet', width = 40, height = 2)
canvas_menu.create_window(500, 100, window = label_jeu)

# Image menu
image1 = PhotoImage(file = "photo_menu_casse_brique.ppm")
canvas_menu.create_image(0 , 0 , anchor = NW , image = image1)
canvas_menu.image = image1

if __name__ == '__main__':
    Jeu().lancer()


#Menu_principal.config(menu = menu_aide)
Menu_principal.mainloop()
