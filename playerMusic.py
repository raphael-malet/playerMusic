import os
import time
import tkinter.ttk as ttk
from tkinter import *
from tkinter import filedialog
import pygame
import random
from mutagen.mp3 import MP3

# variable global
en_pause = False
stoper = False
en_boucle = False
en_aleatoire = True


# avoir le chemin du fichier musique.
def obtenir_chemin():
    chemin = os.getcwd()
    chemin = chemin.split('\\')
    chemin.append('musique/')
    chemin = '/'.join(chemin)
    return chemin


# on remet le chemin pour pouvoir lancer la musique
def chemine_musique_lancement():
    chemin_musique = obtenir_chemin()
    chemin_musique = chemin_musique.split('/')
    chemin_musique = '\\'.join(chemin_musique)
    return chemin_musique


# -----------
# FONCTION MENU
# -----------

# fonction pour ajouter une musique
def ajout_une_musique():
    # on prend le chemin de la musique
    musique = filedialog.askopenfilename(initialdir="musique/", title='choisir une musique',
                                         filetypes=(("mp3 Files", "*.mp3"),))
    # on supprime le chemin de la musique du nom pour l'insérer dans la liste
    musique = musique.replace(obtenir_chemin(), "")
    musique = musique.replace(".mp3", "")
    # ajout nom de la musique a la liste box
    fenetre_liste_musique.insert(END, musique)


# fonction ajout de plusieur musique a la fois
def ajout_plusieur_musique():
    # on prend le chemin de la musique
    musique = filedialog.askopenfilenames(initialdir="musique/", title='choisir une musique',
                                          filetypes=(("mp3 Files", "*.mp3"),))

    # boucle qui prend une musique a la fois, supprime le chemin et l'ajoute a la listebox
    for i in musique:
        # on supprime le chemin de la musique du nom pour l'insérer dans la liste
        i = i.replace(obtenir_chemin(), "")
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
    global stoper
    global en_pause
    global en_boucle
    en_pause = False
    stoper = False
    # on prend la musique selectionner dans la liste box
    musique = fenetre_liste_musique.get(ACTIVE)
    # on rajoute le chemin du fichier pour que pygame puisse lancer la musique
    musique = f'{chemine_musique_lancement()}{musique}.mp3'

    # permet de lancer la musique grace a pygame
    pygame.mixer.music.load(musique)
    # condition si on veut lancer la musique est lancé en boucle ou non
    if en_boucle:
        pygame.mixer.music.play(loops=-1)
        en_boucle = False
    else:
        pygame.mixer.music.play(loops=0)

    # on remet les timer et la barre de progression a 0
    defilement_temps.config(text='00:00')
    temps_global_musique.config(text='00:00')
    slider_musique.config(value=0)
    # fonction qui affiche depuis combien de temps la musique est joué
    temps_musique()


