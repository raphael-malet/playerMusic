from tkinter import *
from tkinter import filedialog
import pygame
import time

# variable global
en_pause = False


# -----------
# FONCTION MENU
# -----------

# fonction pour ajouter une musique
def ajout_une_musique():
    # on prend le chemin de la musique
    musique = filedialog.askopenfilename(initialdir="musique/", title='choisir une musique',
                                         filetypes=(("mp3 Files", "*.mp3"),))
    # on supprime le chemin de la musique du nom pour l'insérer dans la liste
    musique = musique.replace("/Users/raphaelmalet/Documents/git/playerMusic/musique/", "")
    musique = musique.replace(".mp3", "")
    # jout nom de la musique a la liste box
    fenetre_liste_musique.insert(END, musique)


# fonction ajout de plusieur musique a la fois
def ajout_plusieur_musique():
    # on prend le chemin de la musique
    musique = filedialog.askopenfilenames(initialdir="musique/", title='choisir une musique',
                                          filetypes=(("mp3 Files", "*.mp3"),))

    # boucle qui prend une musique a la fois, supprime le chemin et l'ajoute a la listebox
    for i in musique:
        # on supprime le chemin de la musique du nom pour l'insérer dans la liste
        i = i.replace("/Users/raphaelmalet/Documents/git/playerMusic/musique/", "")
        i = i.replace(".mp3", "")
        # ajout nom de la musique a la liste box
        fenetre_liste_musique.insert(END, i)


# fonction pour supprimer une musique de la liste
def supprimer_une_musique():
    fenetre_liste_musique.delete(ANCHOR)
    stop()  # on stop la musique supprimer


# fonction qui supprime toutes les musiques de la listebox
def supprimer_toutes_les_musiques():
    fenetre_liste_musique.delete(0, END)
    stop()


# ---------------
# FONCTION BOUTON
# ----------------
# fonction lancer une musique
def lancer_musique():
    # on prend la musique selectionner dans la liste box
    musique = fenetre_liste_musique.get(ACTIVE)
    # on rajoute le chemin du fichier pour que pygame puisse lancer la musique
    musique = f'/Users/raphaelmalet/Documents/git/playerMusic/musique/{musique}.mp3'

    # permet de lancer la musique grace a pygame
    pygame.mixer.music.load(musique)
    pygame.mixer.music.play(loops=0)
    # fonction qui affiche depuis combien de temps la musique est joué
    temps_musique()


# fonction qui permet de stop une musique joué
def stop():
    # stop la musique
    pygame.mixer.music.stop()
    # supprime la selection de la musique stopé dans la listbox
    fenetre_liste_musique.select_clear(ACTIVE)


# fonction qui met en pause une musique
def pause():
    global en_pause
    # si pause = True
    if en_pause:
        # reprendre
        pygame.mixer.music.unpause()  # la musique reprend
        en_pause = False  # on met pause = False pour la prochaine fois qu'on appuis sur le bouton

    else:
        pygame.mixer.music.pause()  # musique se met en pause si en_pause = False
        en_pause = True  # change la valeur pour reprendre la musique une fois qu'on rappuis sur le bouton


# focntion musique suivante
def musique_suivante():
    # avoir la position dans la liste de la musique actuelle
    suivante = fenetre_liste_musique.curselection()
    # on ajoute +1 a la position de la muisque actuelle
    suivante = suivante[0] + 1

    # on efface la sélection de la liste box
    fenetre_liste_musique.select_clear(0, END)

    # permet d'activer la selection sur la musique suivante pour lancer la musique
    fenetre_liste_musique.activate(suivante)
    fenetre_liste_musique.select_set(suivante, last=None)
    lancer_musique()  # lance la musique


# fonction musique précédente
def musique_precedente():
    # avoir la position dans la liste de la musique actuelle
    suivante = fenetre_liste_musique.curselection()
    # on soustrait - 1 a la porsiton actuelle
    suivante = suivante[0] - 1

    # on efface la sélection de la listebox
    fenetre_liste_musique.select_clear(0, END)

    # on active la selection de la listebox sur la musique précédente
    fenetre_liste_musique.activate(suivante)
    fenetre_liste_musique.select_set(suivante, last=None)
    lancer_musique()


# FONCTION BARRE DE PROGRESSIOB
def temps_musique():
    temps_actuelle = pygame.mixer.music.get_pos() / 1000

    temps_actuelle_modif = time.strftime('%M:%S', time.gmtime(temps_actuelle))
    barre_progression.configure(text=temps_actuelle_modif)
    barre_progression.after(1000, temps_musique)


if __name__ == '__main__':
    fenetre = Tk()  # nom de la fenetre
    fenetre.configure(bg='')  # background de la fenetre
    fenetre.geometry('500x700')  # taille de la fenetre
    fenetre.title('PlayerMusic')  # titre de la fenetre

    # permet a pygame de lancer les musiques
    pygame.mixer.init()

    # --------
    # MENU
    # ________
    # creation menu
    menu_choix = Menu(fenetre)
    fenetre.configure(menu=menu_choix)

    # ajout musique au player
    ajout_musique = Menu(menu_choix)
    menu_choix.add_cascade(label="ajouter musique", menu=ajout_musique)
    # ajouter une musique au player
    ajout_musique.add_command(label='ajouter une musique', command=ajout_une_musique)
    # ajout plusieurs musique au player
    ajout_musique.add_command(label='ajouter plusieur musique', command=ajout_plusieur_musique)

    supprime_musique = Menu(menu_choix)
    menu_choix.add_cascade(label="supprimer musique", menu=supprime_musique)
    supprime_musique.add_command(label='suprimer une musique', command=supprimer_une_musique)
    supprime_musique.add_command(label='supprimer toutes les musiques', command=supprimer_toutes_les_musiques)

    # -------------
    # IMAGE BOUTON
    # ------------
    # assossiation des image a des boutons de control
    jouer_img = PhotoImage(file="img/jouer_50.png")
    pause_img = PhotoImage(file='img/pause_50.png')
    arret_img = PhotoImage(file='img/arret_50.png')
    suivant_img = PhotoImage(file="img/piste-suivante_50.png")
    precedent_img = PhotoImage(file="img/piste-precedente_50.png")

    # fenetre liste des musiques
    fenetre_liste_musique = Listbox(fenetre, height=10, width=50, selectbackground='grey')
    fenetre_liste_musique.pack(pady=20)

    # barre de status
    barre_progression = Label(fenetre, text='')
    barre_progression.pack(fill=X, ipady=3)

    # fenetre disposition des boutons
    fenetre_bouton = Label(fenetre, height=5, width=50)
    fenetre_bouton.pack()

    # disposition des boutons de control dans la fenetre dispostion des boutons
    jouer_bouton = Button(fenetre_bouton, image=jouer_img, borderwidth=0, command=lancer_musique)
    jouer_bouton.grid(row=0, column=1, padx=10)
    pause_bouton = Button(fenetre_bouton, image=pause_img, borderwidth=0, command=pause)
    pause_bouton.grid(row=0, column=2, padx=10)
    arret_bouton = Button(fenetre_bouton, image=arret_img, borderwidth=0, command=stop)
    arret_bouton.grid(row=0, column=4, padx=10)
    suivant_bouton = Button(fenetre_bouton, image=suivant_img, borderwidth=0, command=musique_suivante)
    suivant_bouton.grid(row=0, column=3, padx=10)
    precedent_bouton = Button(fenetre_bouton, image=precedent_img, borderwidth=0, command=musique_precedente)
    precedent_bouton.grid(row=0, column=0, padx=10)

    fenetre.mainloop()
