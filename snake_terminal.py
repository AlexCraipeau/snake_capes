import curses
import random
from curses import wrapper, KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

KEY_ESC = 27

LARGEUR = 60
HAUTEUR = 20
SPAWN_TIMER = 10

#########################################################
# Apparition aleatoire d'un fruit sur la carte          #
#########################################################
def spawn_fruit(win, fruits_list, snake_list):
    exists = True
    while exists:
        # Position aleatoire
        fruit_largeur = random.randrange(1, LARGEUR - 1)
        fruit_hauteur = random.randrange(1, HAUTEUR - 1)

        # Check si position deja occupee (par snake ou autre fruit)
        if [fruit_hauteur, fruit_largeur] not in fruits_list + snake_list:
            # store
            fruits_list.append([fruit_hauteur, fruit_largeur])
            exists = False

#########################################################
# Detection de collision du snake avec lui-meme         #
#########################################################
def snake_collision(snake_list):
    return snake_list[0] in snake_list[1:]

#########################################################
# Code principal                                        #
#########################################################
def main(stdscr):
    # --- Initialisation de la zone d'affichage
    stdscr.clear()
    win = curses.newwin(HAUTEUR, LARGEUR, 0, 0)
    win.keypad(1)
    curses.noecho()
    curses.curs_set(0)
    win.nodelay(1)
    # ---

    # Parametres initiaux
    snake_list = [[int(HAUTEUR / 2), int(LARGEUR / 2)]]  # On commence a peu pres au milieu
    tete = snake_list[0] # Tete du snake
    touche = KEY_RIGHT  # Le serpent part a droite au debut
    spawn_cpt = 0 # Compteur d'apparition d'un fruit
    random.seed()

    score = 0
    fruits_list = [] # Liste de fruits presents sur la carte a l'instant t


    while True:
        touchePrec = touche
        touche = win.getch()

        if touche == KEY_ESC:
            break

        if touche not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN]:
            touche = touchePrec

        # Changement de direction
        if touche == KEY_LEFT:
            tete[1] -= 1
        if touche == KEY_RIGHT:
            tete[1] += 1
        if touche == KEY_UP:
            tete[0] -= 1
        if touche == KEY_DOWN:
            tete[0] += 1

        # Gestion de la traversee des bords de la map par la tete -- solution moche dupliquee
        if tete[0] == 0: tete[0] = HAUTEUR - 2
        if tete[1] == 0: tete[1] = LARGEUR - 2
        if tete[0] == HAUTEUR - 1: tete[0] = 1
        if tete[1] == LARGEUR - 1: tete[1] = 1

        # Gestion de la traversee des bords de la map par le corps
        for snake in snake_list:
            if snake[0] == 0: snake[0] = HAUTEUR - 2
            if snake[1] == 0: snake[1] = LARGEUR - 2
            if snake[0] == HAUTEUR - 1: snake[0] = 1
            if snake[1] == LARGEUR - 1: snake[1] = 1

        # Verification de la presence d'un fruit
        if snake_list[0] in fruits_list:
            # Presence d'un fruit : augmentation de la taille du snake
            fruits_list.remove(snake_list[0])
            score += 1
            snake_list.insert(0, list(tete))
        else:
            # Pas de fruit : on met juste a jour la position du snake
            snake_list.insert(0, list(tete))
            snake_list.pop()

        win.clear()  # on efface tout
        win.border(0)  # on dessine une bordure

        # Affichage du corps du snake
        for snake in snake_list[1:]:
            win.addch(snake[0], snake[1], 'o')

        # Affichage des fruits
        for fruit in fruits_list:
            win.addch(fruit[0], fruit[1], '*')

        # Affichage de la tete du snake
        win.addch(snake_list[0][0], snake_list[0][1], '#')
        win.addstr(0, 0, " Score : " + str(score) + " ")

        # Verification de defaite (collision)
        if snake_collision(snake_list):
            break

        win.timeout(150)  # on attend un peu

        # Gestion de l'apparition des fruits sur la carte
        spawn_cpt += 1
        if spawn_cpt == SPAWN_TIMER:
            spawn_cpt = 0
            spawn_fruit(win, fruits_list, snake_list)

    curses.endwin()


wrapper(main)
print('Perdu !')