# fonction qui permet de stop une musique joué
def stop():
    global stoper
    stoper = True
    # reset le slider de la musique pourqu'il reparte a 0
    slider_musique.config(value=0)
    # stop la musique
    pygame.mixer.music.stop()
    # supprime la selection de la musique stopé dans la listbox
    fenetre_liste_musique.select_clear(ACTIVE)
    # clear les temps de la musique
    defilement_temps.config(text='00:00')
    temps_global_musique.config(text='00:00')


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
    global stoper
    stoper = False
    # on prend la postion de la musique en cours
    suivante = fenetre_liste_musique.curselection()
    # on ajoute +1 a la position de la muisque actuelle
    suivante = suivante[0] + 1

    # condition pour savoir si on arrive au bout de la liste de musique
    if int(suivante) < fenetre_liste_musique.size():
        # on efface la sélection de la liste box
        fenetre_liste_musique.select_clear(0, END)
        # permet d'activer la selection sur la musique suivante pour lancer la musique
        fenetre_liste_musique.activate(suivante)
        fenetre_liste_musique.select_set(suivante, last=None)
        # in remet les timer et la barre de progression a 0
        defilement_temps.config(text='00:00')
        temps_global_musique.config(text='00:00')
        slider_musique.config(value=0)
        # permet de connaitre le nom de la musique active
        musique = fenetre_liste_musique.get(ACTIVE)
        # on rajoute le chemin du fichier pour que pygame puisse lancer la musique
        musique = f'{chemine_musique_lancement()}{musique}.mp3'
        # permet de lancer la musique grace a pygame
        pygame.mixer.music.load(musique)
        pygame.mixer.music.play(loops=0)
    # on reprend au debut de la liste de musique
    else:
        # on efface la sélection de la liste box
        fenetre_liste_musique.select_clear(0, END)

        # permet d'activer la selection sur la premiere musique pour lancer la musique
        fenetre_liste_musique.activate(0)
        fenetre_liste_musique.select_set(0, last=None)
        # remettre les timer ete barre de progression a 0
        defilement_temps.config(text='00:00')
        temps_global_musique.config(text='00:00')
        slider_musique.config(value=0)
        musique = fenetre_liste_musique.get(ACTIVE)
        # on rajoute le chemin du fichier pour que pygame puisse lancer la musique
        musique = f'{chemine_musique_lancement()}{musique}.mp3'
        # permet de lancer la musique grace a pygame
        pygame.mixer.music.load(musique)
        pygame.mixer.music.play(loops=0)


# fonction musique précédente
def musique_precedente():
    global stoper
    stoper = False
    suivante = fenetre_liste_musique.curselection()
    # on soustrait -1 a la position de la musique actuelle
    suivante = suivante[0] - 1
    # savot si on arrive au bout de la liste de musique
    if int(suivante) >= 0:
        # on efface la sélection de la liste box
        fenetre_liste_musique.select_clear(0, END)
        # permet d'activer la selection sur la musique suivante pour lancer la musique
        fenetre_liste_musique.activate(suivante)
        fenetre_liste_musique.select_set(suivante, last=None)
        # on remet barre de progression et timer a 0
        defilement_temps.config(text='00:00')
        temps_global_musique.config(text='00:00')
        slider_musique.config(value=0)
        musique = fenetre_liste_musique.get(ACTIVE)
        # on rajoute le chemin du fichier pour que pygame puisse lancer la musique
        musique = f'{chemine_musique_lancement()}{musique}.mp3'
        # permet de lancer la musique grace a pygame
        pygame.mixer.music.load(musique)
        pygame.mixer.music.play(loops=0)

    # si on arrive au bout de la liste de musique on repart sur la derniere musique de la liste
    else:
        # on efface la sélection de la liste box
        fenetre_liste_musique.select_clear(0, END)

        # permet d'activer la selection sur la premiere musique pour lancer la musique
        fenetre_liste_musique.activate(END)
        fenetre_liste_musique.select_set(END, last=None)
        defilement_temps.config(text='00:00')
        temps_global_musique.config(text='00:00')
        slider_musique.config(value=0)
        musique = fenetre_liste_musique.get(ACTIVE)
        # on rajoute le chemin du fichier pour que pygame puisse lancer la musique
        musique = f'{chemine_musique_lancement()}{musique}.mp3'
        # permet de lancer la musique grace a pygame
        pygame.mixer.music.load(musique)
        pygame.mixer.music.play(loops=0)


# fonction passage automatique de la musqiue
def passage_auto_musique():
    # conditon pour savoir si une musique est joué ou non
    if en_pause or pygame.mixer.music.get_busy():
        return
    else:
        musique_suivante()  # si une musique n'est pas joué on passe a la musique suivante


# fonction mettre en boucle une musique
def boucle_musique():
    global en_boucle
    en_boucle = False
    if en_boucle:
        en_boucle = False
        lancer_musique()
    else:
        en_boucle = True
        lancer_musique()


# fonction augmenter le son
def augmenter_son():
    volume = pygame.mixer.music.get_volume()  # on prend le colume actuel
    volume += 0.1  # on ajoute 0.1 au volume
    pygame.mixer.music.set_volume(volume)  # on update le vollume


