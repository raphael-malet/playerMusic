from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

# variable global
en_pause = False
stoper = False
musique_longeur = ''


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
    global musique_longeur
    global stoper
    stoper = False
    # on prend la musique selectionner dans la liste box
    musique = fenetre_liste_musique.get(ACTIVE)
    # on rajoute le chemin du fichier pour que pygame puisse lancer la musique
    musique = f'/Users/raphaelmalet/Documents/git/playerMusic/musique/{musique}.mp3'

    # permet de lancer la musique grace a pygame
    pygame.mixer.music.load(musique)
    pygame.mixer.music.play(loops=0)
    # fonction qui affiche depuis combien de temps la musique est joué
    temps_musique()

    # update slider to position
    # slider_position = int(musique_longeur)
    # barre_progression.config(to=slider_position, value=0)


# fonction qui permet de stop une musique joué
def stop():
    global stoper
    # stop la musique
    pygame.mixer.music.stop()
    # supprime la selection de la musique stopé dans la listbox
    fenetre_liste_musique.select_clear(ACTIVE)
    temps_progression.configure(text='')

    # reset de la barre de progression
    barre_progression.config(value=0)
    temps_progression.config(text='')

    # set stop varaible to true
    stoper = True


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
    barre_progression.config(value=0)
    temps_progression.config(text='')
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
    barre_progression.config(value=0)
    temps_progression.config(text='')
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


# FONCTION TEMPS DE PROGRESSION
def temps_musique():
    global musique_longeur
    global en_pause
    global stoper

    if stoper == True:
        return

    temps_actuelle = pygame.mixer.music.get_pos() / 1000
    # label date
    slider_label.config(text=f'slider: {int(barre_progression.get())} and posditon:{int(temps_actuelle)}')
    #temps_actuelle_modif = time.strftime('%M:%S', time.gmtime(temps_actuelle))
    # avoir la longueur du temps

    # musique_actuelle_temps = fenetre_liste_musique.curselection()
    titre_musique = fenetre_liste_musique.get(ACTIVE)
    tire_musique = f'/Users/raphaelmalet/Documents/git/playerMusic/musique/{titre_musique}.mp3'
    musique_mut = MP3(tire_musique)
    musique_longeur = musique_mut.info.length
    convertir_musique_longeur = time.strftime('%M:%S', time.gmtime(musique_longeur))

    temps_actuelle += 1
    if int(barre_progression.get()) == int(musique_longeur):
        temps_progression.config(text=f'{convertir_musique_longeur} / {convertir_musique_longeur}')
        pass

    elif en_pause:
        pass

    # augmente le temps actuelle de 1s
    elif int(barre_progression.get()) == int(temps_actuelle):
        slider_position = int(musique_longeur)
        barre_progression.config(to=slider_position, value=int(temps_actuelle))


    else:
        slider_position = int(musique_longeur)
        barre_progression.config(to=slider_position, value=int(barre_progression.get()))
        temps_actuelle_modif = time.strftime('%M:%S', time.gmtime(barre_progression.get()))
        temps_progression.config(text=f'{temps_actuelle_modif} / {convertir_musique_longeur}')
        # bouger de 1 seconde
        next_time = int(barre_progression.get())
        barre_progression.config(to=slider_position, value=next_time)

    # actualise la progression de la barre en fonction du temps d'écoute de la musique
    # barre_progression.config(value=temps_actuelle)
    # temps_progression.config(text=f'{temps_actuelle_modif} / {convertir_musique_longeur}')
    # actualisation du temps de progresion
    temps_progression.after(1000, temps_musique)


def slider(x):
    global musique_longeur
    slider_label.config(text=f'{int(barre_progression.get())} sur {int(musique_longeur)}')
    musique = fenetre_liste_musique.get(ACTIVE)
    musique = f'/Users/raphaelmalet/Documents/git/playerMusic/musique/{musique}.mp3'

    pygame.mixer.music.load(musique)
    pygame.mixer.music.play(loops=0, start=int(barre_progression.get()))


if __name__ == '__main__':
    playermusic = Tk()  # nom de la fenetre
    playermusic.configure(bg='')  # background de la fenetre
    playermusic.geometry('500x700')  # taille de la fenetre
    playermusic.title('PlayerMusic')  # titre de la fenetre

    # permet a pygame de lancer les musiques
    pygame.mixer.init()

    # --------
    # MENU
    # ________
    # creation menu
    menu_choix = Menu(playermusic)
    playermusic.configure(menu=menu_choix)

    # ajout musique au player
    ajout_musique = Menu(menu_choix)
    menu_choix.add_cascade(label="ajouter musique", menu=ajout_musique)
    # ajouter une musique au player
    ajout_musique.add_command(label='ajouter une musique', command=ajout_une_musique)
    # ajout plusieurs musiques au player
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
    fenetre_liste_musique = Listbox(playermusic, height=10, width=50, selectbackground='grey')
    fenetre_liste_musique.pack(pady=20)

    # temps de la musique
    temps_progression = Label(playermusic, text='')
    temps_progression.pack(fill=X, ipady=3)

    # fenetre disposition des boutons
    fenetre_bouton = Label(playermusic, height=5, width=50)
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

    # fenetre slider
    barre_progression = ttk.Scale(playermusic, from_=0, to=100, orient=HORIZONTAL, value=0, command=slider, length=455)
    barre_progression.pack(pady=10, )

    slider_label = Label(playermusic, text='0')
    slider_label.pack(pady=10)

    playermusic.mainloop()