# fonction baisser le son
def baisser_son():
    volume = pygame.mixer.music.get_volume()
    volume -= 0.1
    pygame.mixer.music.set_volume(volume)


# fonction permet de choisir une musique aléatoirement dans la liste de musique
def musique_aleatoire():
    global stoper
    global en_aleatoire
    stoper = False
    taille_liste = fenetre_liste_musique.size()  # on prend la taille de la liste musique
    choix = random.randrange(taille_liste)  # on choisit un nombre aléatoirement
    fenetre_liste_musique.select_clear(0, END)  # on clear la selection de la liste box
    # permet d'activer la selection sur la musique choisit pour lancer la musique
    fenetre_liste_musique.activate(choix)
    fenetre_liste_musique.select_set(choix, last=None)
    defilement_temps.config(text='00:00')
    temps_global_musique.config(text='00:00')
    slider_musique.config(value=0)
    musique = fenetre_liste_musique.get(ACTIVE)
    # on rajoute le chemin du fichier pour que pygame puisse lancer la musique
    musique = f'{chemine_musique_lancement()}{musique}.mp3'
    # permet de lancer la musique grace a pygame
    pygame.mixer.music.load(musique)
    pygame.mixer.music.play(loops=0)
    # permet de lancer le temps de la musique si c'est la premiere action effectuer
    if en_aleatoire:
        temps_musique()
        en_aleatoire = False


# FONCTION BARRE DE PROGRESSION
def temps_musique():
    global en_pause
    global musique_longueur
    global stoper

    if stoper:
        return

    # temps de la musique passé
    # convertir le temps de la musique en seconde
    temps_actuelle = pygame.mixer.music.get_pos() / 1000

    # mettre le format minute: seconde
    temps_actuelle_modif = time.strftime('%M:%S', time.gmtime(temps_actuelle))
    # temps global de la musique
    # prendre la position de la musique dans la liste box
    musique_jouer = fenetre_liste_musique.curselection()
    # prendre le nom de la musique dans la liste box
    musique = fenetre_liste_musique.get(musique_jouer)
    # avoir le chemin de la musique
    musique = f'{chemine_musique_lancement()}{musique}.mp3'
    # avoir le temps de la musique grace a mutagen
    musique_mutagen_longueur = MP3(musique)
    musique_longueur = musique_mutagen_longueur.info.length

    # la longueur est en second on la modifie en minute:seconde.
    musique_longueur_modif = time.strftime('%M:%S', time.gmtime(musique_longueur))
    # on stop le timer une fois arriver a la fin
    if int(slider_musique.get()) == int(musique_longueur):
        defilement_temps.config(text=musique_longueur_modif)
    # permet de mettre en pause le timer si en_pause = True
    elif en_pause:
        pass

    else:
        # modifer la longeur du slider a la longueur de la musique
        slider_musique.config(to=int(musique_longueur), value=slider_musique.get())
        # afficher le temps dans la fentre barre-progression
        temps_actuelle_modif = time.strftime('%M:%S', time.gmtime(int(slider_musique.get())))
        defilement_temps.config(text=temps_actuelle_modif)
        temps_global_musique.config(text=musique_longueur_modif)
        # bouger la barre de progression une fois bouger
        bouger = int(slider_musique.get()) + 1
        slider_musique.config(value=bouger)

    # fonction passer a la musique precedente si fini
    passage_auto_musique()
    # actualisation de la focntion toute les secondes
    defilement_temps.after(1000, temps_musique)


# fonction permet de modifer les parametre du slider a chaque musique
def slider(x):
    # on prend la musique selectionner dans la liste box
    musique = fenetre_liste_musique.get(ACTIVE)
    # on rajoute le chemin du fichier pour que pygame puisse lancer la musique
    musique = f'{chemine_musique_lancement()}{musique}.mp3'
    # permet de lancer la musique grace a pygame sur la position du slider
    pygame.mixer.music.load(musique)
    # on defini la taille du slider et sa positon
    pygame.mixer.music.play(loops=0, start=int(slider_musique.get()))


if __name__ == '__main__':
    fenetre = Tk()  # nom de la fenetre
    fenetre.configure(bg='grey')  # background de la fenetre
    fenetre.geometry('400x319')  # taille de la fenetre
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
    # association des image a des boutons de control
    jouer_img = PhotoImage(file="img/jouer_50.png")
    pause_img = PhotoImage(file='img/pause_50.png')
    arret_img = PhotoImage(file='img/arret_50.png')
    suivant_img = PhotoImage(file="img/piste-suivante_50.png")
    precedent_img = PhotoImage(file="img/piste-precedente_50.png")
    boucle = PhotoImage(file="img/loop_50.png")
    aleatoire = PhotoImage(file="img/random_50.png")
    son_plus = PhotoImage(file="img/son_plus_50.png")
    son_moin = PhotoImage(file="img/son_moin_50.png")

    # fenetre liste des musiques
    fenetre_liste_musique = Listbox(fenetre, height=10, width=65, selectbackground='green', bg='#808080', fg='green')
    fenetre_liste_musique.pack(pady=0)

    # slider musique
    slider_musique = ttk.Scale(fenetre, from_=0, to=100, orient=HORIZONTAL, value=0, command=slider, length=400)
    slider_musique.pack(pady=0)

    # section affichage temps
    fenetre_temps_progression = Label(fenetre, text='', borderwidth=0)
    fenetre_temps_progression.pack(ipady=0)

    # affichage temps musique écouté
    defilement_temps = Label(fenetre_temps_progression, text='00:00')
    defilement_temps.grid(row=0, column=0, sticky=W, ipadx=85)
    # affichage temps global musique
    temps_global_musique = Label(fenetre_temps_progression, text='00:00')
    temps_global_musique.grid(row=0, column=1, ipadx=85, sticky=E)

    # fenetre disposition des boutons
    fenetre_bouton = Label(fenetre, height=5, width=100)
    fenetre_bouton.pack()

    # disposition des boutons de control dans la fenetre dispostion des boutons
    jouer_bouton = Button(fenetre_bouton, image=jouer_img, borderwidth=0, command=lancer_musique)
    jouer_bouton.grid(row=0, column=1, padx=15)

    pause_bouton = Button(fenetre_bouton, image=pause_img, borderwidth=0, command=pause)
    pause_bouton.grid(row=0, column=2, padx=15)

    arret_bouton = Button(fenetre_bouton, image=arret_img, borderwidth=0, command=stop)
    arret_bouton.grid(row=0, column=4, padx=15)

    suivant_bouton = Button(fenetre_bouton, image=suivant_img, borderwidth=0, command=musique_suivante)
    suivant_bouton.grid(row=0, column=3, padx=15)

    precedent_bouton = Button(fenetre_bouton, image=precedent_img, borderwidth=0, command=musique_precedente)
    precedent_bouton.grid(row=0, column=0, padx=15)

    aleatoire_bouton = Button(fenetre_bouton, image=aleatoire, borderwidth=0, command=musique_aleatoire)
    aleatoire_bouton.grid(row=1, column=0, columnspan=2, padx=15)

    boucle_bouton = Button(fenetre_bouton, image=boucle, borderwidth=0, command=boucle_musique)
    boucle_bouton.grid(row=1, column=1, columnspan=2, padx=15)

    son_plus_bouton = Button(fenetre_bouton, image=son_plus, borderwidth=0, command=augmenter_son)
    son_plus_bouton.grid(row=1, column=2, columnspan=2, padx=15)

    son_moin_bouton = Button(fenetre_bouton, image=son_moin, borderwidth=0, command=baisser_son)
    son_moin_bouton.grid(row=1, column=3, columnspan=2, padx=15)

    fenetre.mainloop()
